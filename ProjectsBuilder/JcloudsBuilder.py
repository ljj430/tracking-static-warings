import os
def buildJclouds(JcloudsPath,commit):
    fileList = os.listdir(JcloudsPath)
    # print(fileList)
    flag = False
    for name in fileList:
        if 'pom.xml' in name:
            flag = True
            break
    if flag:
        print(JcloudsPath)
        os.chdir(JcloudsPath)
        os.system('git checkout -f ' + commit)
        #os.system("mvn clean install -DskipTests")
        os.system("mvn clean install -Drat.numUnapprovedLicenses=100 -DskipTests")

