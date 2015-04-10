import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

#
# ModelRasterizer
#

class ModelRasterizer(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "ModelRasterizer" # TODO make this more human readable by adding spaces
    self.parent.categories = ["Examples"]
    self.parent.dependencies = []
    self.parent.contributors = ["John Doe (AnyWare Corp.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    This is an example of scripted loadable module bundled in an extension.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# ModelRasterizerWidget
#

class ModelRasterizerWidget(ScriptedLoadableModuleWidget):
  """Uses ScriptedLoadableModuleWidget base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py


TODO: change this process into a module


Target resolution:

600dpi on X
300dpi on Y
0.03mm per slice
 
X has to be divisible by 16
 
 

Basic proof of concept:


Python 2.7.3 (default, Nov  2 2014, 17:15:01) 
[GCC 4.2.1 Compatible Clang 3.1 ((tags/RELEASE_31/final))] on darwin
>>> 
>>> pdtis = vtk.vtkPolyDataToImageStencil()
>>> m = getNode('jig*')
>>> v = getNode('CT*')
>>> pdtis.SetInputData(m.GetPolyData())
>>> m.GetPolyData().GetBounds()
(-180.0, 90.0, -90.0, 90.0, -177.0, -93.0)
>>> pdtis.SetOutputWholeExtent(m.GetPolyData().GetBounds())
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: SetOutputWholeExtent argument 1: integer argument expected, got float
>>> pdtis.SetOutputWholeExtent(0, 600, 0, 600, 0, 600)
>>> pdtis.SetOutputOrigin( -300, -300, -300)
>>> pdtis.SetOutputSpacing(1,1,1)
>>> pdtis.Update()
>>> nw = slicer.vtkNRRDWriter()
>>> nw.SetFileName("/tmp/stencil.nrrd")
>>> nw.Write()
0
>>> nw.SetInputData(pdtis.GetOutput())
>>> nw.Write()
1
>>> print(nw)
vtkNRRDWriter (0x156146d80)
  Debug: Off
  Modified Time: 4018004
  Reference Count: 2
  Registered Events: (none)
  Executive: 0x13fe6d420
  ErrorCode: Undefined error: 0
  Information: 0x141e63750
  AbortExecute: Off
  Progress: 0
  Progress Text: (None)
  RAS to IJK Matrix:   Debug: Off
  Modified Time: 4016615
  Reference Count: 1
  Registered Events: (none)
  Elements:
    1 0 0 0 
    0 1 0 0 
    0 0 1 0 
    0 0 0 1 
  Measurement frame:   Debug: Off
  Modified Time: 4016616
  Reference Count: 1
  Registered Events: (none)
  Elements:
    1 0 0 0 
    0 1 0 0 
    0 0 1 0 
    0 0 0 1 


>>> nw.GetFileName()
'/tmp/stencil.nrrd'
>>> nw.Write()
1
>>> 
>>> vtk.vtkWriter()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: this is an abstract class and cannot be instantiated
>>> vtk.vtkBMPWriter()
(vtkBMPWriter)0x13ca51ef0
>>> bw = vtk.vtkBMPWriter()
>>> bw.SetFilePattern('/tmp/bmps/image-%03d.bmp')
>>> bw.SetInputConnection(pdtis.GetOutputPort())
>>> bw.Write()
>>> nw.SetInputConnection(pdtis.GetOutputPort())
>>> nw.Update()
>>> nw.Write()
1
>>> pdtis.GetOutput()
(vtkImageStencilData)0x13ca51ef0
>>> pdtis.GetOutput().GetScalarRange()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: GetScalarRange
>>> print(pdtis.GetOutput())
vtkImageStencilData (0x1425a98c0)
  Debug: Off
  Modified Time: 3957911
  Reference Count: 2
  Registered Events: (none)
  Information: 0x1425a9970
  Data Released: False
  Global Release Data: Off
  UpdateTime: 4016167
  Field Data:
    Debug: Off
    Modified Time: 3951974
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
  Extent: (0, 600, 0, 600, 0, 600)
  Spacing: (1, 1, 1)
  Origin: (-300, -300, -300)


>>> pdtis.GetOutputDataObject()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: GetOutputDataObject() takes exactly 1 argument (0 given)
>>> pdtis.GetOutputDataObject(0)
(vtkImageStencilData)0x13ca51ef0
>>> st = pdtis.GetOutputDataObject(0)
>>> print(st)
vtkImageStencilData (0x1425a98c0)
  Debug: Off
  Modified Time: 3957911
  Reference Count: 2
  Registered Events: (none)
  Information: 0x1425a9970
  Data Released: False
  Global Release Data: Off
  UpdateTime: 4016167
  Field Data:
    Debug: Off
    Modified Time: 3951974
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
  Extent: (0, 600, 0, 600, 0, 600)
  Spacing: (1, 1, 1)
  Origin: (-300, -300, -300)


>>> ti = vtk.vtkImageStencilToImage()
>>> ti.SetInputConnection(pdtis.GetOutputDataObject(0))
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: SetInputConnection argument 1: method requires a vtkAlgorithmOutput, a vtkImageStencilData was provided.
>>> ti.SetInputData(pdtis.GetOutputDataObject(0))
>>> ti.GetOutputDataObject()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
TypeError: GetOutputDataObject() takes exactly 1 argument (0 given)
>>> ti.GetOutputDataObject(0)
(vtkImageData)0x13c9cead0
>>> i = ti.GetOutputDataObject(0)
>>> print(i)
vtkImageData (0x141d4ac70)
  Debug: Off
  Modified Time: 4032089
  Reference Count: 2
  Registered Events: (none)
  Information: 0x1243f7260
  Data Released: False
  Global Release Data: Off
  UpdateTime: 0
  Field Data:
    Debug: Off
    Modified Time: 4032086
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
  Number Of Points: 0
  Number Of Cells: 0
  Cell Data:
    Debug: Off
    Modified Time: 4032089
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
    Copy Tuple Flags: ( 1 1 1 1 1 0 1 1 )
    Interpolate Flags: ( 1 1 1 1 1 0 0 1 )
    Pass Through Flags: ( 1 1 1 1 1 1 1 1 )
    Scalars: (none)
    Vectors: (none)
    Normals: (none)
    TCoords: (none)
    Tensors: (none)
    GlobalIds: (none)
    PedigreeIds: (none)
    EdgeFlag: (none)
  Point Data:
    Debug: Off
    Modified Time: 4032088
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
    Copy Tuple Flags: ( 1 1 1 1 1 0 1 1 )
    Interpolate Flags: ( 1 1 1 1 1 0 0 1 )
    Pass Through Flags: ( 1 1 1 1 1 1 1 1 )
    Scalars: (none)
    Vectors: (none)
    Normals: (none)
    TCoords: (none)
    Tensors: (none)
    GlobalIds: (none)
    PedigreeIds: (none)
    EdgeFlag: (none)
  Bounds: 
    Xmin,Xmax: (1, -1)
    Ymin,Ymax: (1, -1)
    Zmin,Zmax: (1, -1)
  Compute Time: 4032292
  Spacing: (1, 1, 1)
  Origin: (0, 0, 0)
  Dimensions: (0, 0, 0)
  Increments: (0, 0, 0)
  Extent: (0, -1, 0, -1, 0, -1)


>>> ti.Update()
>>> i = ti.GetOutputDataObject(0)
>>> print(i)
vtkImageData (0x141d4ac70)
  Debug: Off
  Modified Time: 4032591
  Reference Count: 2
  Registered Events: (none)
  Information: 0x1243f7260
  Data Released: False
  Global Release Data: Off
  UpdateTime: 4032592
  Field Data:
    Debug: Off
    Modified Time: 4032559
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
  Number Of Points: 217081801
  Number Of Cells: 216000000
  Cell Data:
    Debug: Off
    Modified Time: 4032567
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 0
    Number Of Components: 0
    Number Of Tuples: 0
    Copy Tuple Flags: ( 1 1 1 1 1 0 1 1 )
    Interpolate Flags: ( 1 1 1 1 1 0 0 1 )
    Pass Through Flags: ( 1 1 1 1 1 1 1 1 )
    Scalars: (none)
    Vectors: (none)
    Normals: (none)
    TCoords: (none)
    Tensors: (none)
    GlobalIds: (none)
    PedigreeIds: (none)
    EdgeFlag: (none)
  Point Data:
    Debug: Off
    Modified Time: 4032591
    Reference Count: 1
    Registered Events: (none)
    Number Of Arrays: 1
    Array 0 name = ImageScalars
    Number Of Components: 1
    Number Of Tuples: 217081801
    Copy Tuple Flags: ( 1 1 1 1 1 0 1 1 )
    Interpolate Flags: ( 1 1 1 1 1 0 0 1 )
    Pass Through Flags: ( 1 1 1 1 1 1 1 1 )
    Scalars: 
      Debug: Off
      Modified Time: 4032588
      Reference Count: 1
      Registered Events: (none)
      Name: ImageScalars
      Data type: unsigned char
      Size: 217081801
      MaxId: 217081800
      NumberOfComponents: 1
      Information: 0
      Name: ImageScalars
      Number Of Components: 1
      Number Of Tuples: 217081801
      Size: 217081801
      MaxId: 217081800
      LookupTable: (none)
      Array: 0x16ded2000
    Vectors: (none)
    Normals: (none)
    TCoords: (none)
    Tensors: (none)
    GlobalIds: (none)
    PedigreeIds: (none)
    EdgeFlag: (none)
  Bounds: 
    Xmin,Xmax: (6.95322e-310, 7.11353e-310)
    Ymin,Ymax: (2.81211e-314, 2.81211e-314)
    Zmin,Zmax: (6.95322e-310, 4.17889e-307)
  Compute Time: 4032704
  Spacing: (2.67183e-314, 4.94066e-324, 6.95322e-310)
  Origin: (6.95322e-310, 2.81211e-314, 6.95322e-310)
  Dimensions: (601, 601, 601)
  Increments: (0, 0, 0)
  Extent: (0, 600, 0, 600, 0, 600)


>>> i.GetScalarSize()
1
>>> i.GetPointData().GetScalars()
(vtkUnsignedCharArray)0x13c9ceb90
>>> i.GetPointData().GetScalars().GetScalarRange()
Traceback (most recent call last):
  File "<console>", line 1, in <module>
AttributeError: GetScalarRange
>>> i.GetPointData().GetScalars().GetRange()
(0.0, 1.0)
>>> nw.SetInputData(i)
>>> nw.Write()
1



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
    # input volume selector
    #
    self.inputSelector = slicer.qMRMLNodeComboBox()
    self.inputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.inputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.inputSelector.selectNodeUponCreation = True
    self.inputSelector.addEnabled = False
    self.inputSelector.removeEnabled = False
    self.inputSelector.noneEnabled = False
    self.inputSelector.showHidden = False
    self.inputSelector.showChildNodeTypes = False
    self.inputSelector.setMRMLScene( slicer.mrmlScene )
    self.inputSelector.setToolTip( "Pick the input to the algorithm." )
    parametersFormLayout.addRow("Input Volume: ", self.inputSelector)

    #
    # output volume selector
    #
    self.outputSelector = slicer.qMRMLNodeComboBox()
    self.outputSelector.nodeTypes = ( ("vtkMRMLScalarVolumeNode"), "" )
    self.outputSelector.addAttribute( "vtkMRMLScalarVolumeNode", "LabelMap", 0 )
    self.outputSelector.selectNodeUponCreation = False
    self.outputSelector.addEnabled = True
    self.outputSelector.removeEnabled = True
    self.outputSelector.noneEnabled = False
    self.outputSelector.showHidden = False
    self.outputSelector.showChildNodeTypes = False
    self.outputSelector.setMRMLScene( slicer.mrmlScene )
    self.outputSelector.setToolTip( "Pick the output to the algorithm." )
    parametersFormLayout.addRow("Output Volume: ", self.outputSelector)

    #
    # check box to trigger taking screen shots for later use in tutorials
    #
    self.enableScreenshotsFlagCheckBox = qt.QCheckBox()
    self.enableScreenshotsFlagCheckBox.checked = 0
    self.enableScreenshotsFlagCheckBox.setToolTip("If checked, take screen shots for tutorials. Use Save Data to write them to disk.")
    parametersFormLayout.addRow("Enable Screenshots", self.enableScreenshotsFlagCheckBox)

    #
    # scale factor for screen shots
    #
    self.screenshotScaleFactorSliderWidget = ctk.ctkSliderWidget()
    self.screenshotScaleFactorSliderWidget.singleStep = 1.0
    self.screenshotScaleFactorSliderWidget.minimum = 1.0
    self.screenshotScaleFactorSliderWidget.maximum = 50.0
    self.screenshotScaleFactorSliderWidget.value = 1.0
    self.screenshotScaleFactorSliderWidget.setToolTip("Set scale factor for the screen shots.")
    parametersFormLayout.addRow("Screenshot scale factor", self.screenshotScaleFactorSliderWidget)

    #
    # Apply Button
    #
    self.applyButton = qt.QPushButton("Apply")
    self.applyButton.toolTip = "Run the algorithm."
    self.applyButton.enabled = False
    parametersFormLayout.addRow(self.applyButton)

    # connections
    self.applyButton.connect('clicked(bool)', self.onApplyButton)
    self.inputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)
    self.outputSelector.connect("currentNodeChanged(vtkMRMLNode*)", self.onSelect)

    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = ModelRasterizerLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    screenshotScaleFactor = int(self.screenshotScaleFactorSliderWidget.value)
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), enableScreenshotsFlag,screenshotScaleFactor)


#
# ModelRasterizerLogic
#

class ModelRasterizerLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == slicer.qMRMLScreenShotDialog.FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog.ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog.Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog.Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog.Green:
      # green slice window
      widget = lm.sliceWidget("Green")
    else:
      # default to using the full window
      widget = slicer.util.mainWindow()
      # reset the type so that the node is set correctly
      type = slicer.qMRMLScreenShotDialog.FullLayout

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)

  def run(self,inputVolume,outputVolume,enableScreenshots=0,screenshotScaleFactor=1):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    self.enableScreenshots = enableScreenshots
    self.screenshotScaleFactor = screenshotScaleFactor

    self.takeScreenshot('ModelRasterizer-Start','Start',-1)

    return True


class ModelRasterizerTest(ScriptedLoadableModuleTest):
  """
  This is the test case for your scripted module.
  Uses ScriptedLoadableModuleTest base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_ModelRasterizer1()

  def test_ModelRasterizer1(self):
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
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
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

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = ModelRasterizerLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
