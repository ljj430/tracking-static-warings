from git import Repo
import Utils as utils
import os

def CommitsBasedOnTagsCollect(repoPath, startTagToendTag):
    repo = Repo(repoPath)

    #tag = "v23.0"
    #print(repo.commit(tag))
    commits = list(repo.iter_commits(startTagToendTag))
    for c in commits:
        print(f"commit:{c}")
    print(f"length:{len(commits)}")


def printAllHistoryCommit(repoPath,latestCommit):
    utils.checkout(repoPath,latestCommit)
    repo = Repo(repoPath)
    for commit in list(repo.iter_commits()):
        print(commit.hexsha)
    print(len(list(repo.iter_commits())))

def getBetweenCommits(repoPath,priviousCommit, latterCommit): ###commit1 is a privious commit ###commit2 is a latter commit.
    repo = Repo(repoPath)
    commitList=[]
    msg = 'not matched privious commit'
    utils.checkout(repoPath, latterCommit)
    for commit in list(repo.iter_commits()):
        if priviousCommit in commit.hexsha:
            commitList.append(commit.hexsha)
            commitList.reverse()
            print("The oldest commit is ", commitList[0])
            print("The newest commit is ", commitList[-1])
            return commitList
        commitList.append(commit.hexsha)

def getFixedCountCommit(repoPath, latterCommit, maxCount):
    repo = Repo(repoPath)
    commitList = []
    msg = 'not matched privious commit'
    utils.checkout(repoPath, latterCommit)
    for commit in list(repo.iter_commits(max_count=maxCount)):
        commitList.append(commit.hexsha)
    commitList.reverse()
    print("The oldest commit is ", commitList[0])
    print("The newest commit is ", commitList[-1])
    return commitList

def updateCommit(repoPath,commitListPath, saveUpdateCommitPath):

    f = open(commitListPath)
    lines = f.readline()
    commitList = []
    while lines:
        if lines[-1] == '\n':
            lines = lines[:-1]
        commitList.append(lines)
        lines = f.readline()
    f.close()

    commitUpdateList = []
    #
    for commit in commitList:
        #os.chdir(repoPath)
        #os.system('git checkout -f '+commit)
        utils.checkout(repoPath, commit)
        files = os.listdir(repoPath)
        if 'pom.xml' in files:
            commitUpdateList.append(commit)
    print(len(commitUpdateList))
    ff = open(saveUpdateCommitPath, 'w')
    for commit in commitUpdateList:
        if commit == commitUpdateList[-1]:
            ff.write(commit)
        else:
            ff.write(commit + '\n')
    ff.close()

def showAllTagsInfo(repoPath):
    #tagDic = {}
    repo = Repo(repoPath)
    for tag in repo.tags:
        print(f"tag:{tag}\ttagCommit:{tag.commit}\tDate:{tag.commit.committed_datetime}")
if __name__ == "__main__":


    kafkaPath = r""
    jcloudsPath = r""
    saveCommitListPath = r""


    commit = "5f584101c62023dafab0e9590b5d84f7fc3b5a53"
    springPath = r"D:\ThesisProject\trackingProjects\spring-boot"
    saveCommitListPath = r"D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Spring2000commitList(JJL).txt"
    #CommitsBasedOnTagsCollect(guavaPathOnWin,"v27.0...v29.0")
    commitList = getFixedCountCommit(springPath,commit, 2000)



    #save commitlist
    with open(saveCommitListPath,'w') as f:

        for commit in commitList:
           if commit == commitList[-1]:
               print(commit)
               f.write(commit)
           else:
               print(commit)
               f.write(commit + '\n')


    #updateCommit(repoPath,saveCommitList,saveUpdatePath)
