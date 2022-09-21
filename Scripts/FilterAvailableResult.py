import os
import pandas as pd
import shutil
basicPath = r"/home/ljj/test"



jcloudsPMDReportPath = basicPath + r'/Reports/PMD/jclouds'
jcloudsPMDResultPath = basicPath+ r'/Results/PMD/jclouds'
saveFilterResultsJcloudsPMDPath = basicPath + "/FilterResults/PMD/jclouds/Results"
saveFilterReportsJcloudsPMDPath = basicPath + "/FilterResults/PMD/jclouds/Reports"
jcloudsSBReportPath = basicPath + r'/Reports/Spotbugs/jclouds'
jcloudsSBResultPath = basicPath + r'/Results/Spotbugs/jclouds'
saveFilterResultsJcloudsSBPath = basicPath + "/FilterResults/Spotbugs/jclouds/Results"
saveFilterReportsJcloudsSBPath = basicPath + "/FilterResults/Spotbugs/jclouds/Reports"

kafkaPMDReportPath = basicPath + r'/Reports/PMD/kafka'
kafkaPMDResultPath = basicPath+ r'/Results/PMD/kafka'
saveFilterResultsKafkaPMDPath = basicPath + "/FilterResults/PMD/kafka/Results"
saveFilterReportsKafkaPMDPath = basicPath + "/FilterResults/PMD/kafka/Reports"
kafkaSBReportPath = basicPath + r'/Reports/Spotbugs/kafka/SpotBugslog'
kafkaSBResultPath = basicPath + r'/Results/Spotbugs/kafka/New_approach'
saveFilterResultsKafkaSBPath = basicPath + "/FilterResults/Spotbugs/kafka/Results"
saveFilterReportsKafkaSBPath = basicPath + "/FilterResults/Spotbugs/kafka/Reports"

resultPath = kafkaPMDResultPath
reportPath = kafkaPMDReportPath
saveFilterResultsPath = saveFilterResultsKafkaPMDPath
saveFilterReportssPath = saveFilterReportsKafkaPMDPath




files = os.listdir(resultPath)
s=[]
count=0
fileList = []
warningCount = 0
for file in files:
    csv_data= pd.read_csv(resultPath+'/'+file)
    count+=1
    if not csv_data.empty:  
        print(file)
        fileList.append(file)
if not os.path.exists(saveFilterResultsPath):
    os.mkdir(saveFilterResultsPath)
for file in fileList:
    shutil.copyfile(resultPath+'/'+file,saveFilterResultsPath + '/' +file)
  
if not os.path.exists(saveFilterReportssPath):
    os.mkdir(saveFilterReportssPath)
        
logFiles = os.listdir(saveFilterReportssPath)
commitLogList = []
for file in logFiles:
    commitLogList.append(file)
for file in fileList:
    commitNames = file.split("_")
    commitName1 = commitNames[0][0:7]+'.xml'
    commitName2 = commitNames[1][0:7]+'.xml'
    if commitName1 not in commitLogList: 
        shutil.copyfile(reportPath + '/'+commitName1,saveFilterReportssPath+'/'+commitName1)
        commitLogList.append(commitName1)
    if commitName2 not in commitLogList: 
        shutil.copyfile(reportPath + '/'+commitName2,saveFilterReportssPath+'/'+commitName2)
        commitLogList.append(commitName2)