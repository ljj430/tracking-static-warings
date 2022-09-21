import csv
import time
import MatcherOriginal
import XMLreader as xmlreader
import os
import pandas as pd
import MatchedPairsCollector



####ReadMe####
#Some packages are required:
# 1.pandas
# 2.gitpython
###Two steps to run this code
# 1.set the parameters as below
# 2.In 'read warning report files' parts(there are two parts of 'read warning report files' i.e.,Spotbugs and PMD), you need to set the file name. In my experiment, I set report file name as <commit>.xml So it is easy to read them iterally.
# Maybe you can use a Dic {commit:filename} to do so, or re-set your reports name.
### Note:
# you can first run just 2 commits to test this code
# if there is a 'no element found' error, run Scripts/AddEndingOfPMDReports.py and set the path(PMD reports path) in that file.

def main():
    fNewList = []
    pmd_failed_list = []
    ###Parameter setting
    springPMDReportsPath = r'C:\Workspace\temp\pmd_reports'
    springSpotbugsReportsPath = r'C:\Workspace\temp\spotbugs_reports'

    saveSpringPMDMatchedPairsSavePath = r'C:\Workspace\temp\pmd_matched_pairs'
    saveSpringSpotbugsMatchedPairsSavePath = r'C:\Workspace\temp\spotbugs_matched_pairs'

    saveSpringPMDResultsPath = r'C:\Workspace\temp\pmd_results'
    saveSpringSpotbugsResultsPath = r'C:\Workspace\temp\spotbugs_results'

    commitListPath2000 = r'C:\Workspace\temp\hashs.txt'
    projectPath = r'C:\Workspace\temp\spring-boot'

    TimeMeasurmentPMDPath = r"C:\Workspace\temp\pmd_time_measurment\TimeMeasurment.csv"
    TimeMeasurmentSpotbugsPath = r"C:\Workspace\temp\spotbugs_time_measurement\TimeMeasurment.csv"

    saveResultsPathPMD =saveSpringPMDResultsPath
    saveResultsPathSpotbugs =saveSpringSpotbugsResultsPath
    reportsPathPMD = springPMDReportsPath
    reportsPathSpotbugs = springSpotbugsReportsPath
    saveMatchedPairsPathPMD = saveSpringPMDMatchedPairsSavePath
    saveMatchedPairsPathSpotbugs = saveSpringSpotbugsMatchedPairsSavePath
    TimeMeasurmentPMDPath = TimeMeasurmentPMDPath
    TimeMeasurmentSpotbugsPath = TimeMeasurmentSpotbugsPath
    PMD = xmlreader.PMDReader
    Spotbugs = xmlreader.SpotbugsReader
    

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
    #########
    ####init time measurment file
    #########
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
    ######
    # start to track PMD
    ######
    for i in range(len(commitList[:-1])):
    #for i in range(2):
        parentCommit = commitList[i]
        childCommit =  commitList[i+1]
        parentCommit = parentCommit.replace("\n", "")
        childCommit = childCommit.replace("\n", "")

        ######
        #check whether a certain commit was finished. if yes, jump to next
        ######
        flag = False
        for name in fNewList:
            if parentCommit[0:7] + "_" + childCommit[0:7]+ "_gone_warnings.csv" == name:
                flag = True
        if flag:
            count += 1
            print(f"commit {childCommit} exsits")
            continue

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
        try:
            unmatchedChild, unmatchedParent, matchedPairs = MatcherOriginal.matchChildParent(repoPath,parentBuginstances,childBuginstances, parentCommit,childCommit)
        except KeyError:
            pmd_failed_list.append(childCommit)
            continue

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
    print("pmd failed commits")
    [print(commit) for commit in pmd_failed_list]

    spotbugs_not_typical_failed_list = []
    spotbugs_build_failed_list = []

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


        for name in fNewList:
            if commitList[i][0:7] + "_" + commitList[i + 1][0:7] + "_gone_warnings.csv" == name:
                flag = True
        if flag:
            count += 1
            print(f"commit {childCommit} exsits")
            continue

        print(f"start to commit:{childCommit}")

        ######
        # read warning report files
        ######
        reportParent = os.path.join(reportsPathSpotbugs, parentCommit + '.xml')
        reportChild = os.path.join(reportsPathSpotbugs, childCommit + '.xml')

        childFilename = reportChild
        parentFilename = reportParent

        try:
            parentBuginstances = Spotbugs(parentFilename)
            childBuginstances = Spotbugs(childFilename)
            
        except:
            spotbugs_build_failed_list.append(childCommit)
            continue

        repoPath = projectPath


        matchingStartTime = time.time()
        try:
            unmatchedChild, unmatchedParent, matchedPairs = MatcherOriginal.matchChildParent(repoPath, parentBuginstances,
                                                                                            childBuginstances,
                                                                                            parentCommit, childCommit)
        except KeyError:
            spotbugs_not_typical_failed_list.append(childCommit)
            continue

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
    print("spotbugs not typical failed commits")
    [print(commit) for commit in spotbugs_not_typical_failed_list]
    print("spotbugs build failed commits")
    [print(commit) for commit in spotbugs_build_failed_list]



main()