import os
def buildGuava(GuavaPath,commit):
    os.chdir(GuavaPath)
    os.system('git checkout -f ' + commit)
    fileList = os.listdir(GuavaPath)
    # print(fileList)
    flag = False
    for name in fileList:
        if 'pom.xml' in name:
            flag = True
            break
    if flag:
        print(commit)
        os.chdir(GuavaPath)
        os.system("mvn clean")
        os.system("mvn install -DskipTests")

