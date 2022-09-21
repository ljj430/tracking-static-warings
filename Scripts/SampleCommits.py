#import ToolsRunner.PMDRunner as pRunner

import os
import sys
sys.path.append('../')
from Utils import checkout as checkout
import Utils as utils
import XMLreader as xmlreader
from BugInstance import BugInstance
import pandas as pd
from random import sample
###234
def sampleCommits(sampleSize,commitList):
    commitListAfterSample = sample(commitList, sampleSize)
    return commitListAfterSample
def commitListGenerater(saveResultPathOnLinux,saveCommitListPathOnLinux):
    labels = []
    for key,value in saveResultPathOnLinux.items():
        saveFile = saveCommitListPathOnLinux+'/'+key + '.txt'
        print("save:",saveFile)
        commitList = []
        print(key,value)
        labels.append(key)
##2. count line
        files = os.listdir(value)
        for file in files:
            #print(file[0:14])###print filename
            ###test
            commitList.append(file[0:15])
        if key == "kafka_PMD":###should be changed
            commitList = sampleCommits(234,list(commitList))
             #   print()
        print(len(commitList),commitList)


        f = open(saveFile, 'w')
        for commit in commitList:
            if commit == commitList[-1]:
                f.write(commit)
            else:
                f.write(commit + '\n')
        f.close()


if __name__ == "__main__":
    #
    basicPath = "/home/ljj/test/FilterResults1/"
    jcloudsSpotbugsPath = basicPath + "Spotbugs/jclouds/Results/GoneUnmatchedViolations"
    jcloudsPMDPath = basicPath + "PMD/jclouds/Results/GoneUnmatchedViolations"
    kafkaSpotbugsPath = basicPath + "Spotbugs/kafka/Results/GoneUnmatchedViolations"
    kafkaPMDPath = basicPath + "PMD/kafka/Results/GoneUnmatchedViolations"
    saveResultPathOnLinux = {"jclouds_Spotbugs":jcloudsSpotbugsPath,"jclouds_PMD":jcloudsPMDPath, "kafka_Spotbugs":kafkaSpotbugsPath, "kafka_PMD":kafkaPMDPath}
    saveCommitListPathOnLinux = '/home/ljj/test/findbugsanalysis/FixPatternMining/CommitList'
    commitListGenerater(saveResultPathOnLinux,saveCommitListPathOnLinux)

