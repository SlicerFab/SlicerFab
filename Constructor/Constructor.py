import os
import unittest
from __main__ import vtk, qt, ctk, slicer
from slicer.ScriptedLoadableModule import *

#
# Constructor
#

class Constructor(ScriptedLoadableModule):
  """Uses ScriptedLoadableModule base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def __init__(self, parent):
    ScriptedLoadableModule.__init__(self, parent)
    self.parent.title = "Constructor" # TODO make this more human readable by adding spaces
    self.parent.categories = ["SlicerFab"]
    self.parent.dependencies = []
    self.parent.contributors = ["Steve Pieper (Isomics, Inc.)"] # replace with "Firstname Lastname (Organization)"
    self.parent.helpText = """
    Make segmentations by composition volumes.
    """
    self.parent.acknowledgementText = """
    This file was originally developed by Jean-Christophe Fillion-Robin, Kitware Inc.
    and Steve Pieper, Isomics, Inc. and was partially funded by NIH grant 3P41RR013218-12S1.
""" # replace with organization, grant and thanks.

#
# ConstructorWidget
#

class ConstructorWidget(ScriptedLoadableModuleWidget):
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


    # Add vertical spacer
    self.layout.addStretch(1)

  def cleanup(self):
    pass


#
# ConstructorLogic
#

class ConstructorLogic(ScriptedLoadableModuleLogic):
  """This class should implement all the actual
  computation done by your module.  The interface
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget.
  Uses ScriptedLoadableModuleLogic base class, available at:
  https://github.com/Slicer/Slicer/blob/master/Base/Python/slicer/ScriptedLoadableModule.py
  """

  def run(self):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    return True

  def iceCream(self):

    # based on iceCream.py from VTK/Examples/Modelling

    # This example demonstrates how to use boolean combinations of implicit
    # functions to create a model of an ice cream cone.

    import vtk
    from vtk.util.colors import chocolate, mint

    # Create implicit function primitives. These have been carefully
    # placed to give the effect that we want. We are going to use various
    # combinations of these functions to create the shape we want; for
    # example, we use planes intersected with a cone (which is infinite in
    # extent) to get a finite cone.
    cone = vtk.vtkCone()
    cone.SetAngle(20)
    vertPlane = vtk.vtkPlane()
    vertPlane.SetOrigin(.1, 0, 0)
    vertPlane.SetNormal(-1, 0, 0)
    basePlane = vtk.vtkPlane()
    basePlane.SetOrigin(1.2, 0, 0)
    basePlane.SetNormal(1, 0, 0)
    iceCream = vtk.vtkSphere()
    iceCream.SetCenter(1.333, 0, 0)
    iceCream.SetRadius(0.5)
    bite = vtk.vtkSphere()
    bite.SetCenter(1.5, 0, 0.5)
    bite.SetRadius(0.25)

    # Combine primitives to build ice-cream cone. Clip the cone with planes.
    theCone = vtk.vtkImplicitBoolean()
    theCone.SetOperationTypeToIntersection()
    theCone.AddFunction(cone)
    theCone.AddFunction(vertPlane)
    theCone.AddFunction(basePlane)

    # Take a bite out of the ice cream.
    theCream = vtk.vtkImplicitBoolean()
    theCream.SetOperationTypeToDifference()
    theCream.AddFunction(iceCream)
    theCream.AddFunction(bite)

    # The sample function generates a distance function from the implicit
    # function (which in this case is the cone). This is then contoured to
    # get a polygonal surface.
    theConeSample = vtk.vtkSampleFunction()
    theConeSample.SetImplicitFunction(theCone)
    theConeSample.SetModelBounds(-1, 1.5, -1.25, 1.25, -1.25, 1.25)
    theConeSample.SetSampleDimensions(60, 60, 60)
    theConeSample.ComputeNormalsOff()
    theConeSurface = vtk.vtkContourFilter()
    theConeSurface.SetInputConnection(theConeSample.GetOutputPort())
    theConeSurface.SetValue(0, 0.0)
    coneMapper = vtk.vtkPolyDataMapper()
    coneMapper.SetInputConnection(theConeSurface.GetOutputPort())
    coneMapper.ScalarVisibilityOff()
    coneActor = vtk.vtkActor()
    coneActor.SetMapper(coneMapper)
    coneActor.GetProperty().SetColor(chocolate)

    # The same here for the ice cream.
    theCreamSample = vtk.vtkSampleFunction()
    theCreamSample.SetImplicitFunction(theCream)
    theCreamSample.SetModelBounds(0, 2.5, -1.25, 1.25, -1.25, 1.25)
    theCreamSample.SetSampleDimensions(60, 60, 60)
    theCreamSample.ComputeNormalsOff()
    theCreamSurface = vtk.vtkContourFilter()
    theCreamSurface.SetInputConnection(theCreamSample.GetOutputPort())
    theCreamSurface.SetValue(0, 0.0)
    creamMapper = vtk.vtkPolyDataMapper()
    creamMapper.SetInputConnection(theCreamSurface.GetOutputPort())
    creamMapper.ScalarVisibilityOff()
    creamActor = vtk.vtkActor()
    creamActor.SetMapper(creamMapper)
    creamActor.GetProperty().SetColor(mint)

    # Create the usual rendering stuff
    ren = vtk.vtkRenderer()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)

    # Add the actors to the renderer, set the background and size
    ren.AddActor(coneActor)
    ren.AddActor(creamActor)
    ren.SetBackground(1, 1, 1)
    renWin.SetSize(500, 500)
    ren.ResetCamera()
    ren.GetActiveCamera().Roll(90)
    ren.GetActiveCamera().Dolly(1.5)
    ren.ResetCameraClippingRange()

    iren.Initialize()
    renWin.Render()
    iren.Start()
    return iren



class ConstructorTest(ScriptedLoadableModuleTest):
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
    self.test_Constructor1()

  def test_Constructor1(self):
    """ 
    Construct a simple test volume
    """

    self.delayDisplay("Starting the test",20)

    logic = ConstructorLogic()
    self.assertTrue( logic.run() )
    slicer.modules.ConstructorWidget.iren = logic.iceCream()
    self.delayDisplay('Test passed!')
