from  github import Github
import heapq
projectListPath = r"D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\projectsList.txt"
f=open(projectListPath)
lines = f.readline()
projectList=[]
while lines:
    couple = []
    if lines[-1]=='\n':
        lines=lines[:-1]
    lines = lines.replace("https://github.com/","")
    lines = lines.replace(".git","")
    projectList.append(lines)
    lines = f.readline()
f.close()
g = Github("0ffe7e9f6d71d55d93ce5ca2dc1d7a88b5e49c18",timeout=300)
#g = Github("token")
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")
#g = Github(base_url="https://{hostname}/api/v3", login_or_token="access_token")
#repo = g.get_repo("apache/maven-surefire")
#repo = g.get_repo("IDPF/epubcheck")


#stargazer = repo.get_stargazers()
exceptionList = []
print(f'len:{len(projectList)}')
length = len(projectList)
starList = []
count = 1
for project in projectList:
    #print(project)
    starDic = {}
    try:
        repo = g.get_repo(project)
        #stargazer = repo.get_stargazers()
        #print(repo.name)

        starsCount = repo.stargazers_count
        #print(f'start:{starsCount}')
        starDic["name"] = project
        starDic["starCount"]= int(starsCount)

        starList.append(starDic)
        # lastCommit = repo.updated_at
        # print(lastCommit)
        #print(lastCommit.)
        print(f'{count}/{len(projectList)}')
        count+= 1
    except:
        exceptionList.append(project)
        count += 1
        continue
print(f"exception: {exceptionList}")

filtedProjects = heapq.nlargest(10, starList, key=lambda s: s['starCount'])

for project in filtedProjects:
    repo = g.get_repo(project['name'])
    print(project['name'])

    starsCount = repo.stargazers_count
    print(f'start:{starsCount}')
    lastUpdated = repo.updated_at
    print(f'lastUpdated:{lastUpdated}')
    print()
    #print(lastCommit.)