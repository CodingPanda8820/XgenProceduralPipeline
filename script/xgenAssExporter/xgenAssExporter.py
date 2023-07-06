import sys, os
import imp

from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt

drive = "D:\\"
rootDirList = ["CodingPanda_Outsourcing", "VIVE", "TDL", "work", "script"]

scriptPath = drive
for rootDir in rootDirList:
    scriptPath = os.path.join(scriptPath, rootDir)
    
if scriptPath not in sys.path:
    sys.path.append(scriptPath)
    
import xgenAssExporter.xgenAssExporter_UI as xgAssExportUI
imp.reload(xgAssExportUI)

mWnd = xgAssExportUI.mainWindow()

app = QApplication.instance()
if "hou" in app.applicationName():
  import hou
  mWnd.setParent(hou.ui.mainQtWindow(), Qt.Widget)

mWnd.show()