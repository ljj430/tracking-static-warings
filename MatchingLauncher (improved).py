import time
import MatcherOriginal
import MatcherImproved
import XMLreader as xmlreader
import os
import pandas as pd
import jpype
import Utils as utils

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
                       '/home/ljj/test/findbugsanalysis/FixPatternMining/refactoringJava/out/production/refactoringJava')
dependency = os.path.join(os.path.abspath('.'),
                          '/home/ljj/test/AnalyzeTools/RefactoringMiner/build/distributions/RefactoringMiner-1.0/lib')

jvmPath = jpype.getDefaultJVMPath()
if not jpype.isJVMStarted():
    jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarpath, "-Djava.ext.dirs=%s" % dependency)

jClass = jpype.JClass("edu.concordia.junjie.RefactoringInfo")



commitListPath = commitsKafkaSpotbugsPath

f = open(commitListPath)
lines = f.readline()
while lines:
    lines = lines.replace('\n', '')
    print(lines)
    ###step1 read commitlist and set parent commit and child commit
    lines = lines.split('_')
    parentCommit = lines[0]
    childCommit = lines[1]

    ###step2 set repo path and set reporot path,child and parent filenames and set reader
    projectPath = kafkaPathOnLinux  ##project
    repoPath = projectPath

    saveReportPath = saveKafkaSpotbugsReportPathOnLinux
    childFilename = saveReportPath + '/' + childCommit + '.xml'
    parentFilename = saveReportPath + '/' + parentCommit + '.xml'

    Reader = xmlreader.SpotbugsReader
    parentBuginstances = Reader(parentFilename)
    childBuginstances = Reader(childFilename)

    saveResultPath = saveKafkaSpotbugsResultPath
    saveNewViolations = saveResultPath+'/NewUnmatchedViolations'
    saveGoneViolations = saveResultPath+'/GoneUnmatchedViolations'


    unmatchedChild, unmatchedParent = MatcherImproved1.matchChildParent(repoPath, parentBuginstances, childBuginstances,
                                                               parentCommit, childCommit, githubUrl, jClass)

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

    dataframe.to_csv(saveGoneViolations + "/" + parentCommit + "_" + childCommit + "_gone_warnings.csv", index=False,
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

    dataframe.to_csv(saveNewViolations + "/" + parentCommit + "_" + childCommit + "_new_warnings.csv", index=False,
                     sep=',')
    # test
    # dataframe.to_csv("commendline-U.csv", index=False, sep=',')
    ##

    if lines[-1] == '\n':
        lines = lines[:-1]
    lines = f.readline()
jpype.shutdownJVM()





