import os
import pandas as pd
import shutil



def moveReports(fromPath,targetPath,commitListPath,commits2000):
    ### 0.create dirs if no exist

    if not os.path.exists(targetPath,):
        os.makedirs(targetPath,)

    commitDic2000 = {}
    with open(commits2000) as ff:
        lines = ff.readline()
        while lines:
            if lines[-1] == '\n':
                lines = lines[:-1]
            commitDic2000[lines[0:7]] = lines
            lines = ff.readline()
    ###1.read commit list
    f = open(commitListPath)
    lines = f.readline()
    commitList = []
    ###2.commitList
    while lines:
        if lines[-1] == '\n':
            lines = lines[:-1]
        lines = lines.split('_')
        commitList.append(commitDic2000[lines[0]])
        print(f"line[0]:{commitDic2000[lines[0]]}")
        commitList.append(commitDic2000[lines[1]])
        lines = f.readline()
    commitList = set(commitList)
    commitList = list(commitList)
    print(len(commitList))
    ####3.move report  to target
    for commit in commitList:
        ##for test:
        print("commit:{}.xml".format(commit))
        shutil.copyfile(fromPath+'/'+ commit + '.xml',targetPath + '/' + commit +'.xml')

def moveResults(fromPath,targetPath,commitListPath):
    ### 0.create dirs if no exist
    for t in targetPath:
        if not os.path.exists(t):
            os.makedirs(t)
    ###1.read commit list
    goneViolationPath = fromPath[0]
    newViolationPath = fromPath[1]
    commitList = []
    f = open(commitListPath)
    lines = f.readline()
    ###2.move results to target
    while lines:
        if lines[-1]=='\n':
            lines=lines[:-1]
        commitList.append(lines)
        lines = f.readline()

    ##move gone vioaltions
    files = os.listdir(goneViolationPath)
    print("in results:{}".format(len(files)))
    print("in results:{}".format(len(commitList)))
    count = 0 
    for file in files:
        for commit in commitList:
            if commit in file:
                ##for test:
                print("commit:{}   file:{}".format(commit, file))
                count +=1
                shutil.copyfile(goneViolationPath+'/'+file,targetPath[0] + '/' +file)
    print("in results:{}".format(count))
    #move new violations
    files =  os.listdir(newViolationPath)
    for file in files:
        for commit in commitList:
            if commit in file:
                ##for test:
                print("commit:{}   file:{}".format(commit, file))
                shutil.copyfile(newViolationPath+'/'+file,targetPath[1] + '/' +file)

        #lines = lines.split('_')
        #parentCommit = lines[0]
        #childCommit = lines[1]








###3.move report to target

if __name__=='__main__':
    # #fromResultsPath = ['/home/ljj/test/NewResults/PMD/kafka/Results/GoneUnmatchedViolations','/home/ljj/test/NewResults/PMD/kafka/Results/NewUnmatchedViolations']
    # #targetResultsPath = ['/home/ljj/test/NewResults/PMD/kafka/ResultsAfterSample/GoneUnmatchedViolations','/home/ljj/test/NewResults/PMD/kafka/ResultsAfterSample/NewUnmatchedViolations']
    # fromReportsPath = '/home/ljj/test/Reports/PMD/kafka'
    # targetReportsPath = '/home/ljj/test/NewResults/PMD/kafka/Reports'
    # commitListPath = '/home/ljj/test/findbugsanalysis/FixPatternMining/CommitList/kafka_PMD_NewViolations.txt'

    fromResultsPath = [r'D:\ThesisData\OriginalResults\Spotbugs\guava\gone',
                       r'D:\ThesisData\OriginalResults\Spotbugs\guava\new']
    targetResultsPath = [r'D:\ThesisData\SampledResults\Spotbugs\guava\gone',
                         r'D:\ThesisData\SampledResults\Spotbugs\guava\new']
    fromReportsPath = r'D:\ThesisData\Reports\Spotbugs\guava'
    targetReportsPath = r'D:\ThesisData\SampledReports\Spotbugs\guava'
    guava2000commits = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Guava2000commitList.txt'
    commitListPath = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\guava_Spotbugs.txt'
    moveResults(fromResultsPath,targetResultsPath,commitListPath)
    moveReports(fromReportsPath,targetReportsPath,commitListPath,guava2000commits)