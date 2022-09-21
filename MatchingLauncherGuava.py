import csv
import time
import MatcherOriginal
import XMLreader as xmlreader
import os
import pandas as pd
import MatchedPairsCollector

###Parameter setting
guavaPMDReportsPath = r'D:\ThesisData\Reports\PMD\guava'
guavaSpotbugsReportsPath = r'D:\ThesisData\Reports\Spotbugs\guava'

saveGuavaPMDMatchedPairsSavePath = r'D:\ThesisData\MatchedPairs\PMD\guava'
saveGuavaSpotbugsMatchedPairsSavePath = r'D:\ThesisData\MatchedPairs\Spotbugs\guava'

saveGuavaPMDResultsPath = r'D:\ThesisData\OriginalResults\PMD\guava'
saveGuavaSpotbugsResultsPath = r'D:\ThesisData\OriginalResults\Spotbugs\guava'

commitListPath2000 = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Guava2000commitList.txt'
projectPath = r'D:\ThesisProject\trackingProjects\guava'

TimeMeasurmentPMDPath = r"D:\ThesisData\TimeMeasurment\Original\PMD\guava\TimeMeasurment.csv"
TimeMeasurmentSpotbugsPath = r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\guava\TimeMeasurment.csv"



commitPathPMD = commitListPath2000
commitPathSpotbugs = commitListPath2000
saveResultsPathPMD =saveGuavaPMDResultsPath
saveResultsPathSpotbugs =saveGuavaSpotbugsResultsPath
reportsPathPMD = guavaPMDReportsPath
reportsPathSpotbugs = guavaSpotbugsReportsPath
saveMatchedPairsPathPMD = saveGuavaPMDMatchedPairsSavePath
saveMatchedPairsPathSpotbugs = saveGuavaSpotbugsMatchedPairsSavePath
TimeMeasurmentPMDPath = TimeMeasurmentPMDPath
TimeMeasurmentSpotbugsPath = TimeMeasurmentSpotbugsPath
PMD = xmlreader.PMDReader
Spotbugs = xmlreader.SpotbugsReader





if __name__ == "__main__":
    f = open(commitListPath2000)
    commitList = f.readlines()

    goneResultsPath = os.path.join(saveResultsPathPMD,'gone')
    for i,j,k in os.walk(goneResultsPath):
        fNewList = k
    repoPath = projectPath
    commitList = []
    with open(commitListPath2000) as ff:
        line = ff.readline()
        while line:
            if line[-1] == '\n':
                line = line[:-1]
            commitList.append(line)
            line = ff.readline()
    ####init time measurment file
    if not os.path.exists(TimeMeasurmentPMDPath):
        with open(TimeMeasurmentPMDPath, "w") as csvfile:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(TimeMeasurmentSpotbugsPath):
        with open(TimeMeasurmentSpotbugsPath, "w") as csvfile:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    count = 1
    commitsSkipList = ["fd919e54a55ba169dc7d9f54b7b3485aa7fa0970","fd919e54a55ba169dc7d9f54b7b3485aa7fa0970"]
    ######
    # start to track PMD
    ######
    for i in range(len(commitList[:-1])):
    #for i in range(2):
        parentCommit = commitList[i]
        childCommit =  commitList[i+1]
        parentCommit = parentCommit.replace("\n", "")
        childCommit = childCommit.replace("\n", "")
        if childCommit in commitsSkipList:
            count += 1
            print(f"commit {childCommit} is skipped")
            continue
        ######
        #check whether a certain commit was finished
        ######
        flag = False
        for name in fNewList:
            if parentCommit[0:7] + "_" + childCommit[0:7]+ "_gone_warnings.csv" == name:
                flag = True
        if flag:
            count += 1
            print(f"commit {childCommit} exsits")
            continue
        print(f"start to commit:{childCommit}")
        ######
        # read warning report files
        ######
        reportParent = os.path.join(reportsPathPMD, parentCommit + '.xml')
        reportChild = os.path.join(reportsPathPMD, childCommit + '.xml')
        childFilename = reportChild
        parentFilename = reportParent
        parentBuginstances = PMD(parentFilename)
        childBuginstances = PMD(childFilename)

        ######
        #run the original approach
        ######
        repoPath = projectPath
        matchingStartTime = time.time()
        unmatchedChild, unmatchedParent, matchedPairs = MatcherOriginal.matchChildParent(repoPath,parentBuginstances,childBuginstances, parentCommit,childCommit)
        matchingEndTime = time.time()

        ######
        # save new and gone results
        ######
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


        saveGoneResults = os.path.join(saveResultsPathPMD,'gone')
        dataframe.to_csv(os.path.join(saveGoneResults,parentCommit[0:7] + "_" + childCommit[0:7] + "_gone_warnings.csv"), index=False,
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
            {'Bug': bugAbbvSetChild, 'category': categorySetChild, "class name": classSetChild,\
             "method name": methodSetChild,"field name":  fieldSetChild,"source path":sourcePathSetChild,\
             "start":startSetChild,"end":endSetChild})

        saveNewResults = os.path.join(saveResultsPathPMD, 'new')
        dataframe.to_csv(
            os.path.join(saveNewResults, parentCommit[0:7] + "_" + childCommit[0:7] + "_new_warnings.csv"),
            index=False,
            sep=',')



        matchedPairsSavePath = os.path.join(saveMatchedPairsPathPMD,str(childCommit) + '.xml')
        MatchedPairsCollector.wrtieToXML(matchedPairs,matchedPairsSavePath)
        row = [childCommit, matchingEndTime - matchingStartTime]
        with open(TimeMeasurmentPMDPath, 'a', newline='') as f:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Commit': row[0], 'Time': row[1]})
        print(f"finish {count}/{len(commitList)} commits PMD")
        count += 1

    print("finish analysis of PMD")







    ###start to Spotbugs
    goneResultsPath = os.path.join(saveResultsPathSpotbugs, 'gone')
    for i, j, k in os.walk(goneResultsPath):
        fNewList = k
    repoPath = projectPath

    ###start to track Spotbugs
    f = open(commitListPath2000)
    #print(f"open file {commitListPathOnWin2000}")
    commitList = f.readlines()

    count = 1
    for i in range(len(commitList)-1):
    #for i in range(2):
        flag = False
        parentCommit = commitList[i]  ###parentCommit
        childCommit = commitList[i + 1]  ###childCommit
        parentCommit = parentCommit.replace("\n", "")
        childCommit = childCommit.replace("\n", "")
        if childCommit in commitsSkipList:
            count += 1
            print(f"commit {childCommit} is skipped")
            continue

        for name in fNewList:
            if commitList[i][0:7] + "_" + commitList[i + 1][0:7] + "_gone_warnings.csv" == name:
                flag = True
        if flag:
            count += 1
            print(f"commit {childCommit} exsits")
            continue

        print(f"start to commit:{childCommit}")
        reportParent = os.path.join(reportsPathSpotbugs, parentCommit + '.xml')
        reportChild = os.path.join(reportsPathSpotbugs, childCommit + '.xml')

        childFilename = reportChild
        parentFilename = reportParent
        parentBuginstances = Spotbugs(parentFilename)
        childBuginstances = Spotbugs(childFilename)

        repoPath = projectPath


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

        saveGoneResults = os.path.join(saveResultsPathSpotbugs, 'gone')
        dataframe.to_csv(
            os.path.join(saveGoneResults, commitList[i][0:7] + "_" + commitList[i + 1][0:7] + "_gone_warnings.csv"),
            index=False,
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

        saveNewResults = os.path.join(saveResultsPathSpotbugs, 'new')
        dataframe.to_csv(
            os.path.join(saveNewResults, commitList[i][0:7] + "_" + commitList[i + 1][0:7] + "_new_warnings.csv"),
            index=False,
            sep=',')

        # test
        # dataframe.to_csv("commendline-U.csv", index=False, sep=',')
        ##

        matchedPairsSavePath = os.path.join(saveMatchedPairsPathSpotbugs, str(childCommit) + '.xml')
        MatchedPairsCollector.wrtieToXML(matchedPairs, matchedPairsSavePath)
        row = [childCommit, matchingEndTime - matchingStartTime]
        with open(TimeMeasurmentSpotbugsPath, 'a', newline='') as f:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Commit': row[0], 'Time': row[1]})
        print(f"finish {count}/{len(commitList)} commits Spotbugs::{childCommit}")
        count += 1

    print("finish analysis of Spotbugs")