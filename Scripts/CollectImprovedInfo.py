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



def getStatisticInfo(dict):
    totalViolations = 0
    totalRefactoring = 0
    totalFalsePositives = 0
    totalCommitsOnlyContainsFalsePositives = 0
    totalNewData = 0
    totalTruePositives = 0
    totalFPinstance = []
    for key, value in dict.items():
        print()
        print(key)

        ##2. count line
        files = os.listdir(value)
        fileCount = 0   ## total commits
        violationCount = 0  ## total violations
        falsePositiveCount = 0#Total number of false positive and true positive  of violations
        truePositiveCount = 0
        newDataCount = 0
        commitsNumberOnlyContainFalsePositive = 0#number of commits that only contain false positives
        violationsWithRefactoringNumber = 0#how many false positives are due to refactoring
        FPinfo = []
        for file in files:
            if file.startswith('.'):
                continue
            csv_data = pd.read_csv(value + '/' + file)
            if len(csv_data)!= 0 :
                falsePositiveData = csv_data.loc[csv_data['False positive/true positive'] == 'f']
                falsePositiveCount += len(falsePositiveData)


                truePositiveData = csv_data.loc[csv_data['False positive/true positive'] == 't']
                truePositiveCount += len(truePositiveData)

                newData = csv_data.loc[csv_data['False positive/true positive'].isnull()]
                newDataCount +=len(newData)
                if len(newData)>0:
                    print("New: ",file,len(newData))

                for index,violation in falsePositiveData.iterrows():
                    #print(violation)
                    reasons = violation["Reasons"]
                    FPinfo = []
                    FPinfo.append(key)
                    FPinfo.append(file)
                    FPinfo.append(reasons)
                    totalFPinstance.append(FPinfo)

                    #print(reasons)
                    if reasons.split(':')[0] == '(refactoring)':
                        #print(reasons)
                        violationsWithRefactoringNumber += 1

                fileCount += 1
                violationCount += len(csv_data)

                # print("violation:",violationCount)
                # print("false/positibes:",falsePositiveCount)
                # print("true/positibes:", truePositiveCount)
                #
                # print("new:",newDataCount)
                #print(file,len(csv_data))

                if len(csv_data) == len(falsePositiveData):
                    commitsNumberOnlyContainFalsePositive += 1

        #print information
        print(key, "Total number of commits:", fileCount)
        print(key, "Total number of violations:", violationCount)
        print(key,"Total number of false positive of violations", falsePositiveCount)
        print(key, "Total number of true positive of violations", truePositiveCount)
        print(key, "Total number of new data of violations", newDataCount)
        print(key, "Total number of commits that only contain false positives", commitsNumberOnlyContainFalsePositive)
        print(key, "Total number of false positives that are due to refactorings", violationsWithRefactoringNumber)


        totalViolations += violationCount
        totalFalsePositives += falsePositiveCount
        totalTruePositives += truePositiveCount
        totalCommitsOnlyContainsFalsePositives += commitsNumberOnlyContainFalsePositive
        totalRefactoring += violationsWithRefactoringNumber
        totalNewData += newDataCount
    print("Total info:")
    print("Violations:",totalViolations)
    print("False positives:",totalFalsePositives)
    print("New data:", totalNewData)
    print("refactoring:",totalRefactoring)
    print("True positives:",totalTruePositives)
    print("len of FP:",len(totalFPinstance) )
    # for f in totalFPinstance:
    #
    #     print(f[0])
    #     print(f[1])
    #     print(f[2])
    # print("refacotoring:", totalRefactoring)
if __name__ == "__main__":

    # #count gone violations
    # basicPathLinux = r"/home/ljj/test/ImprovedResults/labeledResults/"
    # basicPathMac = r"/Users/lijunjie/Desktop/Master/manual work/ImprovedResults/labeledResults/"
    #
    # jcloudsSpotbugsPath = basicPathMac + "Spotbugs/jclouds"
    # jcloudsPMDPath = basicPathMac + "PMD/jclouds"
    # kafkaSpotbugsPath = basicPathMac + "Spotbugs/kafka"
    # kafkaPMDPath = basicPathMac + "PMD/kafka"
    # saveResultPathOnLinux = {"kafka_PMD":kafkaPMDPath,"kafka_Spotbugs":kafkaSpotbugsPath,"jclouds_Spotbugs":jcloudsSpotbugsPath,"jclouds_PMD":jcloudsPMDPath}
    # getStatisticInfo(saveResultPathOnLinux)

    ###count labeled new violations
    labeledNewViolationPath = r"/Users/lijunjie/Desktop/Master/manual work/labeledNewResult/"
    jcloudsSpotbugsPath = labeledNewViolationPath + "Spotbugs/jclouds"
    jcloudsPMDPath = labeledNewViolationPath + "PMD/jclouds"
    kafkaSpotbugsPath = labeledNewViolationPath + "Spotbugs/kafka"
    kafkaPMDPath = labeledNewViolationPath + "PMD/kafka"
    labedNewDic = {"kafka_PMD": kafkaPMDPath, "kafka_Spotbugs": kafkaSpotbugsPath, "jclouds_PMD": jcloudsPMDPath,
                   "jclouds_Spotbugs": jcloudsSpotbugsPath}
    getStatisticInfo(labedNewDic)