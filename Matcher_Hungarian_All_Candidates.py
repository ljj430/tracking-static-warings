import XMLreader as xmlreader
import jpype
from Utils import Diff
import Utils as utils
import time
import pandas as pd
from io import StringIO
import git
import os
import numpy as np
from BugInstance import BugInstance
import sys
from munkres import Munkres, print_matrix
import MatcherOriginal

MATCHING_THRESHOLD = 20
DEBUG = False
TRACK = False
trackBuginstance = BugInstance()

def splitDollarMark(className):
    token = className.split("$")
    return token[0]


totoalViolationCount = 0
unchangedExactMatchCount = 0
changedExactMatchCount = 0
locationBasedCount = 0
snippetBasedCount = 0
hashBasedCount = 0
unmatchedCount = 0

unchangedExactMatchTotalTime = 0
changedExactMatchTotalTime = 0
locationBasedTotalTime = 0
snippetBasedTotalTime = 0
hashBasedTotalTime = 0
unmatchedTotalTime = 0


def matchChildParent(repoPath, parentBuginstances, childBuginstances, parentCommit, childCommit, githubUrl, jClass):
    global trackBuginstance
    global totoalViolationCount
    global unchangedExactMatchCount
    global changedExactMatchCount
    global locationBasedCount
    global snippetBasedCount
    global hashBasedCount
    global unmatchedCount

    global unchangedExactMatchTotalTime
    global changedExactMatchTotalTime
    global locationBasedTotalTime
    global snippetBasedTotalTime
    global hashBasedTotalTime
    global unmatchedTotalTime
    utils.checkout(repoPath, childCommit)
    ###initial
    parentTracked = []
    parentTracked = set(parentTracked)
    childTracked = []
    childTracked = set(childTracked)
    unmatchedParent = set()
    trackingMap = {}
    ### Diff object
    diff = Diff(repoPath)
    ###parentChangedPaths is a list that contains the package path + class name of each parent changed file
    ### diffMap is a dic (a path -> a diff object)
    ###path: kafka.common.xxx.java/scala
    ####the diffMap's key is a path org.apache.kafka.clients.st.java. the value is a diff object
    ##### parentChangedPaths list is a list that saves diffMap's key
    parentChangedPaths, childChangedPaths, diffMap = \
        utils.transformFilesToPackagePaths(diff, parentCommit, childCommit, repoPath)

    # mapParentPath = utils.createMapPath(kafkaPath, parentCommit)
    # mapchildPath = utils.createMapPath(kafkaPath, childCommit)
    ###inline functions


    def recordSuccessMatch(pa, matchedBugInstances, mainClassName, matchedby):
        untrackedInstances = matchedBugInstances - childTracked
        if len(untrackedInstances) == 0:
            return False
        else:
            ####track childBuginstance
            ### check out whether it is already in tracked alarms.(if it is, exceptional case.)
            untrackedInstances = list(untrackedInstances)
            matchedChild = untrackedInstances[0]  # assuming there are one single match.
            parentTracked.add(pa)
            childTracked.add(matchedChild)
            # print(pa)
            trackingMap[pa] = matchedChild
            return True  ##matched

    def findExactMatching(pa, mainClassName):
        matchedChildAlarms = findExactMatchingAlarm(pa, childHash)
        if (len(matchedChildAlarms) == 0):  ###no matching
            return False
        else:
            return recordSuccessMatch(pa, matchedChildAlarms, mainClassName, matchedby="exact")

    ###end inline functions
    parentBuginstances = set(parentBuginstances)
    exactCandidates = []
    locationCandidates = []
    snippetCandidates = []
    childHash = {}
    for ch in childBuginstances:
        childHash[ch] = ch

    for pa in parentBuginstances:
        ###time evaluation
        startTime = time.time()

        ###
        ### 0.find out whether it is in changed set
        ###
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True

        #### take exact matching in unchagned files.
        if not isChanged:  ###if not in changed  ##mainClassPath is like kafka.common.xxx.java
            ###
            ### 1.Try to find matching bugInstance in child alarm set
            ### (only one method available since it is in the unchanged set).
            ### exact matching in non-changed set.
            ###
            # print("start to match changed file")

            successAny = findExactMatching(pa, mainClassPath)
            if successAny == True:
                if DEBUG and TRACK:
                    print("success match in unchanged exact matching")
                unchangedExactMatchCount = unchangedExactMatchCount + 1
                endTime = time.time()
                unchangedExactMatchTotalTime = unchangedExactMatchTotalTime + endTime - startTime

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After exact matching in unchanged file:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")

    githubPath = githubUrl
    instance = jClass()
    refactoringInfo = instance.getRefactoringInfo(repoPath, githubPath, childCommit)
    paCandidates, chCandidates, candidatesList = set(), set(), []
    for pa in untrackedParent:
        ####todo:snippet matching
        ### 1.take snippet-based matching
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True
        if isChanged:
            d = diffMap[mainClassPath]
            if utils.getDiffType(d) == "A" or utils.getDiffType(d) == "D":
                pass
            else:
                candidates = set()
                snippetMatchingInstance = set()
                for ch in untrackedChild:
                    if utils.isSameButDiffLoc(pa, ch):
                        candidates.add(ch)
                if len(candidates) > 0:
                    parentSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.b_path, parentCommit),
                                                       pa.getStartLine(), pa.getEndLine())
                    parentSnippet = parentSnippet.replace(" ", "")
                    for ch in candidates:
                        childSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.a_path, childCommit),
                                                          ch.getStartLine(), ch.getEndLine())
                        childSnippet = childSnippet.replace(" ", "")
                        if childSnippet == parentSnippet:
                            snippetMatchingInstance.add(ch)
                    if len(snippetMatchingInstance) > 0:
                        for ch in snippetMatchingInstance:
                            candidatesList.append([pa, ch])
                            if ch not in chCandidates:
                                chCandidates.add(ch)
                        paCandidates.add(pa)

                ####location-matching
                edits = utils.getEditList(d)
                locMatchingInstance = findLocBasedMatchingAlarms(pa, untrackedChild, edits)
                if len(locMatchingInstance) > 0:
                    ###Todo:if locMatching Instance>0 -> save as candidates
                    for ch in locMatchingInstance:
                        candidatesList.append([pa,ch])
                        if ch not in chCandidates:
                            chCandidates.add(ch)
                    paCandidates.add(pa)



                paRefactoring = utils.createACopy(pa)
                paRefactoring, isRefactoring, sourceCodePath, refactoringType = utils.getPaRefactoringWihoutOthers(
                    paRefactoring,
                    refactoringInfo)
                ###
                ### 3.Location-based matching.
                ###
                if refactoringType == "MOVE_CLASS" or refactoringType == "MOVE_RENAME_CLASS":
                    continue
                else:
                    locMatchingInstance = findLocBasedMatchingAlarms(paRefactoring, untrackedChild, edits)
                    if len(locMatchingInstance) > 0:

                        ###debug:
                        if isRefactoring:
                            print(f"{childCommit} find refactoring candidates in loc-matching({refactoringType}):\n{pa}\n")

                        for ch in locMatchingInstance:

                            ###debug:
                            if isRefactoring:
                                print(f"pa's candidates in loc-matching:\n{ch}\n")

                            candidatesList.append([pa, ch])
                            if ch not in chCandidates:
                                chCandidates.add(ch)
                        paCandidates.add(pa)

                ###snippet-refactoring
                candidates = set()
                snippetMatchingInstance = set()
                for ch in untrackedChild:
                    if utils.isSameButDiffLoc(paRefactoring, ch):
                        candidates.add(ch)

                if len(candidates) > 0:
                    parentSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.b_path, parentCommit),
                                                       pa.getStartLine(), pa.getEndLine())
                    parentSnippet = parentSnippet.replace(" ", "")

                    for ch in candidates:

                        if isRefactoring:
                            childSnippet = utils.getLineRange(utils.getSourceText(repoPath, sourceCodePath, childCommit),
                                                              ch.getStartLine(), ch.getEndLine())
                            childSnippet = childSnippet.replace(" ", "")

                            if childSnippet == parentSnippet:
                                snippetMatchingInstance.add(ch)

                if len(snippetMatchingInstance) > 0:

                    ###debug:
                    if isRefactoring:
                        print(f"{childCommit} find refactoring candidates in snippet-matching({refactoringType}):\n{pa}\n")
                    for ch in snippetMatchingInstance:
                        ###debug:
                        if isRefactoring:
                            print(f"pa's candidates in snippet-matching:\n{ch}\n")
                        candidatesList.append([pa, ch])
                        if ch not in chCandidates:
                            chCandidates.add(ch)
                    paCandidates.add(pa)


    # if len(paCandidates) > 0:
    #     matchedPaList, matchedChList = hungarianAlgorithm(paCandidates, chCandidates, candidatesList)
    #     untrackedParent = set(untrackedParent) - set(matchedPaList)
    #     untrackedChild = set(untrackedChild) - set(matchedChList)
    # print("After snippet-based matching:")
    # print("the number of untrackedParent", len(untrackedParent))
    # print("the number of untrackedChild", len(untrackedChild))
    # print("\n")

    ####TODO:location matching
    # paCandidates, chCandidates, candidatesList=findLocationCandidates(untrackedParent, untrackedChild, diffMap, parentChangedPaths)
    # #for pairs in candidatesList:
    #     #print(f'{pairs[0]}->{pairs[1]}')
    # if len(paCandidates) > 0:
    #     matchedPaList, matchedChList =hungarianAlgorithm(paCandidates, chCandidates,candidatesList)
    #     untrackedParent = set(untrackedParent) - set(matchedPaList)
    #     untrackedChild = set(untrackedChild) - set(matchedChList)
    # print("After location-based matching:")
    # print("the number of untrackedParent", len(untrackedParent))
    # print("the number of untrackedChild", len(untrackedChild))
    # print("\n")

    # githubPath = githubUrl
    # instance = jClass()
    # refactoringInfo = instance.getRefactoringInfo(repoPath, githubPath, childCommit)
    #
    # paCandidates, chCandidates, candidatesList = findRefactoringLocationCandidates(untrackedParent, untrackedChild, diffMap, parentChangedPaths, refactoringInfo)
    # if len(paCandidates) > 0:
    #     matchedPaList, matchedChList = hungarianAlgorithm(paCandidates, chCandidates, candidatesList)
    #     untrackedParent = set(untrackedParent) - set(matchedPaList)
    #     untrackedChild = set(untrackedChild) - set(matchedChList)
    # print("After refactoring lcoation-based matching:")
    # print("the number of untrackedParent", len(untrackedParent))
    # print("the number of untrackedChild", len(untrackedChild))
    # print("\n")
    #
    # paCandidates, chCandidates, candidatesList = findRefactoringSnippetCandidates(untrackedParent, untrackedChild,
    #                                                                                diffMap, parentChangedPaths,parentCommit,childCommit,
    #                                                                                refactoringInfo)
    # if len(paCandidates) > 0:
    #     matchedPaList, matchedChList = hungarianAlgorithm(paCandidates, chCandidates, candidatesList)
    #     untrackedParent = set(untrackedParent) - set(matchedPaList)
    #     untrackedChild = set(untrackedChild) - set(matchedChList)
    # print("After refactoring snippet-based matching:")
    # print("the number of untrackedParent", len(untrackedParent))
    # print("the number of untrackedChild", len(untrackedChild))
    # print("\n")

    if len(paCandidates) > 0:
        paCandidates = list(paCandidates)
        chCandidates = list(chCandidates)

        matchedPaList, matchedChList = hungarianAlgorithm(paCandidates, chCandidates, candidatesList)
        untrackedParent = set(untrackedParent) - set(matchedPaList)
        untrackedChild = set(untrackedChild) - set(matchedChList)
    print("After matching:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")

    return untrackedChild, untrackedParent

def hungarianAlgorithm(paCandidates, chCandidates,relations): ###relations -> (parentInstance, childInstance)
    matrix =  np.zeros((len(paCandidates),len(chCandidates)),dtype=np.int16)
    matchedPaList, matchedChList = [],[]

    for pair in relations:
        for i in range(len(paCandidates)):
            if paCandidates[i] == pair[0]:
                for j in range(len(chCandidates)):
                    if pair[1] == chCandidates[j]:
                        matrix[i,j] += 1
    matrix.tolist()
    costMatrix = []
    for row in matrix:
        cost_row = []
        for col in row:
            cost_row += [sys.maxsize - col]
        costMatrix += [cost_row]

    ###MUNKRES
    m = Munkres()
    indexes = m.compute(costMatrix)
    #print_matrix(matrix,msg='Lowest cost through this matrix:') ###changed813
    total = 0
    for row, column in indexes:
        value = matrix[row][column]
        total += value
        #print(f'({row},{column}) -> {value}')###changed813
        #print(f'pa:\n{paCandidates[row]}')###changed813
        matchedPaList.append(paCandidates[row])
        #print("->")###changed813
        #print(f'ch:\n{chCandidates[column]}')###changed813
        matchedChList.append(chCandidates[column])
        #print()###changed813
    #print(f'total cost:{total}')###changed813
    return matchedPaList,matchedChList


def findExactMatchingAlarm(pa, childHash):
    output = []
    if pa in childHash:
        output.append(childHash[pa])
    output = set(output)
    return output





def lessThanMATCHING_THRESHOLD(x, matchingEdits, pa):
    childEdits = utils.getOverlappingEditsChild(x.getStartLine(), x.getEndLine(), matchingEdits)

    for i in childEdits:
        ####
        ### check i.start_line
        ####
        # print("parent start",i.parentStart)
        # print("child start",i.childStart)
        # print("pa start",pa.getStartLine())
        # print("ch start", x.getStartLine())
        if abs(abs(int(pa.getStartLine()) - int(i.parentStart)) - abs(
                int(x.getStartLine()) - int(i.childStart))) <= MATCHING_THRESHOLD:
            return True
    return False



###Todo:take location matching
def findLocationCandidates(untrackedParent,untrackedChild,diffMap, parentChangedPaths):
    paCandidates, chCandidates, candidatesList=[],[],[]

    for pa in untrackedParent: ####chenged8.13
        ###
        ### 3.Location-based matching.
        ###
        # print("start location matching")
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True
        if isChanged:
            d = diffMap[mainClassPath]
            if utils.getDiffType(d) == "A" or utils.getDiffType(d) == "D":
                pass
            else:
                edits = utils.getEditList(d)
                locMatchingInstance = findLocBasedMatchingAlarms(pa, untrackedChild, edits)
                if len(locMatchingInstance) > 0:
                    ###Todo:if locMatching Instance>0 -> save as candidates
                    for ch in locMatchingInstance:
                        candidatesList.append([pa,ch])
                        if ch not in chCandidates:
                            chCandidates.append(ch)
                    paCandidates.append(pa)
    return paCandidates, chCandidates, candidatesList


def findLocBasedMatchingAlarms(pa, childBuginstances, edits):
    candidate1 = []
    for ch in childBuginstances:
        if utils.isSameButDiffLoc(pa, ch):
            candidate1.append(ch)
    candidate1 = set(candidate1)
    matchingChild = set()
    ## TODO:if in edits 1.in:... 2. not in and find last edits 3. not in and cannot find last edits.
    if utils.hasEditedParent(int(pa.getStartLine()), int(pa.getEndLine()), edits): ####pa is in diff
        matchingEdits = utils.getOverlappingEditsParent(pa.getStartLine(), pa.getEndLine(), edits)
        candidate2 = set(filter(lambda ch: utils.hasEditedChild(ch.getStartLine(), ch.getEndLine(), matchingEdits),
                                candidate1))  ###changed813
        for ca in candidate2:
            # print(i,'\n')
            if lessThanMATCHING_THRESHOLD(ca, matchingEdits, pa):
                matchingChild.add(ca)
    else: ##pa is not in diff
        minimumEdit = utils.getMinimumEdit(edits)
        if int(pa.getStartLine()) < minimumEdit.parentStart and int(pa.getEndLine()) < minimumEdit.parentStart:### there is no diff before this pa.
            for ca in candidate1:
                if abs(int(ca.getStartLine()) - int(pa.getStartLine())) <= MATCHING_THRESHOLD:
                    matchingChild.add(ca)
        else: ### there is a diff before this pa.
            adjacentEdit = utils.getAdjacentEdit(int(pa.getStartLine()),edits)
            for ca in candidate1:
                if abs(abs(int(pa.getStartLine()) - adjacentEdit.parentEnd) - abs(int(ca.getStartLine()) - adjacentEdit.childEnd)):
                    matchingChild.add(ca)
    return matchingChild

###Todo:take snippet matching
def findSnippetCandidates(untrackedParent, untrackedChild, diffMap,parentChangedPaths,parentCommit,childCommit):
    paCandidates, chCandidates, candidatesList = [], [], []
    for pa in untrackedParent:
        ### 1.take snippet-based matching
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True
        if isChanged:
            d = diffMap[mainClassPath]
            if utils.getDiffType(d) == "A" or utils.getDiffType(d) == "D":
                pass
            else:
                candidates = set()
                snippetMatchingInstance = set()
                for ch in untrackedChild:
                    if utils.isSameButDiffLoc(pa, ch):
                        candidates.add(ch)
                if len(candidates) > 0:
                    parentSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.b_path, parentCommit),
                                                       pa.getStartLine(), pa.getEndLine())
                    parentSnippet = parentSnippet.replace(" ", "")
                    for ch in candidates:
                        childSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.a_path, childCommit),
                                                          ch.getStartLine(), ch.getEndLine())
                        childSnippet = childSnippet.replace(" ", "")
                        if childSnippet == parentSnippet:
                            snippetMatchingInstance.add(ch)
                    if len(snippetMatchingInstance) > 0:
                        for ch in snippetMatchingInstance:
                            candidatesList.append([pa, ch])
                            if ch not in chCandidates:
                                chCandidates.append(ch)
                        paCandidates.append(pa)
    return paCandidates, chCandidates, candidatesList


###Todo:take refactoring snippet matching
def findRefactoringSnippetCandidates(untrackedParent, untrackedChild, diffMap,parentChangedPaths,parentCommit,childCommit,refactoringInfo):
    paCandidates, chCandidates, candidatesList = [], [], []

    for pa in untrackedParent:
        isClassRefactoring = False
        sourceCodePath = ""
        paRefactoring = utils.createACopy(pa)
        paRefactoring, isClassRefactoring, sourceCodePath, refactoringType = utils.getPaRefactoring(paRefactoring,
                                                                                                    refactoringInfo,
                                                                                                    isClassRefactoring)
        ### 1.take refactoring snippet-based matching

        startTime = time.time()
        mainClassPath = str(pa.getSourcePath())
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx

        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True
        if isChanged:
            d = diffMap[mainClassPath]
            candidates = set()
            snippetMatchingInstance = set()
            for ch in untrackedChild:
                if utils.isSameButDiffLoc(paRefactoring, ch):
                    candidates.add(ch)

            if len(candidates) > 0:
                parentSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.b_path, parentCommit),
                                                   pa.getStartLine(), pa.getEndLine())
                parentSnippet = parentSnippet.replace(" ", "")

            for ch in candidates:

                if isClassRefactoring:
                    childSnippet = utils.getLineRange(utils.getSourceText(repoPath, sourceCodePath, childCommit),
                                                      ch.getStartLine(), ch.getEndLine())
                    childSnippet = childSnippet.replace(" ", "")

                    if childSnippet == parentSnippet:
                        snippetMatchingInstance.add(ch)
            if len(snippetMatchingInstance) > 0:
                for ch in snippetMatchingInstance:
                    candidatesList.append([pa, ch])
                    if ch not in chCandidates:
                        chCandidates.append(ch)
                paCandidates.append(pa)
    return paCandidates, chCandidates, candidatesList


if __name__ == "__main__":
    kafkaGithub = "https://github.com/apache/kafka"
    jcloudsGithub = "https://github.com/jclouds/jclouds"

    filenameOnLinux = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/forTest"
    saveResultsPath = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/forTest/Results"
    repoPath = r"/Users/lijunjie/Desktop/Master/testProject/jclouds"
    githubPath = jcloudsGithub

    PMD = xmlreader.PMDReader
    Spotbugs = xmlreader.SpotbugsReader

    parentCommits = ["09cf57101d8b961a32ebc1adc3b1b093c00278b1", "ba868af5534b5d6558b8501cb0f6edcd5116782f"]
    childCommits = ["717a545baa5bbc9ae9c78a29a313898abf2403a7", "a449b24e7dd9d4872b3d729a3c63add5b6033318"]

    ##start JVM
    # jarpath = os.path.join(os.path.abspath('.'),
    #                        r'D:\ThesisProject\findbugsanalysis\FixPatternMining\refactoringJava\out\production\refactoringJava')
    # dependency = os.path.join(os.path.abspath('.'),
    #                           r'D:\ThesisProject\RefactoringMiner\build\distributions\RefactoringMiner-1.0\RefactoringMiner-1.0\lib')

    jarpath = os.path.join(os.path.abspath('.'),
                           r'/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/refactoringJava/out/production/refactoringJava')
    dependency = os.path.join(os.path.abspath('.'),
                              r'/Users/lijunjie/Desktop/Master/AnalysisTools/RefactoringMiner/build/distributions/RefactoringMiner-2.0.2/lib')

    jvmPath = jpype.getDefaultJVMPath()
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarpath, "-Djava.ext.dirs=%s" % dependency)

    jClass = jpype.JClass("edu.concordia.junjie.RefactoringInfo")
    # for i in range(len(parentCommits)):
    for i in range(len(parentCommits)):
        ###Spotbugs
        utils.checkout(repoPath, childCommits[i])




        parentPMDFileName = os.path.join(filenameOnLinux,r"PMD/"+parentCommits[i]+".xml")
        childPMDFileName = os.path.join(filenameOnLinux, r"PMD/" + childCommits[i]+".xml")
        parentSpotbugsFileName = os.path.join(filenameOnLinux, r"Spotbugs/" + parentCommits[i]+".xml")
        childSpotbugsFileName = os.path.join(filenameOnLinux, r"Spotbugs/" + childCommits[i]+".xml")

        startTime = time.time()
        parentBuginstances = Spotbugs(parentSpotbugsFileName)
        childBuginstances = Spotbugs(childSpotbugsFileName)


        endTime = time.time()
        readXMLTime = endTime - startTime

        matchingStartTime = time.time()
        unmatchedChild, unmatchedParent = matchChildParent(repoPath, parentBuginstances, childBuginstances,
                                                           parentCommits[i], childCommits[i], githubPath, jClass)
        matchingEndTime = time.time()

        ##############################
        ### Debug
        ##############################
        print(f"commit:{childCommits[i]}")
        print("spot readXMLTime:", readXMLTime)
        totoalViolationCount = len(parentBuginstances)
        print("spot totoalViolationCount:", totoalViolationCount)
        print("spot totalMatchingTime: ", matchingEndTime - matchingStartTime)
        #
        # print("unchangedExactMatchCount: ",unchangedExactMatchCount)
        # print("unchangedExactMatchTotalTime: ",unchangedExactMatchTotalTime)
        #
        #
        # print("changedExactMatchCount: ", changedExactMatchCount)
        # print("changedExactMatchTotalTime: ", changedExactMatchTotalTime)
        #
        # print("locationBasedCount: ", locationBasedCount)
        # print("locationBasedTotalTime: ", locationBasedTotalTime)
        #
        # print("snippetBasedCount: ", snippetBasedCount)
        # print("snippetBasedTotalTime: ", snippetBasedTotalTime)
        #
        # print("hashBasedCount: ", hashBasedCount)
        # print("hashBasedTotalTime: ", hashBasedTotalTime)
        #
        # print("unmatchedCount: ", unmatchedCount)
        # print("unmatchedTotalTime: ", unmatchedTotalTime)

        ################
        ### write to file
        ################
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
        savePath = os.path.join(saveResultsPath,
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_gone_spotbugs.csv")
        dataframe.to_csv(
            savePath,
            index=False,
            sep=',')

        bugAbbvSetParent = []
        categorySetParent = []
        classSetParent = []
        methodSetParent = []
        fieldSetParent = []
        sourcePathSetParent = []
        startSetParent = []
        endSetParent = []
        for eachUnmatched in unmatchedChild:
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
        savePath = os.path.join(saveResultsPath,
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_new_spotbugs.csv")
        dataframe.to_csv(
            savePath,
            index=False,
            sep=',')

        #####PMD
        utils.checkout(repoPath, childCommits[i])
        # parentFilename = filenameOnLinux + parentCommit+'.xml'
        # childFilename = filenameOnLinux + childCommit+'.xml'



        startTime = time.time()
        parentBuginstances = PMD(parentPMDFileName)
        childBuginstances = PMD(childPMDFileName)

        # parentBuginstances = xmlreader.SpotbugsReader(parentFilename)
        # childBuginstances = xmlreader.SpotbugsReader(childFilename)

        endTime = time.time()
        readXMLTime = endTime - startTime

        matchingStartTime = time.time()
        unmatchedChild, unmatchedParent = matchChildParent(repoPath, parentBuginstances, childBuginstances,
                                                           parentCommits[i], childCommits[i], githubPath, jClass)
        matchingEndTime = time.time()

        ##############################
        ### Debug
        ##############################
        print(f"commit:{childCommits[i]}")
        print("pmd readXMLTime:", readXMLTime)
        totoalViolationCount = len(parentBuginstances)
        print("pmd totoalViolationCount:", totoalViolationCount)
        print("pmd totalMatchingTime: ", matchingEndTime - matchingStartTime)
        #
        # print("unchangedExactMatchCount: ",unchangedExactMatchCount)
        # print("unchangedExactMatchTotalTime: ",unchangedExactMatchTotalTime)
        #
        #
        # print("changedExactMatchCount: ", changedExactMatchCount)
        # print("changedExactMatchTotalTime: ", changedExactMatchTotalTime)
        #
        # print("locationBasedCount: ", locationBasedCount)
        # print("locationBasedTotalTime: ", locationBasedTotalTime)
        #
        # print("snippetBasedCount: ", snippetBasedCount)
        # print("snippetBasedTotalTime: ", snippetBasedTotalTime)
        #
        # print("hashBasedCount: ", hashBasedCount)
        # print("hashBasedTotalTime: ", hashBasedTotalTime)
        #
        # print("unmatchedCount: ", unmatchedCount)
        # print("unmatchedTotalTime: ", unmatchedTotalTime)

        ################
        ### write to file
        ################
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
        savePath = os.path.join(saveResultsPath,
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_gone_pmd.csv")
        dataframe.to_csv(
            savePath,
            index=False,
            sep=',')

        bugAbbvSetParent = []
        categorySetParent = []
        classSetParent = []
        methodSetParent = []
        fieldSetParent = []
        sourcePathSetParent = []
        startSetParent = []
        endSetParent = []
        for eachUnmatched in unmatchedChild:
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
        savePath = os.path.join(saveResultsPath,
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_new_pmd.csv")
        dataframe.to_csv(
            savePath,
            index=False,
            sep=',')

    # shutdown JVM
    jpype.shutdownJVM()