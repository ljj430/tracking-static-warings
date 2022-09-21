
import os
import pandas as pd
import numpy as np

originalResultPathOnMac=r'/Users/lijunjie/Desktop/Master/Thesis/Task/Week9/5 commits/orignal_results/29violations/2a56db0_09936b5_gone_warnings29violations.csv'
improvedResultPathOnMac=r'/Users/lijunjie/Desktop/Master/Thesis/Task/Week9/5 commits/orignal_results/Improved2/2a56db0_09936b5_gone_warnings.csv'

originalResultPathOnLinux=r'/home/ljj/test/5Commits/labelledResult/2a56db0_09936b5_gone_warnings29vio.csv'
improvedResultPathOnLinux=r'/home/ljj/test/5Commits/Improved2/2a56db0_09936b5_gone_warnings.csv'

originalResultPathOnMac=r'/Users/lijunjie/Desktop/Master/Thesis/Task/Week9/5 commits/orignal_results/Improved2/2a56db0_09936b5_gone_warningsImproved2 .csv'
improvedResultPathOnMac=r'/Users/lijunjie/Desktop/Master/Thesis/Task/Week9/5 commits/orignal_results/Improved3/2a56db0_09936b5_gone_warnings3.csv'



def fillCompareInfo(fileName,originalPath,improvedPath,savePath):
    newViolationFromImproved = []
    goneViolationFromImproved = []

    #originalResult = pd.read_csv(originalResultPathOnLinux)
    #improvedResult = pd.read_csv(improvedResultPathOnLinux)
    originalResult = pd.read_csv(originalPath+'/'+fileName)##changed

    improvedResult = pd.read_csv(improvedPath+'/'+fileName)##changed

    improvedResult['False positive/true positive'] = ""
    improvedResult['Reasons'] = ""
    originalResult = originalResult.fillna("")
    improvedResult = improvedResult.fillna("")

    for i in range(0,len(originalResult)):
        matchedFlag = False
        for j in range(0,len(improvedResult)):
            #class name    method name    field name    source path    start    end    False positive / true positive    Reasons

            #print(originalResult.iloc[i]['False positive/true positive'])
            if originalResult.iloc[i]['Bug'] == improvedResult.iloc[j]['Bug'] and originalResult.iloc[i]['class name'] == improvedResult.iloc[j]['class name']and originalResult.iloc[i]['method name'] == improvedResult.iloc[j]['method name']and originalResult.iloc[i]['field name'] == improvedResult.iloc[j]['field name']\
                and originalResult.iloc[i]['source path'] == improvedResult.iloc[j]['source path']and originalResult.iloc[i]['start'] == improvedResult.iloc[j]['start']and originalResult.iloc[i]['end'] == improvedResult.iloc[j]['end']:
                improvedResult.loc[j,'False positive/true positive'] = originalResult.iloc[i]['False positive/true positive']
                improvedResult.loc[j,'Reasons'] = originalResult.iloc[i]['Reasons']
                matchedFlag = True
                break
        if not matchedFlag:
            goneViolationFromImproved.append(originalResult.iloc[i])


    # ###Gone after improved
    # print("Gone after improved:")
    # for i in goneViolationFromImproved:
    #     print(i['Bug'],i['class name'],i['method name'],i['field name'],i['start'],i['end'])
    # print("The number of gone")
    # print(len(goneViolationFromImproved))
    #
    #
    # ###New after improved:
    # print("New after improved:")
    # count = 0
    # for i in range(0,len(improvedResult)):
    #     if improvedResult.iloc[i]['False positive/true positive'] == "":
    #         print(improvedResult.iloc[i]['Bug'],improvedResult.iloc[i]['class name'],improvedResult.iloc[i]['method name'],improvedResult.iloc[i]['field name'],improvedResult.iloc[i]['start'],improvedResult.iloc[i]['end'])
    #         count += 1
    # print("The number of new")
    # print(count)

    #improvedResult.to_csv(improvedResultPathOnLinux,index=False,sep=',')
    improvedResult.to_csv(savePath+'/'+fileName,index=False,sep=',')##changed


def fillCompareInfo2(fileName,originalPath,improvedPath,savePath):
    newViolationFromImproved = []
    goneViolationFromImproved = []

    #originalResult = pd.read_csv(originalResultPathOnLinux)
    #improvedResult = pd.read_csv(improvedResultPathOnLinux)
    originalResult = pd.read_csv(originalPath+'/'+fileName)##changed

    improvedResult = pd.read_csv(improvedPath+'/'+fileName)##changed

    improvedResult['False positive/true positive'] = ""
    improvedResult['Reasons'] = ""
    originalResult = originalResult.fillna("")
    improvedResult = improvedResult.fillna("")

    for i in range(0,len(originalResult)):
        matchedFlag = False
        for j in range(0,len(improvedResult)):
            #class name    method name    field name    source path    start    end    False positive / true positive    Reasons

            #print(originalResult.iloc[i]['False positive/true positive'])
            if improvedResult.iloc[j]['Bug'] == originalResult.iloc[i]['Bug'] and improvedResult.iloc[j][
                'class name'] in originalResult.iloc[i]['class name'] and improvedResult.iloc[j]['method name'] in \
                    originalResult.iloc[i]['method name'] and improvedResult.iloc[j]['field name'] in \
                    originalResult.iloc[i]['field name'] \
                    and originalResult.iloc[i]['source path'] == improvedResult.iloc[j]['source path'] and \
                    originalResult.iloc[i]['start'] == improvedResult.iloc[j]['start'] and originalResult.iloc[i][
                'end'] == improvedResult.iloc[j]['end']:
                improvedResult.loc[j, 'False positive/true positive'] = originalResult.iloc[i][
                    'False positive/true positive']
                improvedResult.loc[j, 'Reasons'] = originalResult.iloc[i]['Reasons']
                matchedFlag = True
                break
        if not matchedFlag:
            goneViolationFromImproved.append(originalResult.iloc[i])


    ###Gone after improved
    # print("Gone after improved:")
    # for i in goneViolationFromImproved:
    #     print(i['Bug'],i['class name'],i['method name'],i['field name'],i['start'],i['end'])
    # print("The number of gone")
    # print(len(goneViolationFromImproved))


    ###New after improved:
    print("New after improved:")
    count = 0
    for i in range(0,len(improvedResult)):
        if improvedResult.iloc[i]['False positive/true positive'] == "":
            print(improvedResult.iloc[i]['Bug'],improvedResult.iloc[i]['class name'],improvedResult.iloc[i]['method name'],improvedResult.iloc[i]['field name'],improvedResult.iloc[i]['start'],improvedResult.iloc[i]['end'])
            count += 1
    print("The number of new")
    print(count)

    #improvedResult.to_csv(improvedResultPathOnLinux,index=False,sep=',')
    improvedResult.to_csv(savePath+'/'+fileName,index=False,sep=',')##changed



def getGoneTruePositive(fileName,originalPath,improvedPath):
    if os.path.exists(originalPath + '/' + fileName) and os.path.exists(improvedPath + '/' + fileName):
        goneTruePositive = []

        #originalResult = pd.read_csv(originalResultPathOnLinux)
        #improvedResult = pd.read_csv(improvedResultPathOnLinux)
        originalResult = pd.read_csv(originalPath+'/'+fileName)##changed
        improvedResult = pd.read_csv(improvedPath+'/'+fileName)##changed

        improvedResult['False positive/true positive'] = ""
        improvedResult['Reasons'] = ""
        originalResult = originalResult.fillna("")
        improvedResult = improvedResult.fillna("")

        for i in range(0,len(originalResult)):
            matchedFlag = False
            for j in range(0,len(improvedResult)):
                #class name    method name    field name    source path    start    end    False positive / true positive    Reasons

                #print(originalResult.iloc[i]['False positive/true positive'])
                if originalResult.iloc[i]['Bug'] == improvedResult.iloc[j]['Bug'] and originalResult.iloc[i]['class name'] == improvedResult.iloc[j]['class name']and originalResult.iloc[i]['method name'] == improvedResult.iloc[j]['method name']and originalResult.iloc[i]['field name'] == improvedResult.iloc[j]['field name']\
                    and originalResult.iloc[i]['source path'] == improvedResult.iloc[j]['source path']and originalResult.iloc[i]['start'] == improvedResult.iloc[j]['start']and originalResult.iloc[i]['end'] == improvedResult.iloc[j]['end']:
                    improvedResult.loc[j,'False positive/true positive'] = originalResult.iloc[i]['False positive/true positive']
                    improvedResult.loc[j,'Reasons'] = originalResult.iloc[i]['Reasons']
                    matchedFlag = True
                    break
            if (not matchedFlag) and originalResult.iloc[i]['False positive/true positive'] == 't':
                goneTruePositive.append(originalResult.iloc[i])
        return goneTruePositive


def getGoneTruePositive2(fileName,originalPath,improvedPath):  ##to resolve opt$5 match opt
    if os.path.exists(originalPath + '/' + fileName) and os.path.exists(improvedPath + '/' + fileName):
        goneTruePositive = []

        #originalResult = pd.read_csv(originalResultPathOnLinux)
        #improvedResult = pd.read_csv(improvedResultPathOnLinux)
        originalResult = pd.read_csv(originalPath+'/'+fileName)##changed
        improvedResult = pd.read_csv(improvedPath+'/'+fileName)##changed

        improvedResult['False positive/true positive'] = ""
        improvedResult['Reasons'] = ""
        originalResult = originalResult.fillna("")
        improvedResult = improvedResult.fillna("")

        for i in range(0,len(originalResult)):
            matchedFlag = False
            for j in range(0,len(improvedResult)):
                #class name    method name    field name    source path    start    end    False positive / true positive    Reasons

                #print(originalResult.iloc[i]['False positive/true positive'])
                if   improvedResult.iloc[j]['Bug'] == originalResult.iloc[i]['Bug'] and  improvedResult.iloc[j]['class name'] in originalResult.iloc[i]['class name'] and  improvedResult.iloc[j]['method name'] in originalResult.iloc[i]['method name'] and  improvedResult.iloc[j]['field name'] in originalResult.iloc[i]['field name'] \
                    and originalResult.iloc[i]['source path'] == improvedResult.iloc[j]['source path']and originalResult.iloc[i]['start'] == improvedResult.iloc[j]['start']and originalResult.iloc[i]['end'] == improvedResult.iloc[j]['end']:
                    improvedResult.loc[j,'False positive/true positive'] = originalResult.iloc[i]['False positive/true positive']
                    improvedResult.loc[j,'Reasons'] = originalResult.iloc[i]['Reasons']
                    matchedFlag = True
                    break
            if (not matchedFlag) and originalResult.iloc[i]['False positive/true positive'] == 't':
                goneTruePositive.append(originalResult.iloc[i])
        return goneTruePositive


def SynchronizeData(fileName,originalPath,improvedPath):
    if os.path.exists(originalPath + '/' + fileName) and os.path.exists(improvedPath + '/' + fileName):
        originalResult = pd.read_csv(originalPath + '/' + fileName)  ##changed
        improvedResult = pd.read_csv(improvedPath + '/' + fileName)  ##changed
        originalResult = originalResult.fillna("")
        improvedResult = improvedResult.fillna("")
        for i in range(0,len(originalResult)):
            matchedFlag = False
            for j in range(0,len(improvedResult)):
                #class name    method name    field name    source path    start    end    False positive / true positive    Reasons

                #print(originalResult.iloc[i]['False positive/true positive'])
                if originalResult.iloc[i]['Bug'] == improvedResult.iloc[j]['Bug'] and originalResult.iloc[i]['class name'] == improvedResult.iloc[j]['class name']and originalResult.iloc[i]['method name'] == improvedResult.iloc[j]['method name']and originalResult.iloc[i]['field name'] == improvedResult.iloc[j]['field name']\
                    and originalResult.iloc[i]['source path'] == improvedResult.iloc[j]['source path']and originalResult.iloc[i]['start'] == improvedResult.iloc[j]['start']and originalResult.iloc[i]['end'] == improvedResult.iloc[j]['end']\
                        and originalResult.iloc[i]['False positive/true positive'] == 'f' and improvedResult.iloc[j]['False positive/true positive'] == 't':
                    print("path:",originalPath)
                    print("file:",fileName)
                    print("violation type:",originalResult.iloc[i]['Bug'])
                    print("violation soucefile:", originalResult.iloc[i]['source path'])

                    print("violation start:", originalResult.iloc[i]['start'])
                    print("violation end:", originalResult.iloc[i]['end'])




if __name__=="__main__":
    originalPathLinux = "/home/ljj/test/resultsLJJ/Spotbugs/jclouds"
    improvedPathLinux = "/home/ljj/test/ImprovedResults/Spotbugs/jclouds/GoneUnmatchedViolations"
    savePathLinux = "/home/ljj/test/ImprovedResults/labeledResults/PMD/kafka"


    # compare gone violations
    # originalPathMac = r"/Users/lijunjie/Desktop/Master/manual work/labeled results/PMD/kafka"
    # improvedPathMac = r"/Users/lijunjie/Desktop/Master/manual work/ImprovedResults/PMD/kafka/GoneUnmatchedViolations"
    # savePathMac = r"/Users/lijunjie/Desktop/Master/manual work/ImprovedResults/labeledResults/PMD/kafka"
    #
    # #files = os.listdir(improvedPathMac)
    # files = os.listdir(originalPathMac)
    # for file in files:
    #
    #     if file.startswith('.'):
    #         continue
    #     fillCompareInfo(file,originalPathMac,improvedPathMac,savePathMac)
    #     goneTruePositives = getGoneTruePositive(file, originalPathMac, improvedPathMac)
    #
    #
    #     #print(goneTruePositives is None)
    #     if goneTruePositives is not None:
    #         if len(goneTruePositives)>0:
    #             print("commit:",file)
    #             for each in goneTruePositives:
    #                 print("violation")
    #                 print(each.Bug,each["source path"],each.start,each.end)

    #    #SynchronizeData(file,originalPathMac,savePathMac)



    #for new violation
    originalPathMac = r"/Users/lijunjie/Desktop/Master/manual work/newViolations/labeled/Spotbugs/kafka/NewUnmatchedViolations"
    improvedPathMac = r"/Users/lijunjie/Desktop/Master/manual work/ImprovedResults/Spotbugs/kafka/NewUnmatchedViolations"
    savePathMac = r"/Users/lijunjie/Desktop/Master/manual work/labeledNewResult/Spotbugs/kafka"
    #files = os.listdir(improvedPathMac)
    files = os.listdir(originalPathMac)
    for file in files:

        if file.startswith('.'):
            continue
        #print("file:", file)
        fillCompareInfo(file,originalPathMac,improvedPathMac,savePathMac)

        goneTruePositives = getGoneTruePositive(file, originalPathMac, improvedPathMac)


        #print(goneTruePositives is None)
        if goneTruePositives is not None:
            if len(goneTruePositives)>0:
                print("commit:",file)
                for each in goneTruePositives:
                    print("violation")
                    print(each.Bug,each["source path"],each.start,each.end)