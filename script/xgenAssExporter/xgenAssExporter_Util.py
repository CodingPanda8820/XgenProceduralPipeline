import imp, re
import sys, os

class AssFileEdit:

  @classmethod
  def GetXgenProcedurals(cls, multiString):

    regex = re.compile(r'(?P<xgProc>xgen_procedural\n\{[\s\S]+?\})')
    xgProcedurals = regex.findall(multiString)

    return xgProcedurals

  @classmethod
  def CompileXgenProcedural(cls, multiString, attributeName):

      regex = re.compile(r'[\s\-]{an}[\s]+(?P<{an}>[\S]+)'.format(an=attributeName))
      compiled = regex.search(multiString)

      value = compiled.group(attributeName)
      comment = compiled.group()
      
      return (attributeName, value, comment)

class XgenFileEdit:

  @classmethod
  def GetDescriptions(cls, multiString):

    regex = re.compile(r'(?P<Description>\sDescription[\s\S]+?\nGLRenderer[\s\S]+?endAttrs)\n\n')
    compiled = regex.findall(multiString)

    return compiled

  @classmethod
  def GetModule(cls, multiString, moduleName):

    regex = re.compile(r'(?P<{mn}>{mn}[\s.\S]+?endAttrs)'.format(mn=moduleName))
    compiled = regex.search(multiString)
    try:
      value = compiled.group(moduleName)
      comment = compiled.group()

      return (moduleName, value, comment)
    except:
      return False

  @classmethod
  def GetAttribute(cls, multiString, moduleName, attributeName):

    regex = re.compile(r'{an}[\t]+?(?P<{an}>[\S. ]+)'.format(an=attributeName))
    compiled = regex.search(multiString)

    value = compiled.group(attributeName)
    comment = compiled.group()
    
    return (attributeName, value, comment)

class FileEdit:

  @classmethod
  def ConvertFileToMultiString(cls, filePath):

    multiString = ""
    with open(filePath, "r") as f:
      for line in f.readlines():
        multiString += line

    return multiString



  # @classmethod
  # def GetAttribute(cls, multiString, moduleName, attributeName):

  #   # regex = re.compile(r'{mn}[\s\S]+?{an}[\s]+?(?P<{an}>[\S]+?)\s'.format(mn=moduleName, an=attributeName))
  #   regex = re.compile(r'{an}[\s]+?(?P<{an}>[\S]+?)\s'.format(mn=moduleName, an=attributeName))
  #   compiled = regex.search(multiString)

  #   value = compiled.group(attributeName)
  #   comment = compiled.group()
    
  #   return (attributeName, value, comment)