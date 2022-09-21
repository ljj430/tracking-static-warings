### ToDo:
### 1)Total number of violations and commits
### 2)Total number of false positive and true positive  of violations
### 3)number of commits that only contain false positives
### 4)how many false positives are due to refactoring

# import ToolsRunner.PMDRunner as pRunner



import os
import sys
import pandas as pd
from random import sample

def countNewViolations(newDict,goneDict,goneOrNew):
    totalNewViolations = 0
    tmpDic = { "kafka_PMD":[],"kafka_Spotbugs":[],"jclouds_PMD":[],"jclouds_Spotbugs":[]}
    for key,value in goneDict.items():
        #print(key,value)
        files = os.listdir(value)
        for file in files:
            if file.startswith('.'):
                continue
            else:
                tmpDic[key].append(file)

    for key, value in newDict.items():
        print(key, value)
        ##2. count line
        files = os.listdir(value)
        eachFileNewViolation = 0
        #print("tmpDic:",tmpDic[key])

        for file in files:
            #print("file:",file)
            tmp = file[0:15] + goneOrNew
            #print("tmp:",tmp)
            if tmp in tmpDic[key]:
                csv_data = pd.read_csv(value + '/' + file)
                eachFileNewViolation += len(csv_data)
        print("new violation:",eachFileNewViolation)
        totalNewViolations += eachFileNewViolation
    print("total new violations:", totalNewViolations)

def getStatisticInfo(dict):
    totalCommits = 0
    totalViolations = 0
    totalRefactoring = 0
    totalFalsePositives = 0
    totalCommitsOnlyContainsFalsePositives = 0
    totalTruePositives = 0
    for key, value in dict.items():
        print(key, value)

        ##2. count line
        files = os.listdir(value)
        fileCount = 0   ## total commits
        violationCount = 0  ## total violations
        falsePositiveCount = 0#Total number of false positive and true positive  of violations
        truePositiveCount = 0
        commitsNumberOnlyContainFalsePositive = 0#number of commits that only contain false positives
        violationsWithRefactoringNumber = 0#how many false positives are due to refactoring
        for file in files:
            if file.startswith('.'):
                continue
            #print(file)
            csv_data = pd.read_csv(value + '/' + file)

            if len(csv_data)!= 0 :
                falsePositiveData = csv_data.loc[csv_data['False positive/true positive'] == 'f']
                falsePositiveCount += len(falsePositiveData)

                truePositiveData = csv_data.loc[csv_data['False positive/true positive'] == 't']
                truePositiveCount += len(truePositiveData)



                for index,violation in falsePositiveData.iterrows():
                    #print(violation)
                    reasons = violation["Reasons"]
                    #print(reasons)
                    if reasons.split(':')[0] == '(refactoring)':
                        #print(reasons)
                        violationsWithRefactoringNumber += 1

                fileCount += 1
                violationCount += len(csv_data)


                #print(file,len(csv_data))

                if len(csv_data) == len(falsePositiveData):
                    commitsNumberOnlyContainFalsePositive += 1

        #print information
        print(key, "Total number of commits:", fileCount)
        print(key, "Total number of violations:", violationCount)
        print(key,"Total number of false positive of violations", falsePositiveCount)
        print(key, "Total number of true positive of violations", truePositiveCount)
        print(key, "Total number of commits that only contain false positives", commitsNumberOnlyContainFalsePositive)
        print(key, "Total number of false positives that are due to refactorings", violationsWithRefactoringNumber)

        totalCommits += fileCount
        totalViolations += violationCount
        totalFalsePositives += falsePositiveCount
        totalCommitsOnlyContainsFalsePositives += commitsNumberOnlyContainFalsePositive
        totalRefactoring += violationsWithRefactoringNumber
        totalTruePositives += truePositiveCount
    print("Total info:")
    print("Commits:",totalCommits)
    print("Violations:",totalViolations)
    print("False positives:",totalFalsePositives)
    print("True positives:", totalTruePositives)
    print("Commits Only Contains FalsePositives:", totalCommitsOnlyContainsFalsePositives)
    print("refacotoring:", totalRefactoring)
if __name__ == "__main__":

    basicPath = "/Users/lijunjie/Desktop/Master/manual work/labeled results/"
    basicPath2 = "/Users/lijunjie/Desktop/Master/manual work/resultsLJJ/"
    #basicPath = "/home/ljj/test/resultsLJJ/"
    jcloudsSpotbugsPath = basicPath + "Spotbugs/jclouds"
    jcloudsPMDPath = basicPath + "PMD/jclouds"
    kafkaSpotbugsPath = basicPath + "Spotbugs/kafka"
    kafkaPMDPath = basicPath + "PMD/kafka"
    saveResultPathOnLinux = { "kafka_PMD":kafkaPMDPath,"kafka_Spotbugs":kafkaSpotbugsPath,"jclouds_PMD":jcloudsPMDPath,"jclouds_Spotbugs":jcloudsSpotbugsPath}
    #getStatisticInfo(saveResultPathOnLinux)


    string = "/NewUnmatchedViolations"
    newjcloudsSpotbugsPath = basicPath2 + "Spotbugs/jclouds"+string
    newjcloudsPMDPath = basicPath2 + "PMD/jclouds"+string
    newkafkaSpotbugsPath = basicPath2 + "Spotbugs/kafka"+string
    newkafkaPMDPath = basicPath2 + "PMD/kafka"+string
    newDict = {"kafka_PMD":newkafkaPMDPath,"kafka_Spotbugs":newkafkaSpotbugsPath,"jclouds_PMD":newjcloudsPMDPath,"jclouds_Spotbugs":newjcloudsSpotbugsPath}
    goneDict = saveResultPathOnLinux
    goneOrNew = "_new_warnings.csv"
    #countNewViolations(newDict, goneDict,goneOrNew)


    ###count labeled new violations
    labeledNewViolationPath = "/Users/lijunjie/Desktop/Master/manual work/newViolations/labeled/"
    jcloudsSpotbugsPath = labeledNewViolationPath + "Spotbugs/jclouds"+string
    jcloudsPMDPath = labeledNewViolationPath + "PMD/jclouds"+string
    kafkaSpotbugsPath = labeledNewViolationPath + "Spotbugs/kafka"+string
    kafkaPMDPath = labeledNewViolationPath + "PMD/kafka"+string
    labedNewDic = { "kafka_PMD":kafkaPMDPath,"kafka_Spotbugs":kafkaSpotbugsPath,"jclouds_PMD":jcloudsPMDPath,"jclouds_Spotbugs":jcloudsSpotbugsPath}
    getStatisticInfo(labedNewDic)