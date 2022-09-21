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
###jclouds_Spotbugs:364
###jclouds_PMD:204
###kafka_Spotbugs:164
###kafka_PMD:260

def sampleNewViolation(gonePathDic, newPathDic, saveResultPath, sampleSizeDic):

    goneComDic = {"kafka_PMD": [], "kafka_Spotbugs": [], "jclouds_PMD": [], "jclouds_Spotbugs": []}
    newComDic = {"kafka_PMD": {}, "kafka_Spotbugs": {}, "jclouds_PMD": {}, "jclouds_Spotbugs": {}}

    ###1. get the each path of gone violations and generate 4 lists
    for key,value in gonePathDic.items():
        #print(key,value)
        files = os.listdir(value)
        for file in files:
            if file.startswith('.'):
                continue
            else:
                goneComDic[key].append(file)
    ###2. get the each path of new violations based on the GV and genrerate 4 Dic recorded(1.project_tool, 2.file name 3. new violations number)
    for key, value in newPathDic.items():
        print(key, value)
        ##2. count line
        files = os.listdir(value)
        for file in files:

            tmp = file[0:15] + "_gone_warnings.csv"
            if tmp in goneComDic[key]:

                csv_data = pd.read_csv(value + '/' + file)
                if file[0:15] not in newComDic[key].keys() and len(csv_data)!= 0 and len(csv_data)<1000:
                    newComDic[key][file[0:15]] = 0
                if len(csv_data)!= 0 and len(csv_data)<1000:
                    newComDic[key][file[0:15]]=len(csv_data)
    for key,value in newComDic.items():
        print(key)
        print(value)
        print()

    ###3. sample them using sampleSize  total number - the number of ssmpled new violations
    sampledComDic = {"kafka_PMD": [], "kafka_Spotbugs": [], "jclouds_PMD": [], "jclouds_Spotbugs": []}

    for key,value in sampleSizeDic.items():
        print(key,value)
        sampleSize = sampleSizeDic[key]
        ###start to sample
        while (sampleSize > 0):
            commits = sample(list(newComDic[key].keys()), 1)
            for commit in commits:
                sampleSize -= newComDic[key][commit]
                print("the rest of sample num is {}".format(sampleSize))
                newComDic.pop(commit, None)
                sampledComDic[key].append(commit)
    print(sampledComDic)

    ###4. generate commits list
    for key, value in sampledComDic.items():
        ###save to commitList
        saveFile = saveResultPath + '/' + key+"_NewViolations" + '.txt'
        f = open(saveFile, 'w')
        for commit in sampledComDic[key]:
            f.write(commit + '\n')
        f.close()

def sampleCommits(sampleSize,commitList):
    commitListAfterSample = sample(commitList, sampleSize)
    return commitListAfterSample

def mapViolationCountToEachCommit(saveResultPathOnLinux):
    violationNumberDic = {}
    files = os.listdir(saveResultPathOnLinux)
    for file in files:
        csv_data = pd.read_csv(saveResultPathOnLinux + '/' + file)
        violationCount = len(csv_data)
        violationNumberDic[file[0:15]] = violationCount
    return violationNumberDic


###314 violations
def commitListGenerater(saveResultPathOnLinux,saveCommitListPathOnLinux,sample_num,project_name):
    violationCountDic = mapViolationCountToEachCommit(saveResultPathOnLinux)
    commitList = []
    ###start to sample
    while(sample_num>0):
        commits = sample(list(violationCountDic.keys()), 1)
        for commit in commits:
            sample_num -= violationCountDic[commit]
            print("the rest of sample num is {}".format(sample_num))
            violationCountDic.pop(commit, None)
            commitList.append(commit)

    ###save to commitList
    saveFile = saveCommitListPathOnLinux + '/' + project_name + '.txt'
    f = open(saveFile, 'w')
    for commit in commitList:
        if commit == commitList[-1]:
            f.write(commit)
        else:
            f.write(commit + '\n')
    f.close()


if __name__ == "__main__":

    gonePath = "/Users/lijunjie/Desktop/Master/manual work/labeled results/"
    newPath = "/Users/lijunjie/Desktop/Master/manual work/resultsLJJ/"
    #basicPath = "/home/ljj/test/resultsLJJ/"
    gonejcloudsSpotbugsPath = gonePath + "Spotbugs/jclouds"
    gonejcloudsPMDPath = gonePath + "PMD/jclouds"
    gonekafkaSpotbugsPath = gonePath + "Spotbugs/kafka"
    gonekafkaPMDPath = gonePath + "PMD/kafka"
    gonePathDic = { "kafka_PMD":gonekafkaPMDPath,"kafka_Spotbugs":gonekafkaSpotbugsPath,"jclouds_PMD":gonejcloudsPMDPath,"jclouds_Spotbugs":gonejcloudsSpotbugsPath}
    #getStatisticInfo(saveResultPathOnLinux)


    string = "/NewUnmatchedViolations"
    newjcloudsSpotbugsPath = newPath + "Spotbugs/jclouds"+string
    newjcloudsPMDPath = newPath + "PMD/jclouds"+string
    newkafkaSpotbugsPath = newPath + "Spotbugs/kafka"+string
    newkafkaPMDPath = newPath + "PMD/kafka"+string
    newPathDic = {"kafka_PMD":newkafkaPMDPath,"kafka_Spotbugs":newkafkaSpotbugsPath,"jclouds_PMD":newjcloudsPMDPath,"jclouds_Spotbugs":newjcloudsSpotbugsPath}
    saveResultPath = "/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList"
    sampleSizeDic = {"kafka_PMD":260,"kafka_Spotbugs":115,"jclouds_PMD":204,"jclouds_Spotbugs":146}
    sampleNewViolation(gonePathDic,newPathDic,saveResultPath, sampleSizeDic)

