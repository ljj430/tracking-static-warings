#import ToolsRunner.PMDRunner as pRunner


##1 open commit list  violationNumberDic
##2 random sample 1 commit
##3 open commit file and count the number
##4 sample number = sample number - number
##5 save the commit.
import os
import sys
import pandas as pd
from random import sample
###314 violations

def sampleCommits(sampleSize,commitList):
    commitListAfterSample = sample(commitList, sampleSize)
    return commitListAfterSample

def mapViolationCountToEachCommit(saveResultPath):
    violationNumberDic = {}
    files = os.listdir(saveResultPath)
    for file in files:
        csv_data = pd.read_csv(saveResultPath + '/' + file)
        violationCount = len(csv_data)
        violationNumberDic[file[0:15]] = violationCount
    return violationNumberDic


###314 violations
def commitListGenerater(saveResultPath, saveCommitListPath, sample_num, project_name):
    violationCountDic = mapViolationCountToEachCommit(saveResultPath)
    commitList = []
    ###start to sample
    while(sample_num>0):
        commits = sample(list(violationCountDic.keys()), 1)
        for commit in commits:
            if violationCountDic[commit] == 0:
                continue
            else:
                sample_num -= violationCountDic[commit]
                print(f"selected commit:{commit}\tthe rest of sample num is {sample_num}")
                violationCountDic.pop(commit, None)
                commitList.append(commit)

    ###save to commitList
    saveFile = saveCommitListPath + '/' + project_name + '.txt'
    f = open(saveFile, 'w')
    for commit in commitList:
        if commit == commitList[-1]:
            f.write(commit)
        else:
            f.write(commit + '\n')
    f.close()


if __name__ == "__main__":
    #
    basicPath = "/home/ljj/test/NewResults/"
    jcloudsSpotbugsPath = basicPath + "Spotbugs/jclouds/Results/GoneUnmatchedViolations"
    jcloudsPMDPath = basicPath + "PMD/jclouds/Results/GoneUnmatchedViolations"
    kafkaSpotbugsPath = basicPath + "Spotbugs/kafka/Results/GoneUnmatchedViolations"
    guavaPMDPath = "D:\ThesisData\OriginalResults\PMD\guava\gone"
    guavaSpotbugsPath = "D:\ThesisData\OriginalResults\Spotbugs\guava\gone"
    saveResultPath = guavaPMDPath

    ###for test
    #violationCountDic = mapViolationCountToEachCommit(saveResultPathOnLinux)
    #print(violationCountDic)
    
    ###excute
    sample_num = 289
    project_name = 'guava_Spotbugs'
    saveCommitListPath = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList'
    commitListGenerater(saveResultPath,saveCommitListPath,sample_num,project_name)

