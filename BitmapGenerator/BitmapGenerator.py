import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

#
# BitmapGenerator
#

class BitmapGenerator(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "BitmapGenerator" # TODO make this more human readable by adding spaces
    self.parent.categories = ["SlicerFab"]
    self.parent.dependencies = []
    self.parent.contributors = ["Steve Pieper (Isomics, Inc.), Steve Keating (MIT), Ahmed Hosny (Harvard), James Weaver (Harvard)"] # replace with "Firstname Lastname (Organization)"
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
    # Instantiate and connect widgets ...

    #
    # Parameters Area
    #
    parametersCollapsibleButton = ctk.ctkCollapsibleButton()
    parametersCollapsibleButton.text = "Parameters"
    self.layout.addWidget(parametersCollapsibleButton)

    # Layout within the dummy collapsible button
    parametersFormLayout = qt.QFormLayout(parametersCollapsibleButton)


    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass


  def onApplyButton(self):
    logic = BitmapGeneratorLogic()
    volumeRenderingNode = slicer.util.getNode(pattern="VolumeRendering")
    logic = BitmapGeneratorLogic()
    filePattern = '/tmp/slabs/slice_%04d.png' # underscore not dash - will need 2 serial names for both materials
    logic.generate(volumeRenderingNode, filePattern)
    print("Generated to %s" % filePattern)


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
    self.width = 1024
    self.height = 1024
    self.buildDirection = "SI" # TODO: allow other build directions
    self.slabSpacing = 0.03 # in mm, # DONE
    self.slabSpacing = 0.5
    self.slabThickness = 1 # in mm, TODO: confirm this is good - Not sure what this refers to


  def captureBitmap(self,threeDWidget,filePath):

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(threeDWidget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)
    qimage.save(filePath)


  def generate(self,volumeRenderingNode,filePattern="/tmp/slice_%04d.png"): # underscore not dash
    """

    """
    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    # just the 3D window
    mainThreeDWidget = lm.threeDWidget(0).threeDView()
    viewNode = mainThreeDWidget.mrmlViewNode()

    # create the dummy threeD widget
    threeDWidget = slicer.qMRMLThreeDWidget()
    threeDWidget.resize(self.width,self.height)
    threeDWidget.setObjectName("ThreeDWidget%s" % viewNode.GetLayoutLabel())
    threeDWidget.setMRMLScene(slicer.mrmlScene)
    threeDWidget.setMRMLViewNode(viewNode)
    self.threeDWidget = threeDWidget
    threeDWidget.show()

    # configure the view
    cacheViewNode = slicer.vtkMRMLViewNode()
    cacheViewNode.Copy(viewNode)
    viewNode.SetBoxVisible(0)
    viewNode.SetAxisLabelsVisible(0)
    viewNode.SetBackgroundColor((1,1,1))
    viewNode.SetBackgroundColor2((1,1,1))


    roi = volumeRenderingNode.GetROINode()
    roiCenter = [0,]*3
    roiRadius = [0,]*3
    roi.GetXYZ(roiCenter)
    roi.GetRadiusXYZ(roiRadius)
    roi.SetDisplayVisibility(0)
    camera = vtk.vtkCamera()
    camera.SetFocalPoint(roiCenter)
    camera.SetPosition(roiCenter[0], roiCenter[1], roiCenter[2] + roiRadius[2])
    camera.SetViewUp((0, 1, 0))

    mrmlCamera = slicer.util.getNode('Default Scene Camera')
    cacheCamera = vtk.vtkCamera()
    cacheCamera.DeepCopy(mrmlCamera.GetCamera())

    mrmlCamera.GetCamera().DeepCopy(camera)
    viewNode.SetRenderMode(slicer.vtkMRMLViewNode.Orthographic)

    # cycle through the slabs
    slabRadius = list(roiRadius)
    slabRadius[2] = self.slabThickness
    roi.SetRadiusXYZ(slabRadius)
    slabCounter=0
    slabCenter = [roiCenter[0], roiCenter[1], roiCenter[2] - roiRadius[2]]
    slabTop = roiCenter[2] + roiRadius[2]

    threeDView = threeDWidget.threeDView()
    renderWindow = threeDView.renderWindow()
    self.delayDisplay("Starting render...", 300)

    while slabCenter[2] <= slabTop:
      roi.SetXYZ(slabCenter)
      threeDView.forceRender()
      windowToImage = vtk.vtkWindowToImageFilter()
      windowToImage.SetInput(renderWindow)
      writer = vtk.vtkPNGWriter()
      writer.SetInputConnection(windowToImage.GetOutputPort())
      filePath = filePattern % slabCounter
      windowToImage.Update()
      writer.SetFileName(filePath)
      writer.Write()
      slabCounter += 1
      slabCenter[2] = slabCenter[2] + self.slabSpacing

    # reset things
    viewNode.Copy(cacheViewNode)
    mrmlCamera.GetCamera().DeepCopy(cacheCamera)
    roi.SetXYZ(roiCenter)
    roi.SetRadiusXYZ(roiRadius)
    roi.SetDisplayVisibility(1)


    # for debugging convenience
    ##slicer.modules.BitmapGeneratorWidget.threeDWidget = threeDWidget
    ##slicer.modules.BitmapGeneratorWidget.volumeRenderingNode = volumeRenderingNode


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
