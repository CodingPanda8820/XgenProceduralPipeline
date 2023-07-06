import sys, os
import imp, re

from PySide2.QtWidgets import *
from PySide2.QtCore import *
from PySide2.QtGui import *

from shutil import copyfile

# VirtualKey
Qt.Key_Enter = 16777220

from . import xgenAssExporter_Util, xgenAssExporter_StyleSheet
imp.reload(xgenAssExporter_Util)
imp.reload(xgenAssExporter_StyleSheet)

AssFileEdit = xgenAssExporter_Util.AssFileEdit
XgenFileEdit = xgenAssExporter_Util.XgenFileEdit
FileEdit = xgenAssExporter_Util.FileEdit
Style = xgenAssExporter_StyleSheet

# GLOBAL VARIABLES
__PATH__FILE__ = __file__.replace("\\", "/")
__PATH__SOURCE__ = os.path.split(__PATH__FILE__)[0] + "/source"

class mainWindow(QMainWindow):
    
  def __init__(self, parent=None):
      
    super(mainWindow, self).__init__(parent)
    
    # Attributes
    self.mousePosX = QCursor.pos().x()
    self.mousePosY = QCursor.pos().y()

    self.xgenDescriptions = list()
    self.xgenDescriptionTabs = list()

    self.xgenCollectionMultiString = ""
    self.xgenDescriptionsMap = dict()
    self.xgenAssMultiString = ""

    # UI
    self.setWindowTitle("Xgen Arnold Stand-In Exporter")
    
    self.centralQW = QWidget()
    self.centralQVBL = QVBoxLayout(self.centralQW)
    self.centralQVBL.setAlignment(Qt.AlignTop)
    self.setCentralWidget(self.centralQW)
    
    self.titleQLB = QLabel("Xgen Arnold Stand-In Exporter")
    self.titleQLB.setStyleSheet(Style.mainWindow.titleQLB)
    self.titleQHBL = QHBoxLayout()
    self.titleQHBL.addWidget(self.titleQLB)
    
    self.xgenCollectionFilePathQLB = QLabel("Xgen Collection")
    self.xgenCollectionFilePathQLB.setMinimumWidth(130)
    self.xgenCollectionFilePathQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.xgenCollectionFilePathQLE = QLineEdit()
    self.xgenCollectionFilePathQPB = QPushButton()
    self.xgenCollectionFilePathQPB.setIcon(QIcon(__PATH__SOURCE__ + "/file.png"))
    self.xgenCollectionFilePathQHBL = QHBoxLayout()
    self.xgenCollectionFilePathQHBL.addWidget(self.xgenCollectionFilePathQLB)
    self.xgenCollectionFilePathQHBL.addWidget(self.xgenCollectionFilePathQLE)
    self.xgenCollectionFilePathQHBL.addWidget(self.xgenCollectionFilePathQPB)

    self.xgenArnoldStandInPathQLB = QLabel("Xgen Ass")
    self.xgenArnoldStandInPathQLB.setMinimumWidth(130)
    self.xgenArnoldStandInPathQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.xgenArnoldStandInPathQLE = QLineEdit()
    self.xgenArnoldStandInPathQPB = QPushButton()
    self.xgenArnoldStandInPathQPB.setIcon(QIcon(__PATH__SOURCE__ + "/file.png"))
    self.xgenArnoldStandInPathQHBL = QHBoxLayout()
    self.xgenArnoldStandInPathQHBL.addWidget(self.xgenArnoldStandInPathQLB)
    self.xgenArnoldStandInPathQHBL.addWidget(self.xgenArnoldStandInPathQLE)
    self.xgenArnoldStandInPathQHBL.addWidget(self.xgenArnoldStandInPathQPB)
    
    self.compileXgenCollectionQPB = QPushButton("Compile Xgen Collection File")
    self.compileXgenCollectionQPB.setMinimumWidth(500)
    self.compileXgenCollectionQHBL = QHBoxLayout()
    self.compileXgenCollectionQHBL.setAlignment(Qt.AlignCenter)
    self.compileXgenCollectionQHBL.addWidget(self.compileXgenCollectionQPB)
    
    self.xgenCollectionFolderPathQLB = QLabel("Xgen Collection Directory")
    self.xgenCollectionFolderPathQLB.setMinimumWidth(130)
    self.xgenCollectionFolderPathQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.xgenCollectionFolderPathQLE = QLineEdit()
    self.xgenCollectionFolderPathQPB = QPushButton("Set")
    self.xgenCollectionFolderPathQHBL = QHBoxLayout()
    self.xgenCollectionFolderPathQHBL.addWidget(self.xgenCollectionFolderPathQLB)
    self.xgenCollectionFolderPathQHBL.addWidget(self.xgenCollectionFolderPathQLE)
    # self.xgenCollectionFolderPathQHBL.addWidget(self.xgenCollectionFolderPathQPB)

    self.xgenPatchFilePathQLB = QLabel("Xgen Patch File")
    self.xgenPatchFilePathQLB.setMinimumWidth(130)
    self.xgenPatchFilePathQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.xgenPatchFilePathQLE = QLineEdit()
    self.xgenPatchFilePathQPB = QPushButton("Set")
    self.xgenPatchFilePathQHBL = QHBoxLayout()
    self.xgenPatchFilePathQHBL.addWidget(self.xgenPatchFilePathQLB)
    self.xgenPatchFilePathQHBL.addWidget(self.xgenPatchFilePathQLE)
    # self.xgenPatchFilePathQHBL.addWidget(self.xgenPatchFilePathQPB)
    
    self.projectPathQLB = QLabel("Project Folder")
    self.projectPathQLB.setMinimumWidth(130)
    self.projectPathQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.projectPathQLE = QLineEdit()
    self.projectPathQPB = QPushButton("Set")
    self.projectPathQHBL = QHBoxLayout()
    self.projectPathQHBL.addWidget(self.projectPathQLB)
    self.projectPathQHBL.addWidget(self.projectPathQLE)
    # self.projectPathQHBL.addWidget(self.projectPathQPB)

    self.descriptionTabQGB = QGroupBox("Description List")
    self.descriptionTabQgbQVBL = QVBoxLayout(self.descriptionTabQGB)
    self.descriptionTabQgbQVBL.setAlignment(Qt.AlignCenter)

    self.descriptionRootTabQTW = QTabWidget()
    self.descriptionRootTabQTB = self.descriptionRootTabQTW.tabBar()
    self.descriptionRootTabQTB.setUsesScrollButtons(True)
    self.descriptionTabQgbQVBL.addWidget(self.descriptionRootTabQTW)

    self.descriptionDefaultQW = QWidget()
    self.descriptionDefaultQLB = QLabel("Import Xgen Collection File First")
    self.descriptionDefaultQLB.setAlignment(Qt.AlignCenter)
    self.descriptionDefaultQLB.setMaximumHeight(512)
    self.descriptionDefaultQVBL = QVBoxLayout(self.descriptionDefaultQW)
    self.descriptionDefaultQVBL.addWidget(self.descriptionDefaultQLB)
    self.descriptionRootTabQTW.addTab(self.descriptionDefaultQW, "Default")

    self.repathWiresFileQLB = QLabel("Repath WiresFiles")
    self.repathWiresFileQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.repathWiresFileQPB = QPushButton("Execute")
    self.repathWiresFileQPB.setMinimumWidth(128)
    self.repathWiresFileQHBL = QHBoxLayout()
    self.repathWiresFileQHBL.setAlignment(Qt.AlignRight)
    self.repathWiresFileQHBL.addWidget(self.repathWiresFileQLB)
    self.repathWiresFileQHBL.addWidget(self.repathWiresFileQPB)
    self.descriptionTabQgbQVBL.addLayout(self.repathWiresFileQHBL)

    self.descriptionTabQVBL = QVBoxLayout()
    self.descriptionTabQVBL.addWidget(self.descriptionTabQGB)
    
    # Export Options ==============================================
    self.exportOptionsQGB = QGroupBox("Export Options")
    
    self.frameRangeQLB = QLabel("Frame Range")
    self.frameRangeQLB.setMinimumWidth(130)
    self.frameRangeQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.frameStartQLE = QLineEdit("950")
    self.frameStartQLE.setAlignment(Qt.AlignRight)
    self.frameStartQLE.setMaximumWidth(64)
    self.frameEndQLE = QLineEdit("1001")
    self.frameEndQLE.setAlignment(Qt.AlignRight)
    self.frameEndQLE.setMaximumWidth(64)
    self.framePerSecondQLB = QLabel("FPS")
    self.framePerSecondQLB.setMinimumWidth(32)
    self.framePerSecondQLB.setMaximumWidth(32)
    self.framePerSecondQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.framePerSecondQLE = QLineEdit()
    self.framePerSecondQLE.setAlignment(Qt.AlignRight)
    self.framePerSecondQLE.setMaximumWidth(80)
    self.frameRangeEmptyQLB = QLabel()
    self.frameOptionsQHBL = QHBoxLayout()    
    self.frameOptionsQHBL.addWidget(self.frameRangeQLB)
    self.frameOptionsQHBL.addWidget(self.frameStartQLE)
    self.frameOptionsQHBL.addWidget(self.frameEndQLE)
    self.frameOptionsQHBL.addWidget(self.framePerSecondQLB)
    self.frameOptionsQHBL.addWidget(self.framePerSecondQLE)
    self.frameOptionsQHBL.addWidget(self.frameRangeEmptyQLB)
    
    self.motionBlurQLB = QLabel("Motion Blur")
    self.motionBlurQLB.setMinimumWidth(130)
    self.motionBlurQLB.setMaximumWidth(130)
    self.motionBlurQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.motionBlurStartQLE = QLineEdit()
    self.motionBlurStartQLE.setMaximumWidth(64)
    self.motionBlurStartQLE.setAlignment(Qt.AlignRight)
    self.motionBlurEndQLE = QLineEdit()
    self.motionBlurEndQLE.setMaximumWidth(64)
    self.motionBlurEndQLE.setAlignment(Qt.AlignRight)
    self.motionBlurEmptyQLB = QLabel()
    self.motionBlurQHBL = QHBoxLayout()
    self.motionBlurQHBL.setAlignment(Qt.AlignLeft)
    self.motionBlurQHBL.addWidget(self.motionBlurQLB)
    self.motionBlurQHBL.addWidget(self.motionBlurStartQLE)
    self.motionBlurQHBL.addWidget(self.motionBlurEndQLE)
    self.motionBlurQHBL.addWidget(self.motionBlurEmptyQLB)

    self.xgenPatchDeformedQLB = QLabel("Xgen Patch Deformed")
    self.xgenPatchDeformedQLB.setMinimumWidth(130)
    self.xgenPatchDeformedQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.xgenPatchDeformedQLE = QLineEdit()
    self.xgenPatchDeformedQLE.setAlignment(Qt.AlignRight)
    self.xgenPatchDeformedQPB = QPushButton()
    self.xgenPatchDeformedQPB.setIcon(QIcon(__PATH__SOURCE__ + "/file.png"))
    self.xgenPatchDeformedQHBL = QHBoxLayout()
    self.xgenPatchDeformedQHBL.addWidget(self.xgenPatchDeformedQLB)
    self.xgenPatchDeformedQHBL.addWidget(self.xgenPatchDeformedQLE)
    self.xgenPatchDeformedQHBL.addWidget(self.xgenPatchDeformedQPB)
    
    self.exportOptionsQgbQVBL = QVBoxLayout(self.exportOptionsQGB)
    self.exportOptionsQgbQVBL.addLayout(self.frameOptionsQHBL)
    self.exportOptionsQgbQVBL.addLayout(self.motionBlurQHBL)
    self.exportOptionsQgbQVBL.addLayout(self.xgenPatchDeformedQHBL)
    
    self.exportOptionsQHBL = QHBoxLayout()
    self.exportOptionsQHBL.setAlignment(Qt.AlignLeft)
    self.exportOptionsQHBL.addWidget(self.exportOptionsQGB)
    # Export Options ==============================================
    
    self.exportPathQLB = QLabel("Export Path")
    self.exportPathQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.exportPathQLE = QLineEdit()
    self.exportPathQPB = QPushButton()
    self.exportPathQPB.setIcon(QIcon(__PATH__SOURCE__ + "/file.png"))
    self.exportPathQHBL = QHBoxLayout()
    self.exportPathQHBL.addWidget(self.exportPathQLB)
    self.exportPathQHBL.addWidget(self.exportPathQLE)
    self.exportPathQHBL.addWidget(self.exportPathQPB)
    
    self.exportButtonQPB = QPushButton("Export Xgen Arnold Stand-In")
    self.closeButtonQPB = QPushButton("Cancel")
    self.exportButtonQHBL = QHBoxLayout()
    self.exportButtonQHBL.setAlignment(Qt.AlignRight)
    self.exportButtonQHBL.addWidget(self.exportButtonQPB)
    self.exportButtonQHBL.addWidget(self.closeButtonQPB)
    
    self.authorEmailQLB = QLabel("CodingPanda8820@gmail.com")
    self.authorEmailQHBL = QHBoxLayout()
    self.authorEmailQHBL.setAlignment(Qt.AlignRight)
    self.authorEmailQHBL.addWidget(self.authorEmailQLB)
    
    self.centralQVBL.addLayout(self.titleQHBL)
    self.centralQVBL.addLayout(self.xgenCollectionFilePathQHBL)
    self.centralQVBL.addLayout(self.xgenArnoldStandInPathQHBL)
    self.centralQVBL.addLayout(self.compileXgenCollectionQHBL)
    self.centralQVBL.addLayout(self.xgenCollectionFolderPathQHBL)
    self.centralQVBL.addLayout(self.xgenPatchFilePathQHBL)
    self.centralQVBL.addLayout(self.projectPathQHBL)
    self.centralQVBL.addLayout(self.descriptionTabQVBL)
    self.centralQVBL.addLayout(self.exportOptionsQHBL)
    self.centralQVBL.addLayout(self.exportPathQHBL)
    self.centralQVBL.addLayout(self.exportButtonQHBL)
    self.centralQVBL.addLayout(self.authorEmailQHBL)

    self.resize(512,self.sizeHint().height())

    self.__connect__()

  def __connect__(self):
    self.xgenCollectionFilePathQPB.clicked.connect(self.__conenct__xgenCollectionFilePathQPB)
    self.xgenArnoldStandInPathQPB.clicked.connect(self.__connect__xgenArnoldStandInPathQPB)
    self.compileXgenCollectionQPB.clicked.connect(self.__connect__compileXgenCollectionQPB)
    self.xgenCollectionFolderPathQPB.clicked.connect(self.__connect__xgenCollectionFolderPathQPB)
    self.xgenPatchFilePathQPB.clicked.connect(self.__connect__xgenPatchFilePathQPB)
    self.projectPathQPB.clicked.connect(self.__connect__projectPathQPB)
    self.xgenPatchDeformedQPB.clicked.connect(self.__connect__xgenPatchDeformedQPB)
    self.repathWiresFileQPB.clicked.connect(self.__connect__repathWiresFileQPB)
    self.exportPathQPB.clicked.connect(self.__connect__exportPathQPB)
    self.exportButtonQPB.clicked.connect(self.__connect__exportButtonQPB)
    self.closeButtonQPB.clicked.connect(self.__connect__closeButtonQPB)

  def __conenct__xgenCollectionFilePathQPB(self):
    self.OpenFileQFD(self.xgenCollectionFilePathQLE, "Import Xgen Collection File", "Collection (*.xgen)")

  def __connect__xgenArnoldStandInPathQPB(self):
    self.OpenFileQFD(self.xgenArnoldStandInPathQLE, "Import Xgen Arnold Stand-In File", "*.ass")

  def __connect__compileXgenCollectionQPB(self):
    self.CompileXgenArnoldStandInFile()
    self.CompileXgenCollectionFile()

  def __connect__xgenCollectionFolderPathQPB(self):
    self.OpenDirectoryQFD(self.xgenCollectionFolderPathQLE, "Select Collection Directory")

  def __connect__xgenPatchFilePathQPB(self):
    self.OpenFileQFD(self.xgenPatchFilePathQLE, "Import XgenPatch Alembic File", "alembic (*.abc)")

  def __connect__projectPathQPB(self):
    self.OpenDirectoryQFD(self.projectPathQPB, "Select Maya Project Path")

  def __connect__repathWiresFileQPB(self):

    instDialog = RepathWiresFileQDG(self.xgenDescriptionTabs, self)
    instDialog.show()

  def __connect__xgenPatchDeformedQPB(self):
    self.OpenFileQFD(self.xgenPatchDeformedQLE, "Import XgenPatch Alembic Animated File", "alembic (*.abc)")

  def __connect__exportPathQPB(self):
    self.SaveFileQFD(self.exportPathQLE, "Set Export File Path", "Ass (*.ass)")

  def __connect__exportButtonQPB(self):
    self.exportCacheData()

  def __connect__closeButtonQPB(self):
    self.close()
    del(self)

  def keyPressEvent(self, keyEvent):
    if keyEvent.key() == Qt.Key_Escape:
      self.closeButtonQPB.click()

  def OpenFileQFD(self, pLineEdit, pTitle, pFilter):

    filePath = QFileDialog.getOpenFileName(parent=self, caption=pTitle, filter=pFilter)

    if not filePath or not filePath[0]:
      return False

    pLineEdit.setText(filePath[0])

    return filePath[0]

  def OpenDirectoryQFD(self, pLineEdit, pTitle):

    directoryPath = QFileDialog.getExistingDirectory(parent=self, caption=pTitle)

    if not directoryPath:
      return False

    pLineEdit.setText(directoryPath)

    return directoryPath

  def SaveFileQFD(self, pLineEdit, pTitle, pFilter):

    filePath = QFileDialog.getSaveFileName(parent=self, caption=pTitle, filter=pFilter)

    if not filePath or not filePath[0]:
      return False

    pLineEdit.setText(filePath[0])

    return filePath[0]

  def CompileXgenCollectionFile(self):

    self.xgenCollectionMultiString = FileEdit.ConvertFileToMultiString(self.xgenCollectionFilePathQLE.text())

    xgcDataPath = XgenFileEdit.GetAttribute(self.xgenCollectionMultiString, 'Palette', 'xgDataPath');
    xgcProjectPath = XgenFileEdit.GetAttribute(self.xgenCollectionMultiString, 'Palette', 'xgProjectPath');

    self.xgenCollectionFolderPathQLE.setText(xgcDataPath[1])
    self.projectPathQLE.setText(xgcProjectPath[1])

    xgDescriptions = XgenFileEdit.GetDescriptions(self.xgenCollectionMultiString)

    if not xgDescriptions:
      return False

    self.descriptionRootTabQTW.clear()
    for xgDescription in xgDescriptions:
      self.CompileXgenDescription(xgDescription)  

  def CompileXgenDescription(self, multiString):
    descriptionName = XgenFileEdit.GetAttribute(multiString, 'Description', 'name')

    AnimWiresFXModuleData = XgenFileEdit.GetModule(multiString, 'AnimWiresFXModule')

    if not AnimWiresFXModuleData:
      return False

    AnimWiresFXModuleMultiString = AnimWiresFXModuleData[1]

    descriptionTabQW = self.CreateXgenDescriptionQTW(descriptionName[1], self.descriptionRootTabQTW)

    animWires_mask = XgenFileEdit.GetAttribute(AnimWiresFXModuleMultiString, 'AnimWiresFXModule', 'mask')
    descriptionTabQW.maskQLE.setText(animWires_mask[1])

    animWires_magnitude = XgenFileEdit.GetAttribute(AnimWiresFXModuleMultiString, 'AnimWiresFXModule', 'magnitude')
    descriptionTabQW.magnitudeQLE.setText(animWires_magnitude[1])

    animWires_magnitudeScale = XgenFileEdit.GetAttribute(AnimWiresFXModuleMultiString, 'AnimWiresFXModule', 'magnitudeScale')
    descriptionTabQW.magnitudeScaleQLE.setText(animWires_magnitudeScale[1])

    animWires_wiresFile = XgenFileEdit.GetAttribute(AnimWiresFXModuleMultiString, 'AnimWiresFXModule', 'wiresFile')
    descriptionTabQW.wiresFileQLE.setText(animWires_wiresFile[1])

    animWires_refWiresFrame = XgenFileEdit.GetAttribute(AnimWiresFXModuleMultiString, 'AnimWiresFXModule', 'refWiresFrame')
    descriptionTabQW.refWiresFrameQLE.setText(animWires_refWiresFrame[1])

    animWires_interpolation = XgenFileEdit.GetAttribute(AnimWiresFXModuleMultiString, 'AnimWiresFXModule', 'interpolation')
    descriptionTabQW.interpolationQLE.setText(animWires_interpolation[1])

    self.xgenDescriptionsMap[descriptionName] = {"first":multiString, "second":descriptionTabQW}

  def CreateXgenDescriptionQTW(self, name, pRootTabQTW):
    descriptionTabQW = DescriptionTabQW(name, pRootTabQTW)
    self.xgenDescriptionTabs.append(descriptionTabQW)
    self.xgenDescriptions.append(name)

    return descriptionTabQW

  def CompileXgenArnoldStandInFile(self):
    xgAssFile = self.xgenArnoldStandInPathQLE.text()
    self.xgenAssMultiString = FileEdit.ConvertFileToMultiString(xgAssFile)
    xgProcs = AssFileEdit.GetXgenProcedurals(self.xgenAssMultiString)

    if not xgProcs:
      return False

    xgDescs = list()
    for xgProc in xgProcs:
      xgDesc = AssFileEdit.CompileXgenProcedural(xgProc, 'name')[1].split("/")[2]
      xgDescs.append(xgDesc)

    xgPatch = AssFileEdit.CompileXgenProcedural(xgProcs[0], 'geom')
    self.xgenPatchFilePathQLE.setText(xgPatch[1])
    
    xgFPS = AssFileEdit.CompileXgenProcedural(xgProcs[0], 'fps')
    self.framePerSecondQLE.setText(xgFPS[1])

    xgFrameStart = AssFileEdit.CompileXgenProcedural(xgProcs[0],'motion_start')
    self.motionBlurStartQLE.setText(xgFrameStart[1])

    xgFrameEnd = AssFileEdit.CompileXgenProcedural(xgProcs[0], 'motion_end')
    self.motionBlurEndQLE.setText(xgFrameEnd[1])

    return xgDescs

  def exportCacheData(self):

    exportDirectoryPath = os.path.split(self.exportPathQLE.text())[0]

    # get xgen collection path
    source_xgenCollection = AssFileEdit.CompileXgenProcedural(self.xgenAssMultiString, 'file')
    target_xgenCollection = self.exportXgenCollections(exportDirectoryPath)

    # copy xgen patch deformed
    source_xgenPatchDeformed = self.xgenPatchDeformedQLE.text()
    target_xgenPatchDeformed = os.path.join(exportDirectoryPath, os.path.split(source_xgenPatchDeformed)[1]).replace("\\", "/")
    copyfile(source_xgenPatchDeformed, target_xgenPatchDeformed)  

    startFrame = int(self.frameStartQLE.text())
    endFrame = int(self.frameEndQLE.text())

    for currentFrame in range(startFrame, endFrame + 1):
      self.exportXgenArnoldStandIn(target_xgenCollection, target_xgenPatchDeformed, currentFrame)

  def exportXgenCollections(self, exportDirectoryPath):

    update_xgenCollectionMultiString = self.xgenCollectionMultiString
    for descriptionName in self.xgenDescriptionsMap.keys():
      descriptionMultiString = self.exportXgenCollection(descriptionName)
      regex_descriptionMultiString = descriptionMultiString[0]
      update_descriptionMultiString = descriptionMultiString[1]

      update_xgenCollectionMultiString = update_xgenCollectionMultiString.replace(regex_descriptionMultiString,update_descriptionMultiString)

    exportFileName = os.path.split(self.xgenCollectionFilePathQLE.text())[1]

    exportFilePath = os.path.join(exportDirectoryPath, exportFileName).replace("\\", "/")

    with open(exportFilePath,"w") as f:
      f.write(update_xgenCollectionMultiString)

    return exportFilePath

  def exportXgenCollection(self, descriptionName):

    descriptionMultiString = self.xgenDescriptionsMap[descriptionName]["first"]
    AnimWiresFXModule = XgenFileEdit.GetModule(descriptionMultiString, 'AnimWiresFXModule')    

    default_mask = XgenFileEdit.GetAttribute(AnimWiresFXModule[1], 'AnimWiresFXModule', 'mask')
    default_magnitude = XgenFileEdit.GetAttribute(AnimWiresFXModule[1], 'AnimWiresFXModule', 'magnitude')
    default_magnitudeScale = XgenFileEdit.GetAttribute(AnimWiresFXModule[1], 'AnimWiresFXModule', 'magnitudeScale')
    default_wiresFile = XgenFileEdit.GetAttribute(AnimWiresFXModule[1], 'AnimWiresFXModule', 'wiresFile')
    default_refWiresFrame = XgenFileEdit.GetAttribute(AnimWiresFXModule[1], 'AnimWiresFXModule', 'refWiresFrame')
    default_interpolation = XgenFileEdit.GetAttribute(AnimWiresFXModule[1], 'AnimWiresFXModule', 'interpolation')

    descriptionTabQW = self.xgenDescriptionsMap[descriptionName]["second"]

    update_mask = default_mask[2].replace(default_mask[1], descriptionTabQW.maskQLE.text())
    update_magnitude = default_magnitude[2].replace(default_magnitude[1], descriptionTabQW.magnitudeQLE.text())
    update_magnitudeScale = default_magnitudeScale[2].replace(default_magnitudeScale[1], descriptionTabQW.magnitudeScaleQLE.text())
    update_wiresFile = default_wiresFile[2].replace(default_wiresFile[1], descriptionTabQW.wiresFileQLE.text())
    update_refWiresFrame = default_refWiresFrame[2].replace(default_refWiresFrame[1], descriptionTabQW.refWiresFrameQLE.text())
    update_interpolation = default_interpolation[2].replace(default_interpolation[1], descriptionTabQW.interpolationQLE.text())

    update_AnimWiresFXModule = AnimWiresFXModule[1].replace(default_mask[2].replace("\n",""), update_mask)
    update_AnimWiresFXModule = update_AnimWiresFXModule.replace(default_magnitude[2].replace("\n",""), update_magnitude)
    update_AnimWiresFXModule = update_AnimWiresFXModule.replace(default_magnitudeScale[2].replace("\n",""), update_magnitudeScale)
    update_AnimWiresFXModule = update_AnimWiresFXModule.replace(default_wiresFile[2].replace("\n",""), update_wiresFile)
    update_AnimWiresFXModule = update_AnimWiresFXModule.replace(default_refWiresFrame[2].replace("\n",""), update_refWiresFrame)
    update_AnimWiresFXModule = update_AnimWiresFXModule.replace(default_interpolation[2].replace("\n",""), update_interpolation)

    update_descriptionMultiString = descriptionMultiString.replace(AnimWiresFXModule[1], update_AnimWiresFXModule)

    return (descriptionMultiString, update_descriptionMultiString)

  def exportXgenArnoldStandIn(self,replace_xgenCollection, replace_xgenPatchDeformed, frame=1):

    default_xgenCollection = AssFileEdit.CompileXgenProcedural(self.xgenAssMultiString, 'file')
    default_xgenPatchDeformed = AssFileEdit.CompileXgenProcedural(self.xgenAssMultiString, 'geom')
    default_frame = AssFileEdit.CompileXgenProcedural(self.xgenAssMultiString, 'frame')
    default_framePerSecond = AssFileEdit.CompileXgenProcedural(self.xgenAssMultiString, 'fps')

    update_xgenCollection = default_xgenCollection[2].replace(default_xgenCollection[1], replace_xgenCollection).replace("\\", "/")
    update_xgenPatchDeformed = default_xgenPatchDeformed[2].replace(default_xgenPatchDeformed[1], replace_xgenPatchDeformed).replace("\\", "/")
    update_frame = default_frame[2].replace(default_frame[1], str(frame))
    update_framePerSecond = default_framePerSecond[2].replace(default_framePerSecond[1], self.framePerSecondQLE.text())

    multiString = self.xgenAssMultiString.replace(default_xgenCollection[2], update_xgenCollection)
    multiString = multiString.replace(default_xgenPatchDeformed[2], update_xgenPatchDeformed)
    multiString = multiString.replace(default_frame[2], update_frame)
    multiString = multiString.replace(default_framePerSecond[2], update_framePerSecond)

    exportFilePath = self.exportPathQLE.text().split('.')[0] + '.{:04d}.ass'.format(frame)

    with open(exportFilePath, "w") as ass:
      ass.write(multiString)

    return exportFilePath

class DescriptionTabQW(QWidget):

  def __init__(self, name, pDescriptionRootTabQTW, parent=None):

    super(DescriptionTabQW, self).__init__(parent)

    self.parent = parent

    self.animWiresFXModuleQLB = QLabel("AnimWiresFXModule")
    self.animWiresFXModuleQHBL = QHBoxLayout()
    self.animWiresFXModuleQHBL.setAlignment(Qt.AlignLeft)
    self.animWiresFXModuleQHBL.addWidget(self.animWiresFXModuleQLB)

    self.maskQLB = QLabel("Mask")
    self.maskQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.maskQLB.setMinimumWidth(130)
    self.maskQLE = QLineEdit()
    self.maskQHBL = QHBoxLayout()
    self.maskQHBL.addWidget(self.maskQLB)
    self.maskQHBL.addWidget(self.maskQLE)

    self.magnitudeQLB = QLabel("Magnitude")
    self.magnitudeQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.magnitudeQLB.setMinimumWidth(130)
    self.magnitudeQLE = QLineEdit()
    self.magnitudeQHBL = QHBoxLayout()
    self.magnitudeQHBL.addWidget(self.magnitudeQLB)
    self.magnitudeQHBL.addWidget(self.magnitudeQLE)

    self.magnitudeScaleQLB = QLabel("Magnitude Scale")
    self.magnitudeScaleQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.magnitudeScaleQLB.setMinimumWidth(130)
    self.magnitudeScaleQLE = QLineEdit()
    self.magnitudeScaleQHBL = QHBoxLayout()
    self.magnitudeScaleQHBL.addWidget(self.magnitudeScaleQLB)
    self.magnitudeScaleQHBL.addWidget(self.magnitudeScaleQLE)
    
    self.wiresFileQLB = QLabel("wiresFile")
    self.wiresFileQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.wiresFileQLB.setMinimumWidth(130)
    self.wiresFileQLE = QLineEdit()
    self.wiresFileQPB = QPushButton()
    self.wiresFileQPB.setIcon(QIcon(__PATH__SOURCE__ + "/file.png"))
    self.wiresFileQHBL = QHBoxLayout()
    self.wiresFileQHBL.addWidget(self.wiresFileQLB)
    self.wiresFileQHBL.addWidget(self.wiresFileQLE)
    self.wiresFileQHBL.addWidget(self.wiresFileQPB)

    self.refWiresFrameQLB = QLabel("Ref Wires Frame")
    self.refWiresFrameQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.refWiresFrameQLB.setMinimumWidth(130)
    self.refWiresFrameQLE = QLineEdit()
    self.refWiresFrameQHBL = QHBoxLayout()
    self.refWiresFrameQHBL.addWidget(self.refWiresFrameQLB)
    self.refWiresFrameQHBL.addWidget(self.refWiresFrameQLE)

    self.interpolationQLB = QLabel("Interpolation")
    self.interpolationQLB.setAlignment(Qt.AlignRight | Qt.AlignCenter)
    self.interpolationQLB.setMinimumWidth(130)
    self.interpolationQLE = QLineEdit()
    self.interpolationQHBL = QHBoxLayout()
    self.interpolationQHBL.addWidget(self.interpolationQLB)
    self.interpolationQHBL.addWidget(self.interpolationQLE)

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.setAlignment(Qt.AlignTop)
    self.mainLayout.addLayout(self.animWiresFXModuleQHBL)
    self.mainLayout.addLayout(self.maskQHBL)
    self.mainLayout.addLayout(self.magnitudeQHBL)
    self.mainLayout.addLayout(self.magnitudeScaleQHBL)
    self.mainLayout.addLayout(self.wiresFileQHBL)
    self.mainLayout.addLayout(self.refWiresFrameQHBL)
    self.mainLayout.addLayout(self.interpolationQHBL)

    pDescriptionRootTabQTW.addTab(self, name)

    self.__connect__()

  def __connect__(self):

    self.wiresFileQPB.clicked.connect(self.__connect__wiresFileQPB)

  def __connect__wiresFileQPB(self):

    self.OpenFileQFD(self.wiresFileQLE, "Import AnimrWire Guide Simulated Alembic Cache", "Alembic (*.abc)");

  def OpenFileQFD(self, pLineEdit, pTitle, pFilter):

    filePath = QFileDialog.getOpenFileName(parent=self, caption=pTitle, filter=pFilter)

    if not filePath or not filePath[0]:
      return False

    pLineEdit.setText(filePath[0])

    return filePath[0]

  def OpenDirectoryQFD(self, pLineEdit, pTitle):

    directoryPath = QFileDialog.getExistingDirectory(parent=self, caption=pTitle)

    if not directoryPath:
      return False

    pLineEdit.setText(directoryPath)

    return directoryPath

class RepathWiresFileQDG(QDialog):

  def __init__(self, xgenDescriptionTabs, parent=None):

    super(RepathWiresFileQDG, self).__init__(parent)

    # Attributes
    self.xgenDescriptionTabs = xgenDescriptionTabs

    self.regexQLB = QLabel("Regex")
    self.regexQLE = QLineEdit()
    self.regexQPB = QPushButton()
    self.regexQPB.setIcon(QIcon(__PATH__SOURCE__ + "/directory.png"))
    self.regexQHBL = QHBoxLayout()
    self.regexQHBL.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
    self.regexQHBL.addWidget(self.regexQLB)
    self.regexQHBL.addWidget(self.regexQLE)
    self.regexQHBL.addWidget(self.regexQPB)

    self.replaceQLB = QLabel("Replace")
    self.replaceQLE = QLineEdit()
    self.replaceQPB = QPushButton()
    self.replaceQPB.setIcon(QIcon(__PATH__SOURCE__ + "/directory.png"))
    self.replaceQHBL = QHBoxLayout()
    self.replaceQHBL.setAlignment(Qt.AlignLeft | Qt.AlignCenter)
    self.replaceQHBL.addWidget(self.replaceQLB)
    self.replaceQHBL.addWidget(self.replaceQLE)
    self.replaceQHBL.addWidget(self.replaceQPB)

    self.enterQPB = QPushButton("Enter")
    self.cancelQPB = QPushButton("Cancel")
    self.buttonsQHBL = QHBoxLayout()
    self.buttonsQHBL.addWidget(self.enterQPB)
    self.buttonsQHBL.addWidget(self.cancelQPB)

    self.mainLayout = QVBoxLayout(self)
    self.mainLayout.addLayout(self.regexQHBL)
    self.mainLayout.addLayout(self.replaceQHBL)
    self.mainLayout.addLayout(self.buttonsQHBL)

    self.resize(512, self.size().height())

    self.__connect__()

  def __connect__(self):

    self.regexQPB.clicked.connect(self.__connect__regexQPB)
    self.replaceQPB.clicked.connect(self.__connect__replaceQPB)
    self.enterQPB.clicked.connect(self.__connect__enterQPB)
    self.cancelQPB.clicked.connect(self.__connect__cancelQPB)

  def __connect__regexQPB(self):

    self.OpenDirectoryQFD(self.regexQLE, "Set Directory Regex Path")

  def __connect__replaceQPB(self):

    self.OpenDirectoryQFD(self.replaceQLE, "Set Directory Replace Path")

  def __connect__enterQPB(self):

    for xgenDescriptionTab in self.xgenDescriptionTabs:
      compiled = xgenDescriptionTab.wiresFileQLE.text().replace(self.regexQLE.text().replace("\\","/"), self.replaceQLE.text().replace("\\","/"))
      xgenDescriptionTab.wiresFileQLE.setText(compiled)

    self.cancelQPB.click()

  def __connect__cancelQPB(self):

    self.close()
    del(self)

  def keyPressEvent(self, keyEvent):
    if keyEvent.key() == Qt.Key_Escape:
      self.cancelQPB.click()
    elif keyEvent.key() == Qt.Key_Enter:
      self.enterQPb.click()

  def OpenDirectoryQFD(self, pLineEdit, pTitle):

    directoryPath = QFileDialog.getExistingDirectory(parent=self, caption=pTitle)

    if not directoryPath:
      return False

    pLineEdit.setText(directoryPath)

    return directoryPath


















