import XMLreader as xmlreader
import jpype
from Utils import Diff
import Utils as utils
import time
import pandas as pd
from io import StringIO
import git
import os
from BugInstance import BugInstance

MATCHING_THRESHOLD = 20
DEBUG = False
TRACK = False
trackBuginstance = BugInstance()

###set tracked buginstance


trackBuginstance.setBugAbbv('SIC_INNER_SHOULD_BE_STATIC_ANON	PERFORMANCE')
trackBuginstance.setCategoryAbbrev('Error Prone')
# trackBuginstance.setPriority('3')
trackBuginstance.setSourcePath('org/jclouds/openstack/nova/v2_0/compute/functions/AllocateAndAddFloatingIpToNode.java')
trackBuginstance.setClass("org.jclouds.openstack.nova.v2_0.compute.functions.AllocateAndAddFloatingIpToNode")
trackBuginstance.setMethod("allocateFloatingIPForNode")
trackBuginstance.setField('')
trackBuginstance.setStartLine('141')
trackBuginstance.setEndLine('141')


##

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
    global DEBUG
    global TRACK
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
        if len(matchedBugInstances) > 1:
            if DEBUG and pa == trackBuginstance:
                print("candidates more than one")
            # print()
            # print("Multiple match!" + matchedby)
            # print("Multiple match:")
            # print("\t Parent:" + pa.getClass() + " in " + parentCommit)
            # for i in matchedBugInstances:
            # print("\t Child:" + i.getClass() + " in " + childCommit)
        ###Todo: take which is not matched already instead of simple head.
        # print("childTracked: ",childTracked,'\n')
        # print("matchedBugInstance: ",matchedBugInstances,'\n')
        untrackedInstances = matchedBugInstances - childTracked
        testUntrackedInstances = []

        if DEBUG and pa == trackBuginstance:
            for instance in untrackedInstances:
                print('untrackedInstances:\n', instance)
            matchedBugInstances = list(matchedBugInstances)
            matchedBugInstances = set(matchedBugInstances)
        if len(untrackedInstances) == 0:
            if DEBUG and TRACK:
                print("no untracked instances")
            a = 1
            # print()
            # print("All candidateds are already matched!" + matchedby)
            # print("All matched!\n" + pa.getClass() + " is in a changed source: " + mainClassName)
            return False

        else:
            ####track childBuginstance
            ### check out whether it is already in tracked alarms.(if it is, exceptional case.)
            if len(untrackedInstances) != len(matchedBugInstances):
                a = 1
                # print()
                # print("Some already matched!" + matchedby)
                # print("Some already matched! \n"+ pa.getClass() + " is in a changed source: " + mainClassName)
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
    childHash = {}
    for ch in childBuginstances:
        childHash[ch] = ch

    for pa in parentBuginstances:
        ##track a violation

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

    for pa in untrackedParent:
        # paRemoveDollar = utils.createARomovedDollarCopy(pa)
        if DEBUG:
            if pa == trackBuginstance:
                TRACK = True
                print("start to track pa in snippet:")
            else:
                TRACK = False
        ### 1.take snippet-based matching
        startTime = time.time()
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True

        if isChanged:
            d = diffMap[mainClassPath]
            if utils.getDiffType(d) == "A" or utils.getDiffType(d) == "D":
                successSnippet = False
            else:
                candidates = set()
                snippetMatchingInstance = set()
                for ch in untrackedChild:
                    # chRemoveDollar = utils.createARomovedDollarCopy(ch)
                    if utils.isSameButDiffLoc(pa, ch) or utils.isSameAlarm(pa, ch):
                        candidates.add(ch)
                if DEBUG and TRACK:
                    print("In snippet approach\ncandidates1:\n")
                    for ca in candidates:
                        print(ca)

                # print("the length of candidates:", len(candidates))
                # snippetMatchingInstance = set()
                # snippetFilterTime = time.time()
                # print("time consumption ofcandidate filter:",snippetFilterTime-snippetStartTime)
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
                            successSnippet = True
                        else:
                            successSnippet = False
                    if len(snippetMatchingInstance) > 0:
                        successSnippet = recordSuccessMatch(pa, snippetMatchingInstance, mainClassPath,
                                                            matchedby="snippet")
                        if successSnippet == True:
                            if DEBUG and TRACK:
                                print("success match in snippet matching")
                                snippetBasedCount = snippetBasedCount + 1
                                endTime = time.time()
                                snippetBasedTotalTime = snippetBasedTotalTime + endTime - startTime
                else:
                    successSnippet = False

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After snippet-based matching:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")

    for pa in untrackedParent:
        ### 2. take exact matching

        startTime = time.time()
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True
        if isChanged:
            ###
            ### 2.Try to find exact matching buginstance in changed files.
            ###
            exactMatches = findExactMatchingAlarm(pa, childHash)
            if len(exactMatches) > 0:
                successExact = recordSuccessMatch(pa, exactMatches, mainClassPath, matchedby="exact")
                if successExact == True:
                    if DEBUG and TRACK:
                        print("success match in changed exact matching")
                    changedExactMatchCount = changedExactMatchCount + 1
                    endTime = time.time()
                    changedExactMatchTotalTime = changedExactMatchTotalTime + endTime - startTime

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After exact matching in changed file:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")


    for pa in untrackedParent:
        ###3.take location matching
        if DEBUG:
            if pa == trackBuginstance:
                TRACK = True
                print("start to track pa in location:")
            else:
                TRACK = False
        ###
        ### 3.Location-based matching.
        ###
        # print("start location matching")
        startTime = time.time()
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True

        if isChanged:
            d = diffMap[mainClassPath]

            if utils.getDiffType(d) == "A" or utils.getDiffType(d) == "D":
                successLocation = False
            else:
                edits = utils.getEditList(d)
                locMatchingInstance = findLocBasedMatchingAlarms(pa, untrackedChild, edits)
                if len(locMatchingInstance) > 0:
                    # print("location-based matching\n")
                    successLoc = recordSuccessMatch(pa, locMatchingInstance, mainClassPath, matchedby="location")
                    # print("match pair:")
                    # print(pa)
                    # for i in locMatchingInstance:
                    # print("childIns:")
                    # print(locMatchingInstance)
                    if successLoc:
                        if DEBUG and TRACK:
                            print("success match in location matching")
                            locationBasedCount = locationBasedCount + 1
                            endTime = time.time()
                            locationBasedTotalTime = locationBasedTotalTime + endTime - startTime

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After location-based matching:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")

    # take refactoring matching

    githubPath = githubUrl
    instance = jClass()
    refactoringInfo = instance.getRefactoringInfo(repoPath, githubPath, childCommit)

    for pa in untrackedParent:
        isClassRefactoring = False
        sourceCodePath = ""
        paRefactoring = utils.createACopy(pa)
        paRefactoring, isClassRefactoring, sourceCodePath, refactoringType = utils.getPaRefactoring(paRefactoring,
                                                                                                    refactoringInfo,
                                                                                                    isClassRefactoring)
        ###take regular matching with paRefactoring and ch



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
            if DEBUG and TRACK:
                for ca in candidates:
                    print("candidates:\n", ca)

            if len(candidates) > 0:
                parentSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.b_path, parentCommit),
                                                   pa.getStartLine(), pa.getEndLine())
                parentSnippet = parentSnippet.replace(" ", "")

            for ch in candidates:

                if isClassRefactoring:
                    childSnippet = utils.getLineRange(utils.getSourceText(repoPath, sourceCodePath, childCommit),
                                                      ch.getStartLine(), ch.getEndLine())
                    childSnippet = childSnippet.replace(" ", "")

                    if DEBUG and TRACK:
                        print("ca's snippet:\n", childSnippet)

                # else:
                #     childSnippet = utils.getLineRange(utils.getSourceText(repoPath, d.a_path, childCommit),
                #                                   ch.getStartLine(), ch.getEndLine())
                #     childSnippet = childSnippet.replace(" ", "")
                #
                #     if DEBUG and TRACK:
                #         print("ca's snippet:\n", childSnippet)

                if childSnippet == parentSnippet:
                    snippetMatchingInstance.add(ch)
                    successSnippet = True
                else:
                    successSnippet = False
            if len(snippetMatchingInstance) > 0:
                successSnippet = recordSuccessMatch(pa, snippetMatchingInstance, mainClassPath,
                                                    matchedby="snippet")
                if successSnippet == True:
                    if DEBUG and TRACK:
                        print("success match in refactoring snippet matching")
                        snippetBasedCount = snippetBasedCount + 1
                        endTime = time.time()
                        snippetBasedTotalTime = snippetBasedTotalTime + endTime - startTime
            else:
                successSnippet = False

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After Refactoring snippet-based matching:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")
    for pa in untrackedParent:
        paRefactoring = utils.createACopy(pa)
        paRefactoring, isClassRefactoring, sourceCodePath, refactoringType = utils.getPaRefactoring(paRefactoring,
                                                                                                    refactoringInfo,
                                                                                                    isClassRefactoring)
        ###take regular matching with paRefactoring and ch

        ### 2. take exact matching
        startTime = time.time()
        mainClassPath = str(paRefactoring.getSourcePath())
        mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx

        ###
        ### 2.Try to find exact matching buginstance in changed files.
        ###

        exactMatches = findExactMatchingAlarm(paRefactoring, childHash)
        if len(exactMatches) > 0:
            successExact = recordSuccessMatch(pa, exactMatches, mainClassPath, matchedby="exact")
            if successExact == True:
                if DEBUG and TRACK:
                    print("success match in changed exact matching")
                changedExactMatchCount = changedExactMatchCount + 1
                endTime = time.time()
                changedExactMatchTotalTime = changedExactMatchTotalTime + endTime - startTime

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After Refactoring exact matching in unchanged file:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")
    for pa in untrackedParent:
        paRefactoring = utils.createACopy(pa)
        paRefactoring, isClassRefactoring, sourceCodePath, refactoringType = utils.getPaRefactoring(paRefactoring,
                                                                                                    refactoringInfo,
                                                                                                    isClassRefactoring)

        ###take regular matching with paRefactoring and ch
        ###3.take location matching
        if DEBUG:
            if pa == trackBuginstance:
                TRACK = True
                print("start to track pa in refactoring location:")
            else:
                TRACK = False
        ###
        ### 3.Location-based matching.
        ###
        # print("start refactoring location matching")
        # track violation

        # startTime = time.time()
        # mainClassPath = str(paRefactoring.getSourcePath())
        # mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx
        if refactoringType == "MOVE_CLASS":
            break


        else:
            mainClassPath = str(pa.getSourcePath())
            mainClassPath = mainClassPath.replace("/", ".")  #####kafka.api.xxx

            isChanged = False
            for path in parentChangedPaths:
                if mainClassPath in path:
                    isChanged = True
            if isChanged:
                d = diffMap[mainClassPath]
                if utils.getDiffType(d) == "A" or utils.getDiffType(d) == "D":
                    successLocation = False

                else:

                    edits = utils.getEditList(d)
                    locMatchingInstance = findLocBasedMatchingAlarms(paRefactoring, untrackedChild, edits)
                    if len(locMatchingInstance) > 0:
                        # print("location-based matching\n")
                        successLoc = recordSuccessMatch(pa, locMatchingInstance, mainClassPath, matchedby="location")
                        # print("match pair:")
                        # print(pa)
                        # for i in locMatchingInstance:
                        # print("childIns:")
                        # print(locMatchingInstance)
                        if successLoc:
                            if DEBUG and TRACK:
                                print("success match in refactoring location matching")
                                locationBasedCount = locationBasedCount + 1
                                endTime = time.time()
                                locationBasedTotalTime = locationBasedTotalTime + endTime - startTime

    untrackedParent = parentBuginstances - parentTracked
    untrackedChild = childBuginstances - childTracked
    print("After Refactoring location-based matching:")
    print("the number of untrackedParent", len(untrackedParent))
    print("the number of untrackedChild", len(untrackedChild))
    print("\n")
    ##

    return untrackedChild, untrackedParent


def findExactMatchingAlarm(pa, childHash):
    output = []
    if pa in childHash:
        output.append(childHash[pa])
    output = set(output)
    return output



def lessThanMATCHING_THRESHOLD(x, matchingEdits, pa):
    global DEBUG
    global TRACK
    childEdits = utils.getOverlappingEditsChild(x.getStartLine(), x.getEndLine(), matchingEdits)
    if DEBUG and TRACK:
        for e in childEdits:
            print("In childEdits:")
            print("parent start:", e.parentStart)
            print("child start:", e.childStart)
            print("pa end:", e.parentEnd)
            print("ch end:", e.childEnd)

    for i in childEdits:
        ####
        ### check i.start_line
        ####
        # print("parent start",i.parentStart)
        # print("child start",i.childStart)
        # print("pa start",pa.getStartLine())
        # print("ch start", x.getStartLine())
        if DEBUG and TRACK:
            print("relevent distance:", abs(
                abs(int(pa.getStartLine()) - int(i.parentStart)) - abs(int(x.getStartLine()) - int(i.childStart))))
        if abs(abs(int(pa.getStartLine()) - int(i.parentStart)) - abs(
                int(x.getStartLine()) - int(i.childStart))) <= MATCHING_THRESHOLD:
            return True
    return False


def findLocBasedMatchingAlarms(pa, childBuginstances, edits):
    global DEBUG
    global TRACK
    candidate1 = []
    # paRemoveDollar = utils.createARomovedDollarCopy(pa)
    for ch in childBuginstances:
        # chRemoveDollar = utils.createARomovedDollarCopy(ch)
        if utils.isSameButDiffLoc(pa, ch):
            candidate1.append(ch)
    candidate1 = set(candidate1)
    if DEBUG and TRACK:
        print("In local matching func:\ncandidates1:")
        for i in candidate1:
            print(i)
    matchingEdits = utils.getOverlappingEditsParent(pa.getStartLine(), pa.getEndLine(), edits)
    if DEBUG and TRACK:
        print("In local matching func:\nmatchingEdits:")
        for e in matchingEdits:
            print("In childEdits:")
            print("parent start:", e.parentStart)
            print("child start:", e.childStart)
            print("pa end:", e.parentEnd)
            print("ch end:", e.childEnd)
        for ch in candidate1:
            print("candidate1 startline and endline: ", ch.getStartLine(), ch.getEndLine())
    candidate2 = set(
        filter(lambda ch: utils.hasEditedChild(ch.getStartLine(), ch.getEndLine(), matchingEdits), candidate1))
    matchingChild = set()
    if DEBUG and TRACK:
        print("In local matching func:\ncandidates2:")
        for i in candidate2:
            print(i)

    for i in candidate2:
        # print(i,'\n')
        if lessThanMATCHING_THRESHOLD(i, matchingEdits, pa):
            matchingChild.add(i)
    return matchingChild


def findLocBasedMatchingAlarmsRemoveDollarMarks(pa, childBuginstances, edits):
    global DEBUG
    global TRACK
    candidate1 = []
    paRemoveDollar = utils.createARomovedDollarCopy(pa)
    for ch in childBuginstances:
        chRemoveDollar = utils.createARomovedDollarCopy(ch)
        if utils.isSameButDiffLoc(paRemoveDollar, chRemoveDollar):
            candidate1.append(ch)
    candidate1 = set(candidate1)
    if DEBUG and TRACK:
        print("In local matching func:\ncandidates1:")
        for i in candidate1:
            print(i)
    matchingEdits = utils.getOverlappingEditsParent(pa.getStartLine(), pa.getEndLine(), edits)
    if DEBUG and TRACK:
        print("In local matching func:\nmatchingEdits:")
        for e in matchingEdits:
            print("In childEdits:")
            print("parent start:", e.parentStart)
            print("child start:", e.childStart)
            print("pa end:", e.parentEnd)
            print("ch end:", e.childEnd)
        for ch in candidate1:
            print("candidate1 startline and endline: ", ch.getStartLine(), ch.getEndLine())
    candidate2 = set(
        filter(lambda ch: utils.hasEditedChild(ch.getStartLine(), ch.getEndLine(), matchingEdits), candidate1))
    matchingChild = set()
    if DEBUG and TRACK:
        print("In local matching func:\ncandidates2:")
        for i in candidate2:
            print(i)

    for i in candidate2:
        # print(i,'\n')
        if lessThanMATCHING_THRESHOLD(i, matchingEdits, pa):
            matchingChild.add(i)
    return matchingChild


if __name__ == "__main__":
    kafkaGithub = "https://github.com/apache/kafka"
    jcloudsGithub = "https://github.com/jclouds/jclouds"
    kafkaPathOnMac = r"/Users/lijunjie/Desktop/Master/testProject/kafka"
    jcloudsPathOnMac = r"/Users/lijunjie/Desktop/Master/testProject/jclouds"
    kafkaPathOnLinux = r"/home/ljj/test/Projects/kafka"
    jcloudsPathOnLinux = r"/home/ljj/test/Projects/jclouds"
    saveResultPathOnMac = r"/Users/lijunjie/Desktop/Master/manual work/testImprove"
    saveResultPathOnLinux = r"/home/ljj/test/tmpResults"

    jcloudsReportNameOnPMDLinux = r"/home/ljj/test/Reports/PMD/jclouds/"
    kafkaReportNameOnSpotbugsLinux = r"/home/ljj/test/Reports/Spotbugs/kafka/"
    jcloudsReportNameOnSpotbugsLinux = r"/home/ljj/test/Reports/Spotbugs/jclouds/"
    kafkaReportNameOnPMDLinux = r"/home/ljj/test/Reports/PMD/kafka/"
    kafkaReportNameOnPMDMac = r"/Users/lijunjie/Desktop/Master/manual work/reports/PMD/kafka"

    filenameOnLinux = r"D:\ThesisProject\trackingData"
    saveResultsPath = r"D:\ThesisProject\trackingData\results\jclouds\improved"
    repoPath = r"D:\ThesisProject\trackingProjects\jclouds"

    # repoPath = kafkaPathOnLinux
    githubPath = jcloudsGithub

    parentCommits = ["2a56db0", "18eb7f3"]
    childCommits = ["09936b5", "dd73410"]

    ##start JVM
    jarpath = os.path.join(os.path.abspath('.'),
                           r'D:\ThesisProject\findbugsanalysis\FixPatternMining\refactoringJava\out\production\refactoringJava')
    dependency = os.path.join(os.path.abspath('.'),
                              r'D:\ThesisProject\RefactoringMiner\build\distributions\RefactoringMiner-1.0\RefactoringMiner-1.0\lib')

    jvmPath = jpype.getDefaultJVMPath()
    if not jpype.isJVMStarted():
        jpype.startJVM(jvmPath, "-ea", "-Djava.class.path=%s" % jarpath, "-Djava.ext.dirs=%s" % dependency)

    jClass = jpype.JClass("edu.concordia.junjie.RefactoringInfo")
    # for i in range(len(parentCommits)):
    for i in range(len(parentCommits)):
        utils.checkout(repoPath, childCommits[i])
        # parentFilename = filenameOnLinux + parentCommit+'.xml'
        # childFilename = filenameOnLinux + childCommit+'.xml'

        parentFilename = filenameOnLinux + '/jclouds/' + parentCommits[i] + 'Spotbugs.xml'  ##CHANGED
        childFilename = filenameOnLinux + '/jclouds/' + childCommits[i] + 'Spotbugs.xml'  ##CHANGED

        startTime = time.time()
        parentBuginstances = xmlreader.SpotbugsReader(parentFilename)
        childBuginstances = xmlreader.SpotbugsReader(childFilename)

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
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_gone_spotbugs_improved.csv")
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
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_new_spotbugs_improved.csv")
        dataframe.to_csv(
            savePath,
            index=False,
            sep=',')

        #####PMD
        utils.checkout(repoPath, childCommits[i])
        # parentFilename = filenameOnLinux + parentCommit+'.xml'
        # childFilename = filenameOnLinux + childCommit+'.xml'

        parentFilename = filenameOnLinux + '/jclouds/' + parentCommits[i] + 'PMD.xml'  ##CHANGED
        childFilename = filenameOnLinux + '/jclouds/' + childCommits[i] + 'PMD.xml'  ##CHANGED

        startTime = time.time()
        parentBuginstances = xmlreader.PMDReader(parentFilename)
        childBuginstances = xmlreader.PMDReader(childFilename)

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
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_gone_pmd_improved.csv")
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
                                parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_new_pmd_improved.csv")
        dataframe.to_csv(
            savePath,
            index=False,
            sep=',')

    # shutdown JVM
    jpype.shutdownJVM()

