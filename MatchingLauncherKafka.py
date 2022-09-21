import csv
import time
import MatcherOriginal
import XMLreader as xmlreader
import os
import pandas as pd

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
saveKafkaPMDReportsPathOnWin = r'D:\ThesisData\Reports\PMD\kafka'
saveKafkaSpotbugsReportsPathOnWin = r'D:\ThesisData\kafkaSpotbugsReports9.27'
saveKafkaPMDResultsPathOnWin = r'D:\ThesisData\OriginalResults\PMD\kafka'
#saveKafkaSpotbugsResultsPathOnWin = r'D:\ThesisData\OriginalResults\Spotbugs\kafka'
saveKafkaSpotbugsResultsPathOnWin =r'D:\ThesisData\kafkaSpotbugsResults10.13'

commitListPathOnWin2000 = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Kafka2000commitList.txt'
commitListPathOnWinPMD = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\kafka_PMD.txt'
commitListPathOnWinSpotbugs = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\kafka_Spotbugs.txt'
projectPathOnWin = r'D:\ThesisProject\trackingProjects\kafka'

PMD = xmlreader.PMDReader
Spotbugs = xmlreader.SpotbugsReader





if __name__ == "__main__":
    # if not os.path.exists(saveResultPath):
    #     os.system('mkdir ' + saveResultPath)
    f = open(commitListPathOnWinPMD)
    commitList = f.readlines()

    goneResultsPath = os.path.join(saveKafkaPMDResultsPathOnWin,'gone')
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
    if not os.path.exists(r"D:\ThesisData\TimeMeasurment\Original\PMD\kafka\TimeMeasurment.csv"):
        with open(r"D:\ThesisData\TimeMeasurment\Original\PMD\kafka\TimeMeasurment.csv", "w") as csvfile:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    if not os.path.exists(r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\kafka\TimeMeasurment.csv"):
        with open(r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\kafka\TimeMeasurment.csv", "w") as csvfile:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    count = 1
    ###start to track PMD
    # for line in commitList:
    #     line = line.replace('\n', '')
    #     lines = line.split('_')
    #     parentCommit = commitDic2000[lines[0]]
    #     childCommit = commitDic2000[lines[1]]
    #
    #
    #     flag = False
    #     for name in fNewList:
    #         if parentCommit[0:7] + "_" + childCommit[0:7]+ "_gone_warnings.csv" == name:
    #             flag = True
    #     if flag:
    #         count += 1
    #         print(f"commit {childCommit} exsits")
    #         continue
    #     resultParent = os.path.join(saveKafkaPMDReportsPathOnWin, parentCommit[0:7] + '.xml')
    #     resultChild = os.path.join(saveKafkaPMDReportsPathOnWin, childCommit[0:7] + '.xml')
    #
    #     childFilename = resultChild
    #     parentFilename = resultParent
    #     parentBuginstances = PMD(parentFilename)
    #     childBuginstances = PMD(childFilename)
    #
    #     repoPath = projectPathOnWin
    #
    #     matchingStartTime = time.time()
    #     unmatchedChild, unmatchedParent, matchedPairs = MatcherOriginal.matchChildParent(repoPath,parentBuginstances,childBuginstances, parentCommit,childCommit)
    #     matchingEndTime = time.time()
    #
    #
    #     bugAbbvSetParent = []
    #     categorySetParent = []
    #     classSetParent = []
    #     methodSetParent = []
    #     fieldSetParent = []
    #     sourcePathSetParent = []
    #     startSetParent = []
    #     endSetParent = []
    #     for eachUnmatched in unmatchedParent:
    #         bugAbbvSetParent.append(eachUnmatched.getBugAbbv())
    #         categorySetParent.append(eachUnmatched.getCategoryAbbrev())
    #         classSetParent.append(eachUnmatched.getClass())
    #         methodSetParent.append(eachUnmatched.getMethod())
    #         fieldSetParent.append(eachUnmatched.getField())
    #         sourcePathSetParent.append(eachUnmatched.getSourcePath())
    #         startSetParent.append(eachUnmatched.getStartLine())
    #         endSetParent.append(eachUnmatched.getEndLine())
    #
    #     dataframe = pd.DataFrame(
    #         {'Bug': bugAbbvSetParent, 'category': categorySetParent, "class name": classSetParent,
    #          "method name": methodSetParent,"field name":  fieldSetParent,"source path":sourcePathSetParent,
    #          "start":startSetParent,"end":endSetParent})
    #
    #
    #     saveGoneResults = os.path.join(saveKafkaPMDResultsPathOnWin,'gone')
    #     dataframe.to_csv(os.path.join(saveGoneResults,parentCommit[0:7] + "_" + childCommit[0:7] + "_gone_warnings.csv"), index=False,
    #                      sep=',')
    #
    #
    #
    #
    #     bugAbbvSetChild = []
    #     categorySetChild = []
    #     classSetChild = []
    #     methodSetChild = []
    #     fieldSetChild = []
    #     sourcePathSetChild = []
    #     startSetChild = []
    #     endSetChild = []
    #     for eachUnmatched in unmatchedChild:
    #         bugAbbvSetChild.append(eachUnmatched.getBugAbbv())
    #         categorySetChild.append(eachUnmatched.getCategoryAbbrev())
    #         classSetChild.append(eachUnmatched.getClass())
    #         methodSetChild.append(eachUnmatched.getMethod())
    #         fieldSetChild.append(eachUnmatched.getField())
    #         sourcePathSetChild.append(eachUnmatched.getSourcePath())
    #         startSetChild.append(eachUnmatched.getStartLine())
    #         endSetChild.append(eachUnmatched.getEndLine())
    #
    #     dataframe = pd.DataFrame(
    #         {'Bug': bugAbbvSetChild, 'category': categorySetChild, "class name": classSetChild,\
    #          "method name": methodSetChild,"field name":  fieldSetChild,"source path":sourcePathSetChild,\
    #          "start":startSetChild,"end":endSetChild})
    #
    #     saveNewResults = os.path.join(saveKafkaPMDResultsPathOnWin, 'new')
    #     dataframe.to_csv(
    #         os.path.join(saveNewResults, parentCommit[0:7] + "_" + childCommit[0:7] + "_new_warnings.csv"),
    #         index=False,
    #         sep=',')
    #
    #
    #
    #     matchedPairsSavePath = os.path.join(r'D:\ThesisData\MatchedPairs\PMD\kafka',str(childCommit) + '.xml')
    #     MatchedPairsCollector.wrtieToXML(matchedPairs,matchedPairsSavePath)
    #     row = [childCommit, matchingEndTime - matchingStartTime]
    #     with open(r"D:\ThesisData\TimeMeasurment\Original\PMD\kafka\TimeMeasurment.csv", 'a', newline='') as f:
    #         fieldnames = ['Commit', 'Time']
    #         writer = csv.DictWriter(f, fieldnames=fieldnames)
    #         writer.writerow({'Commit': row[0], 'Time': row[1]})
    #     print(f"finish {count}/{len(commitList)} commits PMD")
    #     count += 1
    #
    # print("finish analysis of PMD")







    ###start to Spotbugs
    goneResultsPath = os.path.join(saveKafkaSpotbugsResultsPathOnWin, 'gone')
    for i, j, k in os.walk(goneResultsPath):
        fNewList = k
    repoPath = projectPathOnWin

    ###start to track Spotbugs
    f = open(commitListPathOnWin2000)
    #print(f"open file {commitListPathOnWin2000}")
    commitList = f.readlines()

    count = 1
    commitsSkipList = ['ae31ee63dc3bdb9068543791bea44a12a97aa928',"2ef6ee2338178c7501f5bd4c7cce5f4cea9d3e17","1dc30272e1e684764563e3091a19a8ff8892f8eb","77ebd32016d13c64ee5a3c7db63ca71bf4b79aad",
                       "acd669e4248c605ac54c38862a8678f521f6f574","b4d8552218c9ab41bc1e0221c4e79417a2662d19","bce10794a016f86cda63ceb437d8db7dfc65063b","c53e274d3128bc92f0e8b6a79c407cf764f16f7b",
                       "345db596502de59a3119d2f86186143395b74e5b","d99f4a0ffa65ae3a654b043547f114a16fbe4905","f24a62d4acfc48e23dd4bbb854668a727e9445a8","1facab387f8c2e513c8b7397430251dc44970e35",
                       "837f31dd1850b179918f83338b4b4487486b2c58","0c035c46b47cd4734d0529486e776c6c18d6643d","0b3989fd72acc6e989c495c63cb8ca6aa5850811","d2b2fbdf94cf48094081650ebc18ee860e67d8d5",
                       "7d85785d3de7640ca0ee61e7110a32286e328343","49db5a63c043b50c10c2dfd0648f8d74ee917b6a","5145d6b6b413721948bf89079b13ddbe82143bf1","1d5f8649ce3e7c8d3b437e89b2cfbc6fdc18e49f",
                       "de4f4f530a92473edb3665c94ac386d5c53cc893","a5924025126a6ab77fd9fb74cf66a180931ffecf","9a71bfb9d64dae5d0296d162a01a62d8c13324da","37a4d5ea46bb5ba1bdf2d7cb03c3678a128b6f9e",
                       "d504e85011332016447472fb37f1c1edd8acbf1a","cc4dce94af8b19a796eeb7a9be78640739cb1a48","3afe2ed8e39da3605274baddc7245be569b4aed7","96bcfdfc7c9aac075635b2034e65e412a725672e",
                       "e5ec3f55c968292ae8fd0cb8ad8b626abed8f503","6732593bbad3d1e07f1ec7c2d00a2e1eabf382f2","418a91b5d4e3a0579b91d286f61c2b63c5b4a9b6","2db7eb7a8c28f4f5d2550b45a9215948652f82ca",
                       "10b84a3661cde77b25f6408e6f360655ee618a18","e6fd99dc6253333c5aaa9931d8ae319e637e9a11","92004fa21a9cc75e3790ab39e44d4d3b754d95d9","ce19f34f1e3e6e697cce2e01721bedc850fca698",
                       "028e80204dd9bfd9d6258f1eb5b0e4132bd3795d","e7b9e0473062e4062ee65d4eb4b1a35c66f77781","7a9631e6349239b2dff3728d9237e6a17aa5ad81","68fb2932c9bbcec6c71886fd8f7d2b93b4a00274",
                       "5b25d823aff47f1a50848f5d2b3d329441aac8e9","04770916a743ca9526cfa2fdecaef419d429a443","70c51633f2f4bdcdc045697c17cbb47c78ed14ad","ebd1354fd7578deb1cfb15846d7dbf8c9cf26074",
                       "8fb5e63aa88019216e95fdbe0b6874c723b64bb4","f2dd6aa2698345fd0b0348f7bc74ce3215adf682","79757c90df8ee8390aa256998ce5cd1394d8822a","7ea0655711a664296cddb656364d367c66ed277c",
                       "ed3bd79633ae227ad995dafc3d9f384a5534d4e9","0848b78881afce5899cea1f10c323249f9f0b8cc","741cb761c5239297029a446518c332f6c4ed08f6","f393b2f7dd477c3a43e70631f7036a211bf5d740",
                       "a947fe8da8646058335ff76b9a744462a3337a63","4c602e6130e869abbd111d5d4efe1c2046935c6c","eda4a2904a863b04f6ea511a4cf1e2bd4806ad35","e8a3bc74254a8e4e4aaca41395177fa4a98b480c",
                       "9a0ea25fee85837748145d37c69cf4d9bb7f9933","fc1dc358ee9b956e062b0966e1ed1fef40ab43d8","7b5ffa0a070065e5e8320f481bbd8a3a26378f91","eb3335ef592a3dd22895a5bb499a2d0b232227a7",
                       "12f310d50e7f5b1c18c4f61a119a6cd830da3bc0","2155c6d54b087206b6aa1d58747f141761394eaf","0ffdf8307f8c0822def6f97f69777337106fc347","7a3dffb0ca1f7ff2bd838f42ca2f12b7a2fc3b0e",
                       "152292994e45d5bedda0673c142f9406e70d5d3e","145cad752d720c6ea735a5e2f977d10ace5bcc0f","e8959bd766cc6e19f6208fe7ea0a3103cc8fe123","8afce0e338e3715824e309f6289af6bc607ce020",
                       "12947f4f944955240fd14ce8b75fab5464ea6808","523465b3c17fc2ef67b0de10c78f83aae56606ae","4b54eb46212a5d40d814ab36315f589d69782675","269b65279c746bc54c611141a5a6509f9b310f11",
                       "dc634f18f7ea2ef24d202d6a2380365754005b60","ef89cf4eb687dbcca719acca09c98ded001d12dd","4b29487fa9d3d4ff8adaaaa6204db796eccd3a68","e2e8bdbd8cb6ca2ac962c72147d21a9e8b9ba2c0",
                       "d152989f26f51b9004b881397db818ad6eaf0392","71a7219dfdc0a40dc1846c749d2f219776b56955","f775be0514dc6a512245fd244e06e0aa11cc45c4","4824dc994d7fc56b7540b643a78aadb4bdd0f14d",
                       "f11fa5ef402193e2da785466e698e11b56bd19c7","0d56f1413557adabc736cae2dffcdc56a620403e"]
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
        resultParent = os.path.join(saveKafkaSpotbugsReportsPathOnWin, parentCommit + '.xml')
        resultChild = os.path.join(saveKafkaSpotbugsReportsPathOnWin, childCommit + '.xml')

        childFilename = resultChild
        parentFilename = resultParent
        #print(parentFilename)
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

        saveGoneResults = os.path.join(saveKafkaSpotbugsResultsPathOnWin, 'gone')
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

        saveNewResults = os.path.join(saveKafkaSpotbugsResultsPathOnWin, 'new')
        dataframe.to_csv(
            os.path.join(saveNewResults, commitList[i][0:7] + "_" + commitList[i + 1][0:7] + "_new_warnings.csv"),
            index=False,
            sep=',')

        # test
        # dataframe.to_csv("commendline-U.csv", index=False, sep=',')
        ##

        matchedPairsSavePath = os.path.join(r'D:\ThesisData\allkafkaSptobugsMatchedPairs', str(childCommit) + '.xml')
        MatchedPairsCollector.wrtieToXML(matchedPairs, matchedPairsSavePath)
        row = [childCommit, matchingEndTime - matchingStartTime]
        with open(r"D:\ThesisData\TimeMeasurment\Original\Spotbugs\kafka\TimeMeasurment.csv", 'a', newline='') as f:
            fieldnames = ['Commit', 'Time']
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writerow({'Commit': row[0], 'Time': row[1]})
        print(f"finish {count}/{len(commitList)} commits Spotbugs::{childCommit}")
        count += 1

    print("finish analysis of Spotbugs")