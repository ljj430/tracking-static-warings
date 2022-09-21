import csv
import time
import MatcherOriginal
import XMLreader as xmlreader
import os
import pandas as pd

####jclouds PMD

###the Path on Macbook
import MatchedPairsCollector

basicPathOnMac = r"/Users/lijunjie/Desktop/Master"
jcloudsPathOnMac = basicPathOnMac + r"/testProject/jclouds"
kafkaPathOnMac = basicPathOnMac + r"/testProject/kafka"
pmdPathOnMac = basicPathOnMac + r"/AnalysisTools/pmd-bin-6.20.0/bin"
saveJcloudsPMDReportPathOnMac = basicPathOnMac + r"/Reports/PMD/Jclouds"
CommitListPathOnMac = r"./CommitList/Jclouds300commitList.txt"
testCommitListPathOnMac = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/Jclouds2commitList.txt"
#saveOldApproachPath = basicPath+'/Result_old_approach'
#saveNewApproachPath = basicPath+'/Result_new_approach'
###the Path on Ubuntu####NEED TO CHANGE
basicPathOnLinux = r"/home/ljj/test"
kafkaPathOnLinux=basicPathOnLinux+r"/Projects/kafka"
jcloudsPathOnLinux=basicPathOnLinux+r"/Projects/jclouds"
pmdPathOnLinux =basicPathOnLinux +  r'/AnalyzeTools/pmd-bin-6.20.0/bin'

commitsKafkaPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/Kafka2000commitList.txt"
commitsJcloudsPath = basicPathOnLinux + r"/findbugsanalysis/FixPatternMining/CommitList/Jclouds2000UpdateCommitList.txt"

CommitListPathOnLinux300jclouds = r"./CommitList/Jclouds300UpdateCommitList.txt"
testCommitListPathOnLinux = r"testCommitList.txt"
jcloudsPathOnLinux = basicPathOnLinux + r"/Projects/jclouds"

saveJcloudsPMDReportPathOnLinux = basicPathOnLinux + r"/Reports/PMD/jclouds"
saveKafkaPMDReportPathOnLinux = basicPathOnLinux + r"/Reports/PMD/kafka"




ruleSetPathOnLinux = pmdPathOnLinux +r'/rulesets.xml'
saveJcloudsResultPath = basicPathOnLinux + r'/Results1/PMD/jclouds'
saveKafkaResultPath = basicPathOnLinux + r'/Results1/PMD/kafka'



###Parameter set
saveJcloudsPMDReportsPathOnWin = r'D:\ThesisData\Reports\PMD\jclouds'
saveJcloudsSpotbugsReportsPathOnWin = r'D:\ThesisData\Reports\Spotbugs\jclouds'
saveJcloudsPMDResultsPathOnWin = r'D:\ThesisData\OriginalResults\PMD\jclouds'
saveJcloudsSpotbugsResultsPathOnWin =r'D:\ThesisData\OriginalResults\Spotbugs\jclouds'

commitListPathOnWin2000 = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Jclouds2000UpdateCommitList.txt'
commitListPathOnWinPMD = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\jclouds_PMD.txt'
commitListPathOnWinSpotbugs = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\jclouds_Spotbugs.txt'
projectPathOnWin = r'D:\ThesisProject\trackingProjects\jclouds'

PMD = xmlreader.PMDReader
Spotbugs = xmlreader.SpotbugsReader






if __name__ == "__main__":
    # if not os.path.exists(saveResultPath):
    #     os.system('mkdir ' + saveResultPath)

    f = open(commitListPathOnWinPMD)
    commitList = f.readlines()

    goneResultsPath = os.path.join(saveJcloudsPMDResultsPathOnWin,'gone')
    for i,j,k in os.walk(goneResultsPath):
        fNewList = k
    repoPath = projectPathOnWin

    commitDic2000 = {}
    with open(commitListPathOnWin2000) as ff:
        lines = ff.readline()
        while lines:
            if lines[-1] == '\n':
                lines = lines[:-1]
            commitDic2000[lines[0:7]] = lines
            lines = ff.readline()
    ####init time measurment file
    if not os.path.exists(r"D:\ThesisData\TimeMeasurment\Original\PMD\jclouds\TimeMeasurment.csv"):
        with open(r"D:\ThesisData\TimeMeasurment\Original\PMD\jclouds\TimeMeasurment.csv", "w") as csvfile:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\jclouds\TimeMeasurment.csv"):
        with open(r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\jclouds\TimeMeasurment.csv", "w") as csvfile:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    count = 1
    ###start to track PMD
    for line in commitList:
        line = line.replace('\n', '')
        lines = line.split('_')
        parentCommit = commitDic2000[lines[0]]
        childCommit = commitDic2000[lines[1]]


        flag = False
        for name in fNewList:
            if parentCommit[0:7] + "_" + childCommit[0:7]+ "_gone_warnings.csv" == name:
                flag = True
        if flag:
            count += 1
            print(f"commit {line} exsits")
            continue
        resultParent = os.path.join(saveJcloudsPMDReportsPathOnWin, parentCommit[0:7] + '.xml')
        resultChild = os.path.join(saveJcloudsPMDReportsPathOnWin, childCommit[0:7] + '.xml')
        # kafkaResult1='spotbugs_kafka_4a5cba87bcd4621b999f7290d17d88d6859afb84.xml'
        # kafkaResult2='spotbugs_kafka_05ba5aa00847b18b74369a821e972bbba9f155eb.xml'
        ##test
        # kafkaResult1='week4kafka_4a5ccommendline.xml'
        # kafkaResult2='week4kafka4a5cUI.xml'
        ##
        childFilename = resultChild
        parentFilename = resultParent
        parentBuginstances = PMD(parentFilename)
        childBuginstances = PMD(childFilename)

        repoPath = projectPathOnWin

        matchingStartTime = time.time()
        unmatchedChild, unmatchedParent, matchedPairs = MatcherOriginal.matchChildParent(repoPath,parentBuginstances,childBuginstances, parentCommit,childCommit)
        matchingEndTime = time.time()


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
             "method name": methodSetParent,"field name":  fieldSetParent,"source path":sourcePathSetParent,
             "start":startSetParent,"end":endSetParent})


        saveGoneResults = os.path.join(saveJcloudsPMDResultsPathOnWin,'gone')
        dataframe.to_csv(os.path.join(saveGoneResults,parentCommit[0:7] + "_" + childCommit[0:7] + "_gone_warnings.csv"), index=False,
                         sep=',')


        flag = False
        for name in fNewList:
            if parentCommit[0:7] + "_" + childCommit[0:7]+ "_new_warnings.csv" == name:
                flag = True
        if flag:
            continue
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
            {'Bug': bugAbbvSetChild, 'category': categorySetChild, "class name": classSetChild,\
             "method name": methodSetChild,"field name":  fieldSetChild,"source path":sourcePathSetChild,\
             "start":startSetChild,"end":endSetChild})

        saveNewResults = os.path.join(saveJcloudsPMDResultsPathOnWin, 'new')
        dataframe.to_csv(
            os.path.join(saveNewResults,parentCommit[0:7] + "_" + childCommit[0:7] + "_new_warnings.csv"),
            index=False,
            sep=',')

        # test
        # dataframe.to_csv("commendline-U.csv", index=False, sep=',')
        ##

        matchedPairsSavePath = os.path.join(r'D:\ThesisData\MatchedPairs\PMD\jclouds',str(childCommit) + '.xml')
        MatchedPairsCollector.wrtieToXML(matchedPairs,matchedPairsSavePath)
        row = [childCommit, matchingEndTime - matchingStartTime]
        with open(r"D:\ThesisData\TimeMeasurment\Original\PMD\jclouds\TimeMeasurment.csv", 'a', newline='') as f:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Commit': row[0], 'Time': row[1]})
        print(f"finish {count}/{len(commitList)} commits PMD")
        count += 1

    print("finish analysis of PMD")

    ###start to Spotbugs
    goneResultsPath = os.path.join(saveJcloudsSpotbugsResultsPathOnWin, 'gone')
    for i, j, k in os.walk(goneResultsPath):
        fNewList = k
    repoPath = projectPathOnWin


    ###start to track Spotbugs
    f = open(commitListPathOnWinSpotbugs)
    commitList = f.readlines()
    count = 1
    for line in commitList:
        line = line.replace('\n', '')
        lines = line.split('_')
        parentCommit = commitDic2000[lines[0]]
        childCommit = commitDic2000[lines[1]]


        flag = False
        for name in fNewList:
            if parentCommit[0:7] + "_" + childCommit[0:7] + "_gone_warnings.csv" == name:
                flag = True
        if flag:
            count += 1
            print(f"commit {line} exsits")
            continue
        resultParent = os.path.join(saveJcloudsSpotbugsReportsPathOnWin, parentCommit[0:7] + '.xml')
        resultChild = os.path.join(saveJcloudsSpotbugsReportsPathOnWin, childCommit[0:7] + '.xml')
        # kafkaResult1='spotbugs_kafka_4a5cba87bcd4621b999f7290d17d88d6859afb84.xml'
        # kafkaResult2='spotbugs_kafka_05ba5aa00847b18b74369a821e972bbba9f155eb.xml'
        ##test
        # kafkaResult1='week4kafka_4a5ccommendline.xml'
        # kafkaResult2='week4kafka4a5cUI.xml'
        ##
        childFilename = resultChild
        parentFilename = resultParent
        parentBuginstances = Spotbugs(parentFilename)
        childBuginstances = Spotbugs(childFilename)

        repoPath = projectPathOnWin

        matchingStartTime = time.time()
        unmatchedChild, unmatchedParent, matchedPairs = MatcherOriginal.matchChildParent(repoPath, parentBuginstances,
                                                                                         childBuginstances,
                                                                                         parentCommit, childCommit)
        matchingEndTime = time.time()

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

        saveGoneResults = os.path.join(saveJcloudsSpotbugsResultsPathOnWin, 'gone')
        dataframe.to_csv(
            os.path.join(saveGoneResults, parentCommit[0:7] + "_" + childCommit[0:7] + "_gone_warnings.csv"),
            index=False,
            sep=',')

        flag = False
        for name in fNewList:
            if parentCommit[0:7] + "_" + childCommit[0:7] + "_new_warnings.csv" == name:
                flag = True
        if flag:
            continue
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

        saveNewResults = os.path.join(saveJcloudsSpotbugsResultsPathOnWin, 'new')
        dataframe.to_csv(
            os.path.join(saveNewResults, parentCommit[0:7] + "_" + childCommit[0:7] + "_new_warnings.csv"),
            index=False,
            sep=',')

        # test
        # dataframe.to_csv("commendline-U.csv", index=False, sep=',')
        ##

        matchedPairsSavePath = os.path.join(r'D:\ThesisData\MatchedPairs\Spotbugs\jclouds', str(childCommit) + '.xml')
        MatchedPairsCollector.wrtieToXML(matchedPairs, matchedPairsSavePath)
        row = [childCommit, matchingEndTime - matchingStartTime]
        with open(r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\jclouds\TimeMeasurment.csv", 'a', newline='') as f:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Commit': row[0], 'Time': row[1]})
        print(f"finish {count}/{len(commitList)} commits Spotbugs")
        count += 1

    print("finish analysis of Spotbugs")

