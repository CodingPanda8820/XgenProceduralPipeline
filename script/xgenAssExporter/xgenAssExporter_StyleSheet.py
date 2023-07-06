import os, sys

# GLOBAL VARIABLES
__PATH__FILE__ = __file__.replace("\\", "/")
__PATH__SOURCE__ = os.path.split(__PATH__FILE__)[0] + "/source"

class mainWindow:

  titleQLB = """
  QLabel{
    font: bold 28px;
  }
  """