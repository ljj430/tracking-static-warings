import XMLreader as xmlreader
from Utils import Diff
import Utils as utils
import time
import pandas as pd
from io import StringIO
import git
from BugInstance import BugInstance
import MatchedPairsCollector
import csv
import os

MATCHING_THRESHOLD = 20
DEBUG = False
TRACK = False
trackBuginstance=BugInstance()


###set tracked buginstance
###set tracked buginstance
trackBuginstance.setBugAbbv('BeanMembersShouldSerialize')
trackBuginstance.setCategoryAbbrev('Error Prone')
trackBuginstance.setPriority('3')
trackBuginstance.setSourcePath('org/jclouds/profitbricks/http/parser/state/GetProvisioningStateResponseHandlerTest.java')
trackBuginstance.setClass('GetProvisioningStateResponseHandlerTest$GetProvisioningStateResponseHandlerTest')
trackBuginstance.setField('sampleResponses')
trackBuginstance.setStartLine('51')
trackBuginstance.setEndLine('51')

def splitDollarMark(className):
    token=className.split("$")
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





def matchChildParent(repoPath,parentBuginstances,childBuginstances, parentCommit,childCommit):
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
    utils.checkout(repoPath,childCommit)
    ###initial
    parentTracked = []
    parentTracked = set(parentTracked)
    childTracked = []
    childTracked = set(childTracked)
    unmatchedParent = set()
    matchedPairs = []
    trackingMap = {}
    ### Diff object
    diff = Diff(repoPath)
    ###parentChangedPaths is a list that contains the package path + class name of each parent changed file
    ### diffMap is a dic (a path -> a diff object)
    ###path: kafka.common.xxx.java/scala
    ####the diffMap's key is a path org.apache.kafka.clients.st.java. the value is a diff object
    ##### parentChangedPaths list is a list that saves diffMap's key
    parentChangedPaths, childChangedPaths, diffMap = \
        utils.transformFilesToPackagePaths(diff,parentCommit,childCommit,repoPath)

    #mapParentPath = utils.createMapPath(kafkaPath, parentCommit)
    #mapchildPath = utils.createMapPath(kafkaPath, childCommit)
    ###inline functions
    def recordSuccessMatch(pa,matchedBugInstances, mainClassName, matchedby):
        if len(matchedBugInstances)>1:
            if DEBUG and TRACK:
                print("candidates more than one")
            #print()
            #print("Multiple match!" + matchedby)
            #print("Multiple match:")
            #print("\t Parent:" + pa.getClass() + " in " + parentCommit)
            #for i in matchedBugInstances:
                #print("\t Child:" + i.getClass() + " in " + childCommit)
        ###Todo: take which is not matched already instead of simple head.
        #print("childTracked: ",childTracked,'\n')
        #print("matchedBugInstance: ",matchedBugInstances,'\n')
        untrackedInstances = matchedBugInstances - childTracked
        if DEBUG and TRACK:
            for instance in untrackedInstances:
                print('untrackedInstances:\n',instance)
            matchedBugInstances = list(matchedBugInstances)
            if matchedBugInstances[0] in childTracked:
                print("childBuginstance has been in childTracked")
            matchedBugInstances = set(matchedBugInstances)

        if len(untrackedInstances) == 0:
            if DEBUG and TRACK:
                print("no untracked instances")
            a=1
            #print()
            #print("All candidateds are already matched!" + matchedby)
            #print("All matched!\n" + pa.getClass() + " is in a changed source: " + mainClassName)
            return False

        else :
            ####track childBuginstance
            if DEBUG:
                matchedBugInstances = list(matchedBugInstances)
                if matchedBugInstances[0] == trackBuginstance:
                    print("childBugInstance that is same with trackedins has been tracked:")
                    print(matchedby)
                    print("matched pa is:")
                    print(pa)
                matchedBugInstances = set(matchedBugInstances)
            ### check out whether it is already in tracked alarms.(if it is, exceptional case.)
            if len(untrackedInstances) != len(matchedBugInstances):
                a=1
                #print()
                #print("Some already matched!" + matchedby)
                #print("Some already matched! \n"+ pa.getClass() + " is in a changed source: " + mainClassName)
            matchedChild = list(untrackedInstances)[0]  #assuming there are one single match.
            parentTracked.add(pa)
            childTracked.add(matchedChild)
            matchedPairs.append([pa,matchedChild])
            #print(pa)
            trackingMap[pa] = matchedChild
            return True ##matched

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
        ###time evaluation
        startTime = time.time()


        ###
        ### 0.find out whether it is in changed set
        ###
        mainClassPath = pa.getSourcePath()
        mainClassPath = mainClassPath.replace("/", ".")#####kafka.api.xxx
        isChanged = False
        for path in parentChangedPaths:
            if mainClassPath in path:
                isChanged = True
        if  not isChanged: ###if not in changed  ##mainClassPath is like kafka.common.xxx.java
            ###
            ### 1.Try to find matching bugInstance in child alarm set
            ### (only one method available since it is in the unchanged set).
            ### exact matching in non-changed set.
            ###
            #print("start to match changed file")
            successAny = findExactMatching(pa,mainClassPath)
            if successAny == True:
                unchangedExactMatchCount = unchangedExactMatchCount + 1
                endTime = time.time()
                unchangedExactMatchTotalTime = unchangedExactMatchTotalTime + endTime - startTime
        else:
            ###
            ### 2.Try to find exact matching buginstance in changed files.
            ###
            exactMatches = findExactMatchingAlarm(pa, childHash)
            if len(exactMatches) > 0:
                successExact = recordSuccessMatch(pa,exactMatches,mainClassPath,matchedby = "exact")
                if successExact == True:
                    if DEBUG and TRACK:
                        print("success match in changed exact matching")
                    changedExactMatchCount = changedExactMatchCount + 1
                    endTime = time.time()
                    changedExactMatchTotalTime = changedExactMatchTotalTime + endTime - startTime
            else:
                successExact = False
            if not successExact:
                ###
                ### 3.Location-based matching.
                ###
                #print("start location matching")
                d = diffMap[mainClassPath]
                edits = utils.getEditList(d)
                locMatchingInstance = findLocBasedMatchingAlarms(pa, childBuginstances, edits)
                if len(locMatchingInstance) > 0:
                    #print("location-based matching\n")

                    successLoc = recordSuccessMatch(pa, locMatchingInstance, mainClassPath, matchedby="location")
                    if successLoc == True:
                        if DEBUG and TRACK:
                            print("success match in location matching")
                        locationBasedCount = locationBasedCount + 1
                        endTime = time.time()
                        locationBasedTotalTime = locationBasedTotalTime + endTime - startTime
                else:
                    successLoc = False
            else:
                successLoc = True

            if not successLoc:
                ### 4. snippet-based matching: in case of moving
                d = diffMap[mainClassPath]
                if utils.getDiffType(d) == "D":
                    successSnippet = False
                else:

                    #print("start to snippet match:")
                    #snippetStartTime = time.time()
                    #print("pa instance:",pa)
                    #edits = utils.getEditList(d)
                    #parentMatchingEdits = utils.getOverlappingEditsParent(pa.getStartLine(),pa.getEndLine(),edits)

                    parentSnippet = utils.getLineRange(utils.getSourceText(repoPath,d.b_path,parentCommit),pa.getStartLine(),pa.getEndLine())
                    candidates =set()
                    for ch in childBuginstances:
                        if utils.isSameButDiffLoc(pa,ch):##changed
                            candidates.add(ch)
                    #if DEBUG and TRACK:
                        #print("In snippet approach\ncandidates1:\n",candidates)
                    #print("the length of candidates:", len(candidates))
                    snippetMatchingInstance = set()
                    #snippetFilterTime = time.time()
                    #print("time consumption ofcandidate filter:",snippetFilterTime-snippetStartTime)
                    if True:
                        for ch in candidates:
                            childSnippet = utils.getLineRange(utils.getSourceText(repoPath,d.a_path,childCommit),ch.getStartLine(),ch.getEndLine())

                            if childSnippet == parentSnippet:
                                snippetMatchingInstance.add(ch)
                                successSnippet = True
                            else:
                                successSnippet = False

                    #####
                    # if len(parentMatchingEdits) > 0:
                    #     #print("parentMatchingEdits>0")
                    #     snippetMatchingInstance = set()
                    #     for ch in candidates:
                    #         childMatchingEdits = utils.getOverlappingEditsChild(ch.getStartLine(),ch.getEndLine(),parentMatchingEdits)
                    #         if len(childMatchingEdits) > 0:
                    #             childSnippet = utils.getLineRange(utils.getSourceText(repoPath,d.b_path,childCommit),ch.getStartLine(),ch.getEndLine())
                    #             if childSnippet == parentSnippet:
                    #                 snippetMatchingInstance.add(ch)
                    #                 successSnippet = True
                    #             else:
                    #                 successSnippet = False
                        #matchingTime = time.time()
                        #print("matchingTime:", matchingTime - snippetFilterTime)
                        if len(snippetMatchingInstance) > 0 :

                            #print("snippet-based matching\n")
                            #print("snippet-based instance:", pa)
                            successSnippet = recordSuccessMatch(pa, snippetMatchingInstance, mainClassPath, matchedby = "snippet")
                            if successSnippet == True:
                                if DEBUG and TRACK:
                                    print("success match in snippet matching")
                                snippetBasedCount = snippetBasedCount + 1
                                endTime = time.time()
                                snippetBasedTotalTime = snippetBasedTotalTime + endTime - startTime
                        else:
                            successSnippet = False
            else:
                successSnippet = True

            if not successSnippet:
                #### 5. hash-based matching
                d = diffMap[mainClassPath]
                if utils.getDiffType(d) == 'D':
                    successHash = False
                elif d.a_path is None:
                    successHash = False
                else:
                    parentSnippet = utils.getLineRange(utils.getSourceText(repoPath,d.b_path,parentCommit), pa.getStartLine(),pa.getEndLine())
                    candidates = set()
                    for ch in childBuginstances:
                        if utils.isSameTypeAlarm(pa,ch):
                            candidates.add(ch)

                    childSource = utils.getSourceText(repoPath,d.a_path,childCommit)
                    parentTokens = parentSnippet.split()
                    if len(parentTokens)<= utils.HASH_SIZE:
                        successHash = False
                    else:
                        parentHeadHash = utils.hashFirstTokens(utils.HASH_SIZE, parentTokens)
                        parentTailHash = utils.hashLastTokens(utils.HASH_SIZE, parentTokens)
                        hashMatchingInstance = set()
                        for ca in candidates:
                            childSnippet = utils.getLineRange(childSource,ch.getStartLine(),ch.getEndLine())
                            childTokens = childSnippet.split()
                            childHeadHash = utils.hashFirstTokens(utils.HASH_SIZE, childTokens)
                            childTailHash = utils.hashLastTokens(utils.HASH_SIZE, childTokens)
                            if parentHeadHash == childHeadHash or parentTailHash == childTailHash:

                                hashMatchingInstance.add(ca)
                        if len(hashMatchingInstance) >0:
                            #print("hash-based matching\n")
                            #print("hash-base instance:", pa)
                            successHash = recordSuccessMatch(pa,hashMatchingInstance,mainClassPath,matchedby = "hash")
                            if successHash == True:
                                hashBasedCount = hashBasedCount + 1
                                endTime = time.time()
                                hashBasedTotalTime = hashBasedTotalTime + endTime - startTime
                        else :

                            successHash = False
            else:
                successHash = True
            successAny = successHash
        if not successAny:
            if DEBUG and TRACK:
                print("this violation is unmatched")
            unmatchedCount = unmatchedCount + 1
            endTime = time.time()
            unmatchedTotalTime = unmatchedTotalTime + endTime - startTime

            if mainClassPath in diffMap.keys():
                diff = diffMap[mainClassPath]
                if utils.getDiffType(diff) == 'D':
                    report = "disappeared"
                else:
                    report = "fixed"
            else:
                report = "unknown"
            ###print unmatched
            if DEBUG and TRACK:
                print("\nunmatched:")
                print(pa)
                print('Report:'+report+'\n')


            #parentTracked.add(pa)
            unmatchedParent.add(pa)
    time.sleep(0.01)
    untrackedChild = childBuginstances - childTracked
    untrackedParent = parentBuginstances - parentTracked
    return untrackedChild, untrackedParent,matchedPairs

def findExactMatchingAlarm(pa, childHash):
    output = []
    if pa in childHash:
        output.append(childHash[pa])
    output = set(output)
    return output

def lessThanMATCHING_THRESHOLD(x, matchingEdits , pa):
    childEdits = utils.getOverlappingEditsChild(x.getStartLine(),x.getEndLine(), matchingEdits)
    #print("childEdits:\n")
    #print(i for i in childEdits)
    for i in childEdits:
        ####
        ### check i.start_line
        ####
        #print("parent start",i.parentStart)
        #print("child start",i.childStart)
        #print("pa start",pa.getStartLine())
        #print("ch start", x.getStartLine())
        if abs(abs(int(pa.getStartLine()) - int(i.parentStart)) - abs(int(x.getStartLine()) - int(i.childStart))) <= MATCHING_THRESHOLD:
            return True
    return False

def findLocBasedMatchingAlarms(pa, childBuginstances, edits):
    global DEBUG
    global TRACK
    candidate1 = set(filter(lambda ch:utils.isSameButDiffLoc(pa,ch), childBuginstances))
    if DEBUG and TRACK:
        print("In local matching func:\ncandidates1\n:")
        for i in candidate1:
            print(i)
    matchingEdits = utils.getOverlappingEditsParent(pa.getStartLine(),pa.getEndLine(), edits)
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
    candidate2 = set(filter(lambda ch:utils.hasEditedChild(ch.getStartLine(), ch.getEndLine(), matchingEdits), candidate1))
    matchingChild = set()
    if DEBUG and TRACK:
        print("In local matching func:\ncandidates2\n:",candidate2)

    for i in candidate2:
        #print(i,'\n')
        if lessThanMATCHING_THRESHOLD(i, matchingEdits , pa):
            matchingChild.add(i)
    return matchingChild

def oldMatchChildParent(repoPath,parentBuginstances,childBuginstances, parentCommit,childCommit):
    unmatchedParent =   parentBuginstances - childBuginstances
    unmatchedChild =   childBuginstances - parentBuginstances
    return unmatchedChild , unmatchedParent





if __name__ == "__main__":
    kafkaGithub = "https://github.com/apache/kafka"
    jcloudsGithub = "https://github.com/jclouds/jclouds"
    kafkaPathOnMac = r"/Users/lijunjie/Desktop/Master/testProject/kafka"
    jcloudsPathOnMac = r"/Users/lijunjie/Desktop/Master/testProject/jclouds"
    kafkaPathOnLinux = r"/home/ljj/test/Projects/kafka"
    jcloudsPathOnLinux = r"/home/ljj/test/Projects/jclouds"
    saveResultPathOnMac = r"/Users/lijunjie/Desktop/Master/manual work/testImprove"
    saveResultPathOnLinux = r"/home/ljj/test/tmpOriginalAlgorithm"

    jcloudsReportNameOnPMDLinux = r"/home/ljj/test/Reports/PMD/jclouds/"
    kafkaReportNameOnSpotbugsLinux = r"/home/ljj/test/Reports/Spotbugs/kafka/"
    jcloudsReportNameOnSpotbugsLinux = r"/home/ljj/test/Reports/Spotbugs/jclouds/"
    kafkaReportNameOnPMDLinux = r"/home/ljj/test/Reports/PMD/kafka/"



    kafkaReportNameOnPMDMac = r"/Users/lijunjie/Desktop/Master/manual work/reports/PMD/kafka"
    jcloudsReportNameOnPMDMac = r"/Users/lijunjie/Desktop/Master/manual work/reports/PMD/jclouds"
    kafkaReportNameOnSpotbugsMac = r"/Users/lijunjie/Desktop/Master/manual work/reports/Spotbugs/kafka"
    jcloudsReportNameOnSpotbugsMac = r"/Users/lijunjie/Desktop/Master/manual work/reports/Spotbugs/jclouds"
    filenameOnMac = kafkaReportNameOnPMDMac


    saveTmpResultPathOnMac = r"/Users/lijunjie/Desktop/Master/manual work/tmpOriginal"
    saveNewApproachPath = saveTmpResultPathOnMac  ###CHANGED


    filenameOnLinux = r"D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\forTest"
    saveResultsPath = r"D:\ThesisProject\trackingData\results\jclouds\original"
    repoPath = r"D:\ThesisProject\trackingProjects\spring-boot"

    # repoPath = kafkaPathOnLinux
    githubPath = jcloudsGithub

    parentCommits = ["0de466e06efd8617ed00d4f6a54d5311464d1d3a"]
    childCommits = ["07fb4b065d9be6f6ade37e1878ef7a57ee10bf1f"]

    jarOnLinux = r'/home/ljj/test/findbugsanalysis/FixPatternMining/refactoringJava/out/production/refactoringJava'
    depenOnLinux = '/home/ljj/test/findbugsanalysis/FixPatternMining/RefactoringMiner/build/distributions/RefactoringMiner-1.0/lib'
    jarOnMac = r'/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/refactoringJava/out/production/refactoringJava'
    depenOnMac = r'/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/RefactoringMiner/build/distributions/RefactoringMiner-1.0/lib'



    for i in range(len(parentCommits)):
        utils.checkout(repoPath, childCommits[i])
        # parentFilename = filenameOnLinux + parentCommit+'.xml'
        # childFilename = filenameOnLinux + childCommit+'.xml'

        parentFilename = os.path.join(filenameOnLinux , parentCommits[i] + '.xml')  ##CHANGED
        childFilename = os.path.join(filenameOnLinux  , childCommits[i] + '.xml')  ##CHANGED


        parentBuginstances = xmlreader.PMDReader(parentFilename)
        childBuginstances = xmlreader.PMDReader(childFilename)

        # parentBuginstances = xmlreader.SpotbugsReader(parentFilename)
        # childBuginstances = xmlreader.SpotbugsReader(childFilename)

        matchingStartTime = time.time()
        unmatchedChild, unmatchedParent,matchedPairs = matchChildParent(repoPath, parentBuginstances, childBuginstances,
                                                           parentCommits[i], childCommits[i])


        matchingEndTime = time.time()
        print(f"commit:{childCommits[i]}")
        totoalViolationCount = len(parentBuginstances)
        print("SPOT totoalViolationCount:", totoalViolationCount)
        print("SPOT totalMatchingTime: ", matchingEndTime - matchingStartTime)
        print(f"parent warnings:{len(parentBuginstances)}\nchild warnings:{len(childBuginstances)}")
        print(f"unmatchd parent warnings:{len(unmatchedParent)}")
        print(f"unmatchd child warnings:{len(unmatchedChild)}")
    #
        print("unchangedExactMatchCount: ",unchangedExactMatchCount)
    # print("unchangedExactMatchTotalTime: ",unchangedExactMatchTotalTime)
    #
    #
        print("changedExactMatchCount: ", changedExactMatchCount)
    # print("changedExactMatchTotalTime: ", changedExactMatchTotalTime)
    #
        print("locationBasedCount: ", locationBasedCount)
    # print("locationBasedTotalTime: ", locationBasedTotalTime)
    #
        print("snippetBasedCount: ", snippetBasedCount)
    # print("snippetBasedTotalTime: ", snippetBasedTotalTime)
    #
        print("hashBasedCount: ", hashBasedCount)
    # print("hashBasedTotalTime: ", hashBasedTotalTime)
    #
    # print("unmatchedCount: ", unmatchedCount)
    # print("unmatchedTotalTime: ", unmatchedTotalTime)

        #MatchedPairsCollector.wrtieToXML(matchedPairs,r'D:\ThesisData\tmp\1.xml')
        # row = [childCommits[i],matchingEndTime - matchingStartTime]
        # with open(r'xxx/TimeMeasurment.csv','a',newline='') as f:
        #     fieldnames = ['Commit', 'Time']
        #     writer = csv.DictWriter(f, fieldnames=fieldnames)
        #     writer.writerow({'Commit':row[0],'Time':row[1]})

        ###SPOT write to file
        # bugAbbvSetParent = []
        # categorySetParent = []
        # classSetParent = []
        # methodSetParent = []
        # fieldSetParent = []
        # sourcePathSetParent = []
        # startSetParent = []
        # endSetParent = []
        # for eachUnmatched in unmatchedParent:
        #     bugAbbvSetParent.append(eachUnmatched.getBugAbbv())
        #     categorySetParent.append(eachUnmatched.getCategoryAbbrev())
        #     classSetParent.append(eachUnmatched.getClass())
        #     methodSetParent.append(eachUnmatched.getMethod())
        #     fieldSetParent.append(eachUnmatched.getField())
        #     sourcePathSetParent.append(eachUnmatched.getSourcePath())
        #     startSetParent.append(eachUnmatched.getStartLine())
        #     endSetParent.append(eachUnmatched.getEndLine())
        #
        # dataframe = pd.DataFrame(
        #         {'Bug': bugAbbvSetParent, 'category': categorySetParent, "class name": classSetParent,
        #          "method name": methodSetParent,"field name":  fieldSetParent,"source path":sourcePathSetParent,
        #          "start":startSetParent,"end":endSetParent})
        #     #
        #
        # dataframe.to_csv(saveResultsPath + "/" + parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_gone_Spotbugs_original.csv", index=False,sep=',')
        #
        # #
        # #
        # #
        # #
        # bugAbbvSetChild = []
        # categorySetChild = []
        # classSetChild = []
        # methodSetChild = []
        # fieldSetChild = []
        # sourcePathSetChild = []
        # startSetChild = []
        # endSetChild = []
        # for eachUnmatched in unmatchedChild:
        #     bugAbbvSetChild.append(eachUnmatched.getBugAbbv())
        #     categorySetChild.append(eachUnmatched.getCategoryAbbrev())
        #     classSetChild.append(eachUnmatched.getClass())
        #     methodSetChild.append(eachUnmatched.getMethod())
        #     fieldSetChild.append(eachUnmatched.getField())
        #     sourcePathSetChild.append(eachUnmatched.getSourcePath())
        #     startSetChild.append(eachUnmatched.getStartLine())
        #     endSetChild.append(eachUnmatched.getEndLine())
        #
        # dataframe = pd.DataFrame(
        #         {'Bug': bugAbbvSetChild, 'category': categorySetChild, "class name": classSetChild,\
        #          "method name": methodSetChild,"field name":  fieldSetChild,"source path":sourcePathSetChild,\
        #          "start":startSetChild,"end":endSetChild})
        # dataframe.to_csv(saveResultsPath + "/" + parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_new_Spotbugs_original.csv", index=False,sep=',')




        #########
        ###PMD###
        #########

        # utils.checkout(repoPath, childCommits[i])
        # # parentFilename = filenameOnLinux + parentCommit+'.xml'
        # # childFilename = filenameOnLinux + childCommit+'.xml'
        #
        # parentFilename = filenameOnLinux + '/jclouds/' + parentCommits[i] + 'PMD.xml'  ##CHANGED
        # childFilename = filenameOnLinux + '/jclouds/' + childCommits[i] + 'PMD.xml'  ##CHANGED
        #
        # startTime = time.time()
        # parentBuginstances = xmlreader.PMDReader(parentFilename)
        # childBuginstances = xmlreader.PMDReader(childFilename)
        #
        # # parentBuginstances = xmlreader.SpotbugsReader(parentFilename)
        # # childBuginstances = xmlreader.SpotbugsReader(childFilename)
        #
        # endTime = time.time()
        # readXMLTime = endTime - startTime
        #
        # matchingStartTime = time.time()
        # unmatchedChild, unmatchedParent = matchChildParent(repoPath, parentBuginstances, childBuginstances,
        #                                                    parentCommits[i], childCommits[i])
        #
        # matchingEndTime = time.time()
        # print(f"commit:{childCommits[i]}")
        # print("PMD readXMLTime:", readXMLTime)
        # totoalViolationCount = len(parentBuginstances)
        # print("PMD totoalViolationCount:", totoalViolationCount)
        # print("PMD totalMatchingTime: ", matchingEndTime - matchingStartTime)
        # print(f"parent warnings:{len(parentBuginstances)}\nchild warnings:{len(childBuginstances)}")
        # print(f"unmatchd parent warnings:{len(unmatchedParent)}")
        # print(f"unmatchd child warnings:{len(unmatchedChild)}")
        # #
        # print("unchangedExactMatchCount: ",unchangedExactMatchCount)
        # # print("unchangedExactMatchTotalTime: ",unchangedExactMatchTotalTime)
        # #
        # #
        # print("changedExactMatchCount: ", changedExactMatchCount)
        # # print("changedExactMatchTotalTime: ", changedExactMatchTotalTime)
        # #
        # print("locationBasedCount: ", locationBasedCount)
        # # print("locationBasedTotalTime: ", locationBasedTotalTime)
        # #
        # print("snippetBasedCount: ", snippetBasedCount)
        # # print("snippetBasedTotalTime: ", snippetBasedTotalTime)
        # #
        # print("hashBasedCount: ", hashBasedCount)
        # # print("hashBasedTotalTime: ", hashBasedTotalTime)
        # #
        # # print("unmatchedCount: ", unmatchedCount)
        # # print("unmatchedTotalTime: ", unmatchedTotalTime)
        #
        # #
        # bugAbbvSetParent = []
        # categorySetParent = []
        # classSetParent = []
        # methodSetParent = []
        # fieldSetParent = []
        # sourcePathSetParent = []
        # startSetParent = []
        # endSetParent = []
        # for eachUnmatched in unmatchedParent:
        #     bugAbbvSetParent.append(eachUnmatched.getBugAbbv())
        #     categorySetParent.append(eachUnmatched.getCategoryAbbrev())
        #     classSetParent.append(eachUnmatched.getClass())
        #     methodSetParent.append(eachUnmatched.getMethod())
        #     fieldSetParent.append(eachUnmatched.getField())
        #     sourcePathSetParent.append(eachUnmatched.getSourcePath())
        #     startSetParent.append(eachUnmatched.getStartLine())
        #     endSetParent.append(eachUnmatched.getEndLine())
        #
        # dataframe = pd.DataFrame(
        #     {'Bug': bugAbbvSetParent, 'category': categorySetParent, "class name": classSetParent,
        #      "method name": methodSetParent, "field name": fieldSetParent, "source path": sourcePathSetParent,
        #      "start": startSetParent, "end": endSetParent})
        # #
        #
        # dataframe.to_csv(
        #     saveResultsPath + "/" + parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_gone_PMD_original.csv",
        #     index=False,
        #     sep=',')
        #
        # #
        # #
        # #
        # #
        # bugAbbvSetChild = []
        # categorySetChild = []
        # classSetChild = []
        # methodSetChild = []
        # fieldSetChild = []
        # sourcePathSetChild = []
        # startSetChild = []
        # endSetChild = []
        # for eachUnmatched in unmatchedChild:
        #     bugAbbvSetChild.append(eachUnmatched.getBugAbbv())
        #     categorySetChild.append(eachUnmatched.getCategoryAbbrev())
        #     classSetChild.append(eachUnmatched.getClass())
        #     methodSetChild.append(eachUnmatched.getMethod())
        #     fieldSetChild.append(eachUnmatched.getField())
        #     sourcePathSetChild.append(eachUnmatched.getSourcePath())
        #     startSetChild.append(eachUnmatched.getStartLine())
        #     endSetChild.append(eachUnmatched.getEndLine())
        #
        # dataframe = pd.DataFrame(
        #     {'Bug': bugAbbvSetChild, 'category': categorySetChild, "class name": classSetChild,
        #      "method name": methodSetChild, "field name": fieldSetChild, "source path": sourcePathSetChild,
        #      "start": startSetChild, "end": endSetChild})
        # dataframe.to_csv(
        #     saveResultsPath + "/" + parentCommits[i][0:7] + "_" + childCommits[i][0:7] + "_new_PMD_original.csv",
        #     index=False,
        #     sep=',')

