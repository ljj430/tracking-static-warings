import ToolsRunner.PMDRunner as pRunner
from Utils import checkout as checkout
import os

basicPathOnMac = r"/Users/lijunjie/Desktop/Master"
saveJcloudsSBReportPathOnMac = basicPathOnMac + r"/Reports/Spotbugs/Jclouds"

basicPathOnLinux = r"/home/ljj/test"
saveJcloudsSBReportPathOnLinux = basicPathOnLinux + r"/Reports/Spotbugs/jclouds"

###parameter set
saveReportPath = saveJcloudsSBReportPathOnLinux
###check if report is saved.
for i, j, k in os.walk(saveReportPath):
    reportList = k
print(reportList)
for name in reportList:
    names = name.split('.')
    frontName = names[0]
    laterName = names[1]
    os.rename(saveReportPath+'/'+frontName+"."+laterName,saveReportPath+'/'+frontName[0:7]+"."+laterName)
for i, j, k in os.walk(saveReportPath):
    reportList = k
print(reportList)