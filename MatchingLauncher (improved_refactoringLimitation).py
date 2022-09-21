import time
import MatcherOriginal
import MatcherImproved
import XMLreader as xmlreader
import os
import pandas as pd
import jpype
import Utils as utils
import json

###the Path on Macbook
basicPathOnMac = r"/Users/lijunjie/Desktop/Master"
jcloudsPathOnMac = basicPathOnMac + r"/testProject/jclouds"
kafkaPathOnMac = basicPathOnMac + r"/testProject/kafka"
pmdPathOnMac = basicPathOnMac + r"/AnalysisTools/pmd-bin-6.20.0/bin"
saveJcloudsPMDReportPathOnMac = basicPathOnMac + r"/Reports/PMD/Jclouds"
CommitListPathOnMac = r"./CommitList/Jclouds300commitList.txt"
testCommitListPathOnMac = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/Jclouds2commitList.txt"
# saveOldApproachPath = basicPath+'/Result_old_approach'
# saveNewApproachPath = basicPath+'/Result_new_approach'
###the Path on Ubuntu####NEED TO CHANGE
basicPathOnLinux = r"/home/ljj/test"
kafkaPathOnLinux = basicPathOnLinux + r"/Projects/kafka"
jcloudsPathOnLinux = basicPathOnLinux + r"/Projects/jclouds"

pmdPathOnLinux = basicPathOnLinux + r'/AnalyzeTools/pmd-bin-6.20.0/bin'
commitsKafkaPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/Kafka2000commitList.txt"
commitsJcloudsPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/Jclouds2000UpdateCommitList"
CommitListPathOnLinux300jclouds = r"./CommitList/Jclouds300UpdateCommitList.txt"

saveJcloudsPMDReportPathOnLinux = basicPathOnLinux + r"/Reports/PMD/jclouds"
saveKafkaPMDReportPathOnLinux = basicPathOnLinux + r"/Reports/PMD/kafka"
saveKafkaSpotbugsReportPathOnLinux = basicPathOnLinux + r"/Reports/Spotbugs/kafka"
saveJcloudsSpotbugsReportPathOnLinux = basicPathOnLinux + r"/Reports/Spotbugs/jclouds"

saveJcloudsSpotbugsResultPath = basicPathOnLinux + r'/ImprovedResults/Spotbugs/jclouds'
saveKafkaPMDResultPath = basicPathOnLinux + r'/ImprovedResults/PMD/kafka'
saveKafkaSpotbugsResultPath = basicPathOnLinux + r'/ImprovedResults/Spotbugs/kafka'
saveJcloudsPMDResultPath = basicPathOnLinux + r'/ImprovedResults/PMD/jclouds'

commitsJcloudsPMDPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/jclouds_PMD.txt"
commitsKafkaPMDPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/kafka_PMD.txt"
commitsJcloudsSpotbugsPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/jclouds_Spotbugs.txt"
commitsKafkaSpotbugsPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/kafka_Spotbugs.txt"

kafkaGithub = "https://github.com/apache/kafka"
jcloudsGithub = "https://github.com/jclouds/jclouds"

###step1 read commitlist and set parent commit and child commit

###step2 set repo path and set reporot path and set reader
###step3 using matching algorithm
###step4 save Result and Report


# kafkaResult1=saveSBReportPath+'/'+line+'.xml'
# kafkaResult2=saveSBReportPath+'/'+line+'.xml'

githubUrl = kafkaGithub
##start JVM
jarpath = os.path.join(os.path.abspath('.'),
                       r'D:\ThesisProject\findbugsanalysis\FixPatternMining\refactoringJava\out\production\refactoringJava')
dependency = os.path.join(os.path.abspath('.'),
                          r'D:\ThesisProject\RefactoringMiner\build\distributions\RefactoringMiner-1.0\RefactoringMiner-1.0\lib')

jvmPath = jpype.getDefaultJVMPath()
if not jpype.isJVMStarted():
    jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarpath, "-Djava.ext.dirs=%s" % dependency)

jClass = jpype.JClass("edu.concordia.junjie.RefactoringInfo")


with open(r"D:\Thesis\code\findLimitation\finalData.json", "r") as dataJson:
    data = json.loads(dataJson.read())
count=0
filterCount = 0
blackList = [r'liferay-portal',r'android_frameworks_base',r'intellij-community',r'MPS',r'robovm',r'liferay-plugins',r'hive',r'voltdb']
for eachCommit in data:
    #print(f"{eachCommit['repoName']}\n{eachCommit['childCommit']}")

    if eachCommit["repoName"]  in blackList:
        #filterCount += 1
        continue
    startTime = time.time()
    #print(f"repoName:{eachCommit['repoName']} childCommit:{eachCommit['childCommit'][0:7]}")
    parentCommit = eachCommit['parentCommit']
    childCommit = eachCommit['childCommit']
    repoPath = eachCommit['repoPath']
    reportsPath = r"D:\Thesis\limitationRefactoring\reports"
    folderName = reportsPath + "\\" + eachCommit['repoName']
    #fileName = eachCommit['repoName'] + "_" + eachCommit['childCommit'][0:7] + ".xml"
    #saveReportPath = folderName + "\\" + fileName
    childFilename = folderName + "\\" + eachCommit['repoName'] + "_" + eachCommit['childCommit'][0:7] + ".xml"
    parentFilename = folderName + "\\" + eachCommit['repoName'] + "_" + eachCommit['parentCommit'][0:7] + ".xml"
    Reader = xmlreader.PMDReader
    parentBuginstances = Reader(parentFilename)
    childBuginstances = Reader(childFilename)
    #print(f'len of parentBuginstances:{len(parentBuginstances)}')
    # if  len(parentBuginstances)>= 30000:
    #     count += 1
    #     print(f'repoName:{eachCommit["repoName"]}\nparentCommit:{parentCommit}\nlenOfWarning:{len(parentBuginstances)}\ncount:{count}')

    saveResultsPath = r"D:\Thesis\limitationRefactoring\results"
    folderResultsPath = saveResultsPath + '\\' + eachCommit['repoName']
    if not os.path.exists(folderResultsPath):
        os.makedirs(folderResultsPath)
        os.makedirs(folderResultsPath+'\\'+"newViolations")
        os.makedirs(folderResultsPath+'\\'+"goneViolations")
    saveNewViolations = folderResultsPath+'\\'+"newViolations"
    saveGoneViolations = folderResultsPath+'\\'+"goneViolations"
    unmatchedChild, unmatchedParent = MatcherImproved.matchChildParent(repoPath, parentBuginstances, childBuginstances,
                                                               parentCommit, childCommit, githubUrl, jClass)


    # unmatchedChild, unmatchedParent = Matcher.matchChildParent(repoPath, parentBuginstances, childBuginstances,
    #                                                            parentCommit, childCommit)

    bugAbbvSetParent = []
    categorySetParent = []
    classSetParent = []
    methodSetParent = []
    fieldSetParent = []
    sourcePathSetParent = []
    startSetParent = []
    endSetParent = []
    for eachUnmatched in unmatchedParent:
        bugAbbvSetParent.append(eachUnmatched.getBugAbbv())
        categorySetParent.append(eachUnmatched.getCategoryAbbrev())
        classSetParent.append(eachUnmatched.getClass())
        methodSetParent.append(eachUnmatched.getMethod())
        fieldSetParent.append(eachUnmatched.getField())
        sourcePathSetParent.append(eachUnmatched.getSourcePath())
        startSetParent.append(eachUnmatched.getStartLine())
        endSetParent.append(eachUnmatched.getEndLine())

    dataframe = pd.DataFrame(
        {'Bug': bugAbbvSetParent, 'category': categorySetParent, "class name": classSetParent,
         "method name": methodSetParent, "field name": fieldSetParent, "source path": sourcePathSetParent,
         "start": startSetParent, "end": endSetParent})

    dataframe.to_csv(saveGoneViolations + "/" + parentCommit[0:7] + "_" + childCommit[0:7] + "_gone_warnings.csv", index=False,
                     sep=',')

    bugAbbvSetChild = []
    categorySetChild = []
    classSetChild = []
    methodSetChild = []
    fieldSetChild = []
    sourcePathSetChild = []
    startSetChild = []
    endSetChild = []
    for eachUnmatched in unmatchedChild:
        bugAbbvSetChild.append(eachUnmatched.getBugAbbv())
        categorySetChild.append(eachUnmatched.getCategoryAbbrev())
        classSetChild.append(eachUnmatched.getClass())
        methodSetChild.append(eachUnmatched.getMethod())
        fieldSetChild.append(eachUnmatched.getField())
        sourcePathSetChild.append(eachUnmatched.getSourcePath())
        startSetChild.append(eachUnmatched.getStartLine())
        endSetChild.append(eachUnmatched.getEndLine())

    dataframe = pd.DataFrame(
        {'Bug': bugAbbvSetChild, 'category': categorySetChild, "class name": classSetChild, \
         "method name": methodSetChild, "field name": fieldSetChild, "source path": sourcePathSetChild, \
         "start": startSetChild, "end": endSetChild})

    dataframe.to_csv(saveNewViolations + "/" + parentCommit[0:7] + "_" + childCommit[0:7] + "_new_warnings.csv", index=False,
                     sep=',')
    count+=1
    endTime = time.time()
    print(f"finish {count}/387 time:{endTime-startTime} lenOfBuginstance:{len(parentBuginstances)}")




jpype.shutdownJVM()
# if __name__ == "__main__":
#     instances = xmlreader.PMDReader(r'D:\Thesis\limitationRefactoring\reports\elasticsearch\elasticsearch_4f4b1b7.xml')



