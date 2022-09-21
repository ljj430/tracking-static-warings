import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np

##1. read file

def plotFigure(dict):
    labels = []
    data = []
    for key,value in dict.items():
        print(key,value)
        labels.append(key)
##2. count line
        files = os.listdir(value)
        fileCount = 0
        violationCount = 0
        violationCountEachFile=[]
        for file in files:
            csv_data = pd.read_csv(value+ '/' + file)
            if len(csv_data) != 0:
                fileCount += 1
            print("{}'s file name {} has {}".format(key,file,len(csv_data)))
            violationCount += len(csv_data)
            #if len(csv_data) < 100 and len(csv_data) >= 50:
                #print('Abnormal data:',key,file,len(csv_data))
            violationCountEachFile.append(len(csv_data))
        data.append(violationCountEachFile)
        print(key,"file_count:",fileCount)
        print(key,"unmatched_violation_count:",violationCount)
    fig = plt.figure()
    ax = plt.subplot()
    print(labels)
    ax.boxplot(data,labels = labels)
    plt.ylim(0,10)
    plt.show()




##3. plot
#fig = plt.figure()  # 创建画布
#ax = plt.subplot()  # 创建作图区域
# 蓝色矩形的红线：50%分位点是4.5,上边沿：25%分位点是2.25,下边沿：75%分位点是6.75
#ax.boxplot([range(5), range(10), range(20)])
#plt.show()

if __name__ == "__main__":
    jcloudsSpotbugsPath = "/Users/lijunjie/Desktop/Master/Thesis/Manual analysis/PMDjclouds/Results/"
    jcloudsPMDPath = "/Users/lijunjie/Desktop/Master/Thesis/Task/Week9/5 commits/results/"
    kafkaSpotbugsPath = ""
    kafkaPMDPath = ""
    #
    basicPath = "/home/ljj/test/NewResults/"
    jcloudsSpotbugsPath = basicPath + "Spotbugs/jclouds/Results/GoneUnmatchedViolations"
    jcloudsPMDPath = basicPath + "PMD/jclouds/Results/GoneUnmatchedViolations"
    kafkaSpotbugsPath = basicPath + "Spotbugs/kafka/Results/GoneUnmatchedViolations"
    kafkaPMDPath = basicPath + "PMD/kafka/ResultsAfterSample/GoneUnmatchedViolations"
    saveResultPathOnLinux = {"jclouds_Spotbugs":jcloudsSpotbugsPath,"jclouds_PMD":jcloudsPMDPath, "kafka_Spotbugs":kafkaSpotbugsPath, "kafka_PMD":kafkaPMDPath}
    plotFigure(saveResultPathOnLinux)