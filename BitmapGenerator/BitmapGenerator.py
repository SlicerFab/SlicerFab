import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *
import logging

#
# BitmapGenerator
#

class BitmapGenerator(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Bitmap Generator"
    self.parent.categories = ["SlicerFab"]
    self.parent.dependencies = []
    self.parent.contributors = ["Steve Pieper (Isomics, Inc.), Steve Keating (MIT), Ahmed Hosny (Harvard), James Weaver (Harvard)", Andras Lasso (Queens)] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    Generate bitmap images for 3D printers that use images instead of surface models.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# BitmapGeneratorWidget
#

class BitmapGeneratorWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setup(self):
    ScriptedLoadableModuleWidget.setup(self)

    self.logic = BitmapGeneratorLogic()

    # Instantiate and connect widgets ...

    #
    # Printer parameters Area
    #
    printerParametersCollapsibleButton = ctk.ctkCollapsibleButton()
    printerParametersCollapsibleButton.text = "Printer parameters"
    self.layout.addWidget(printerParametersCollapsibleButton)

    # Layout within the dummy collapsible button
    printerParametersFormLayout = qt.QFormLayout(printerParametersCollapsibleButton)

    self.xResolutionDpiSpinBox = ctk.ctkDoubleSpinBox()
    self.xResolutionDpiSpinBox.setToolTip("Resolution of exported images along X axis.")
    self.xResolutionDpiSpinBox.decimals = 0
    self.xResolutionDpiSpinBox.minimum = 60
    self.xResolutionDpiSpinBox.maximum = 2400
    self.xResolutionDpiSpinBox.suffix = "DPI"
    self.xResolutionDpiSpinBox.value = self.logic.xResolutionDpi
    self.xResolutionDpiSpinBox.singleStep = 100
    printerParametersFormLayout.addRow("X resolution: ", self.xResolutionDpiSpinBox)

    self.yResolutionDpiSpinBox = ctk.ctkDoubleSpinBox()
    self.yResolutionDpiSpinBox.setToolTip("Resolution of exported images along Y axis.")
    self.yResolutionDpiSpinBox.decimals = 0
    self.yResolutionDpiSpinBox.minimum = 60
    self.yResolutionDpiSpinBox.maximum = 2400
    self.yResolutionDpiSpinBox.suffix = "DPI"
    self.yResolutionDpiSpinBox.value = self.logic.yResolutionDpi
    self.yResolutionDpiSpinBox.singleStep = 100
    printerParametersFormLayout.addRow("Y resolution: ", self.yResolutionDpiSpinBox)

    self.layerThicknessMmSpinBox = ctk.ctkDoubleSpinBox()
    self.layerThicknessMmSpinBox.setToolTip("Distance between extracted image slices.")
    self.layerThicknessMmSpinBox.decimals = 4
    self.layerThicknessMmSpinBox.minimum = 0.0001
    self.layerThicknessMmSpinBox.maximum = 50.0
    self.layerThicknessMmSpinBox.suffix = "mm"
    self.layerThicknessMmSpinBox.value = self.logic.slabSpacingMm
    self.layerThicknessMmSpinBox.singleStep = 0.1
    printerParametersFormLayout.addRow("Layer thickness: ", self.layerThicknessMmSpinBox)

    #
    # Output parameters Area
    #
    outputParametersCollapsibleButton = ctk.ctkCollapsibleButton()
    outputParametersCollapsibleButton.text = "Output parameters"
    self.layout.addWidget(outputParametersCollapsibleButton)

    # Layout within the dummy collapsible button
    outputParametersFormLayout = qt.QFormLayout(outputParametersCollapsibleButton)

    self.printScaleSpinBox = ctk.ctkDoubleSpinBox()
    self.printScaleSpinBox.setToolTip("Scale of print size relative to real life size. 1.0 means printing in real life size, <1.0 means printed objects are smaller than in real life.")
    self.printScaleSpinBox.decimals = 3
    self.printScaleSpinBox.minimum = 0.01
    self.printScaleSpinBox.maximum = 100.0
    self.printScaleSpinBox.suffix = "x"
    self.printScaleSpinBox.value = self.logic.printScale
    self.printScaleSpinBox.singleStep = 0.1
    outputParametersFormLayout.addRow("Scale: ", self.printScaleSpinBox)

    #
    # Path
    #
    self.dirPath = ctk.ctkPathLineEdit()
    self.dirPath.filters = ctk.ctkPathLineEdit.Dirs
    self.dirPath.settingKey = 'BitmapGeneratorOutputFolder'
    #self.dirPath.currentPath = "/tmp"
    outputParametersFormLayout.addRow("Output folder: ", self.dirPath)

    #
    # Apply Button
    #
    self.applyButtonLabelGenerate = "Generate bitmaps"
    self.applyButtonLabelCancel = "Cancel" 
    self.applyButton = qt.QPushButton(self.applyButtonLabelGenerate)
    self.applyButton.toolTip = "Start/cancel bitmap generation"
    outputParametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    self.logic.cleanup()

  def onApplyButton(self):
    # Disable apply button to prevent multiple clicks
    self.applyButton.setEnabled(False)
    slicer.app.processEvents()

    if self.applyButton.text == self.applyButtonLabelCancel:
      self.logic.requestCancel()
      return 

    self.applyButton.text = self.applyButtonLabelCancel
    self.applyButton.setEnabled(True)

    self.dirPath.addCurrentPathToHistory()

    try:
      # This can be a long operation - indicate it to the user
      qt.QApplication.setOverrideCursor(qt.Qt.WaitCursor) 
      self.logic.slabSpacingMm = self.layerThicknessMmSpinBox.value
      self.logic.printScale = self.printScaleSpinBox.value
      self.logic.xResolutionDpi = self.xResolutionDpiSpinBox.value
      self.logic.yResolutionDpi = self.yResolutionDpiSpinBox.value
      volumeRenderingNode = slicer.mrmlScene.GetFirstNodeByClass("vtkMRMLVolumeRenderingDisplayNode")
      filePattern = self.dirPath.currentPath + '/slice_%04d.png' # underscore not dash - will need 2 serial names for both materials
      self.logic.generate(volumeRenderingNode, filePattern)
      print("Generated to %s" % filePattern)
    except Exception as e:
      logging.error("Error: {0}".format(e.message))
      import traceback
      traceback.print_exc()
    finally:
      qt.QApplication.restoreOverrideCursor()

    self.applyButton.text = self.applyButtonLabelGenerate
    self.applyButton.setEnabled(True) 

#
# BitmapGeneratorLogic
#

class BitmapGeneratorLogic(ScriptedLoadableModuleLogic):
  """
  Generates the bitmaps by slicing through the current volume rendering ROI
  and saving images.

  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self):
    
    # Size of each generated layer image in pixels
    self.width = 1024
    self.height = 1024

    # Slab spacing: must match the printer's layer thickness.
    self.slabSpacingMm = 0.027 # in mm

    # Resolution within the slab.
    self.xResolutionDpi = 600
    self.yResolutionDpi = 300

    # Scale of print size relative to real life size.
    # Value of 1.0 means printing in real life size.
    # Value less than 1.0 means printed objects are smaller than in real life.
    self.printScale = 1.0

    # Slab thickness defines the thickness of the rendered slab for each layer.
    # Thicker slab will result in more opaque image and less noisy image, but some details may be blurred.
    # TODO: confirm this value is good.
    self.slabThickness = 1.0 # in mm

    # Saves transparency in alpha channel
    self.transparentBackground = True

    # Extra view node and widget for image capture
    self.threeDWidget = None
    self.threeDViewNode = None

    self.cancelRequested = False

  def __del__(self):
    self.cleanup()

  def cleanup(self):
    if self.threeDWidget:
      self.threeDWidget.setMRMLViewNode(None)
      self.threeDWidget.deleteLater()
    if self.threeDViewNode:
      slicer.mrmlScene.RemoveNode(self.threeDViewNode)
    self.threeDWidget = None
    self.threeDViewNode = None

  def requestCancel(self):
    logging.info("User requested cancelling of capture")
    self.cancelRequested = True 

  def create3dView(self, viewOwnerNode):
    """
    :param viewOwnerNode: ownerNode manages this view instead of the layout manager (it can be any node in the scene)
    """

    viewLayoutName = "BitmapGenerator"
    # layout label is usually shorter than the full layout name, but in this case it helps if it is
    # obvious that the widget belongs to this module
    viewLayoutLabel = "BitmapGenerator"

    # Retrieve or create MRML view node
    if not self.threeDViewNode:
      self.threeDViewNode = slicer.mrmlScene.GetSingletonNode("BitmapGenerator","vtkMRMLViewNode")
    if not self.threeDViewNode:
      self.threeDViewNode = slicer.mrmlScene.CreateNodeByClass("vtkMRMLViewNode")
      self.threeDViewNode.UnRegister(None)
      self.threeDViewNode.SetSingletonTag("BitmapGenerator")
      self.threeDViewNode.SetName(viewLayoutName)
      self.threeDViewNode.SetLayoutName(viewLayoutName)
      self.threeDViewNode.SetLayoutLabel(viewLayoutLabel)
      self.threeDViewNode.SetLayoutColor(1, 1, 0)
      self.threeDViewNode.SetAndObserveParentLayoutNodeID(viewOwnerNode.GetID())
      self.threeDViewNode = slicer.mrmlScene.AddNode(self.threeDViewNode)

    # Create widget
    if not self.threeDWidget:
      self.threeDWidget = slicer.qMRMLThreeDWidget()
      self.threeDWidget.setObjectName("ThreeDWidget"+self.threeDViewNode.GetLayoutLabel())
      self.threeDWidget.viewLabel = self.threeDViewNode.GetLayoutLabel()
      self.threeDWidget.viewColor = qt.QColor.fromRgbF(*self.threeDViewNode.GetLayoutColor())
      self.threeDWidget.setMRMLScene(slicer.mrmlScene)
      self.threeDWidget.setMRMLViewNode(self.threeDViewNode)


  def generate(self,volumeRenderingNode,filePattern="/tmp/slice_%04d.png"): # underscore not dash
    self.cancelRequested = False

    # Ensure view node and widget exists and cross-references are up-to-date
    self.create3dView(volumeRenderingNode)
    self.threeDViewNode.SetAndObserveParentLayoutNodeID(volumeRenderingNode.GetID())
    self.threeDWidget.setMRMLViewNode(self.threeDViewNode)

    # Make sure the selected volume rendering node is visible in the capture view
    if not volumeRenderingNode.IsDisplayableInView(self.threeDViewNode.GetID()):
      volumeRenderingNode.AddViewNodeID(self.threeDViewNode.GetID())

    # Configure view and widget
    self.threeDViewNode.SetBoxVisible(0)
    self.threeDViewNode.SetAxisLabelsVisible(0)
    self.threeDViewNode.SetVolumeRenderingQuality(slicer.vtkMRMLViewNode.Normal) # viewNode.Maximum could provide better quality but slower
    self.threeDViewNode.SetRenderMode(slicer.vtkMRMLViewNode.Orthographic)
    self.threeDViewNode.SetBackgroundColor((1,1,1))
    self.threeDViewNode.SetBackgroundColor2((1,1,1))

    # Turn off shading. We do not want any lighting effect (specular reflections, etc.) to be baked into the image.
    originalShade = volumeRenderingNode.GetVolumePropertyNode().GetVolumeProperty().GetShade()
    volumeRenderingNode.GetVolumePropertyNode().GetVolumeProperty().SetShade(False)

    self.threeDWidget.resize(self.width,self.height)
    self.threeDWidget.show()

    # Save original ROI
    volumeRenderingNode.SetCroppingEnabled(True)
    roi = volumeRenderingNode.GetROINode()
    roiCenter = [0]*3
    roiRadius = [0]*3
    roi.GetXYZ(roiCenter)
    roi.GetRadiusXYZ(roiRadius)
    originalRoiVisibility = roi.GetDisplayVisibility()
    roi.SetDisplayVisibility(False)

    cameraPositionOffset = 100.0
    cameraNode = slicer.modules.cameras.logic().GetViewActiveCameraNode(self.threeDViewNode)
    cameraNode.SetFocalPoint(roiCenter)
    cameraNode.SetPosition(roiCenter[0], roiCenter[1], roiCenter[2] + roiRadius[2] + cameraPositionOffset)
    cameraNode.SetViewUp((0, 1, 0))
    cameraNode.GetCamera().SetClippingRange(cameraPositionOffset/2.0, roiRadius[2] * 2 + cameraPositionOffset * 2.0)

    windowSizeInPixels = self.threeDWidget.threeDView().renderWindow().GetSize()

    pixelSizeInMm =  25.4 / self.yResolutionDpi
    heightOfViewportInMm = windowSizeInPixels[1] * pixelSizeInMm / self.printScale
    cameraNode.SetParallelScale(heightOfViewportInMm)

    # cycle through the slabs
    slabRadius = list(roiRadius)
    slabRadius[2] = self.slabThickness
    roi.SetRadiusXYZ(slabRadius)
    slabCounter = 0
    slabCenter = [roiCenter[0], roiCenter[1], roiCenter[2] - roiRadius[2]]
    slabTop = roiCenter[2] + roiRadius[2]
    scaledSlabSpacingMm = self.slabSpacingMm / self.printScale
    numberOfSlabs = int(roiRadius[2] * 2.0 / scaledSlabSpacingMm) + 1

    threeDView = self.threeDWidget.threeDView()
    renderWindow = threeDView.renderWindow()
    renderer = renderWindow.GetRenderers().GetFirstRenderer()

    originalCameraUserTransform = cameraNode.GetCamera().GetUserTransform()
    originalPixelAspect = renderer.GetPixelAspect()
    cameraUserTransform = vtk.vtkTransform()
    cameraUserTransform.Scale(self.xResolutionDpi/self.yResolutionDpi,1.0,1.0)
    cameraNode.GetCamera().SetUserTransform(cameraUserTransform)

    if self.transparentBackground:
      originalAlphaBitPlanes = renderWindow.GetAlphaBitPlanes()
      renderWindow.SetAlphaBitPlanes(1)
      originalGradientBackground = renderer.GetGradientBackground()
      renderer.SetGradientBackground(False)

    logging.info("Starting render...")

    while slabCenter[2] <= slabTop:
      slicer.app.processEvents()
      if self.cancelRequested:
        break

      roi.SetXYZ(slabCenter)
      threeDView.forceRender()
      windowToImage = vtk.vtkWindowToImageFilter()
      if self.transparentBackground:
        windowToImage.SetInputBufferTypeToRGBA()
        renderWindow.Render()

      windowToImage.SetInput(renderWindow)

      # Write to file with custom DPI
      # (use Qt file writer to allow saving DPI values)
      filename = "c:/tmp/test.png"
      windowToImage.Update()
      vtkImage = windowToImage.GetOutput()
      qImage = qt.QImage()
      slicer.qMRMLUtils().vtkImageDataToQImage(vtkImage, qImage)
      inchesPerMeter = 1000/25.4
      qImage.setDotsPerMeterX(self.xResolutionDpi*inchesPerMeter)
      qImage.setDotsPerMeterY(self.yResolutionDpi*inchesPerMeter)
      imagePixmap = qt.QPixmap.fromImage(qImage)
      filePath = filePattern % slabCounter
      imagePixmap.save(filePath)

      slabCounter += 1
      slabCenter[2] = slabCenter[2] + scaledSlabSpacingMm
      logging.info("Slab {0}/{1} saved to {2}".format(slabCounter, numberOfSlabs, filePath))

    self.threeDWidget.hide()

    # reset ROI
    roi.SetXYZ(roiCenter)
    roi.SetRadiusXYZ(roiRadius)
    roi.SetDisplayVisibility(originalRoiVisibility)

    cameraNode.GetCamera().SetUserTransform(originalCameraUserTransform)

    if self.transparentBackground:
      renderWindow.SetAlphaBitPlanes(originalAlphaBitPlanes)
      renderer.SetGradientBackground(originalGradientBackground)

    volumeRenderingNode.GetVolumePropertyNode().GetVolumeProperty().SetShade(originalShade)

    # for debugging convenience
    slicer.modules.BitmapGeneratorWidget.threeDWidget = self.threeDWidget
    slicer.modules.BitmapGeneratorWidget.threeDViewNode = self.threeDViewNode
    slicer.modules.BitmapGeneratorWidget.volumeRenderingNode = volumeRenderingNode

    if self.cancelRequested:
      raise ValueError('User requested cancel.')


class BitmapGeneratorTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    #slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_BitmapGenerator1()

  def savePNGs(self,node,pattern):
    wlc = vtk.vtkImageMapToWindowLevelColors()
    wlc.SetInputData(node.GetImageData())
    if not node.GetLabelMap():
      displayNode = node.GetDisplayNode()
      wlc.SetWindow(displayNode.GetWindow())
      wlc.SetLevel(displayNode.GetLevel())
    wlc.Update()
    print(wlc.GetOutput().GetScalarRange())
    cast = vtk.vtkImageCast()
    cast.SetInputConnection(wlc.GetOutputPort())
    cast.SetOutputScalarTypeToUnsignedChar()
    pngWriter = vtk.vtkPNGWriter()
    pngWriter.SetFilePattern(pattern)
    pngWriter.SetInputConnection(cast.GetOutputPort())
    pngWriter.Write()
    slicer.modules.BitmapGeneratorWidget.pngWriter = pngWriter

  def test_BitmapGenerator1(self):
    mask = slicer.util.getNode('Patient*subv*label')
    self.savePNGs(mask, "/tmp/masks/mask-%d.png")
    self.delayDisplay("Wrote mask", 300)
    masked = slicer.util.getNode('masked')
    self.savePNGs(masked, "/tmp/masked/mask-%d.png")
    self.delayDisplay("Wrote masked", 300)

    self.delayDisplay("Finished")


  def test_BitmapGeneratorScene(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://joe.bwh.harvard.edu/slicer/2015-02-09-fab-Scene.mrb', '2015-02-09-fab-Scene.mrb', slicer.util.loadScene),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeRenderingNode = slicer.util.getNode(pattern="VolumeRendering")
    logic = BitmapGeneratorLogic()
    filePattern = slicer.app.temporaryPath + '/slice-%04d.png'
    logic.generate(volumeRenderingNode, filePattern)
    self.delayDisplay('Saved to ' + filePattern)
    self.delayDisplay('Test passed!')
