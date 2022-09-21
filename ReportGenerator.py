import os
import time
import ProjectsBuilder.KafkaBuilder as Kafka
import ProjectsBuilder.JcloudsBuilder as Jclouds
import ToolsRunner.SpotbugsRunner as Spotbugs
import ToolsRunner.PMDRunner as PMD



###the Path on Macbook
basicPathOnMac = r"/Users/lijunjie/Desktop/Master"
jcloudsPathOnMac = basicPathOnMac + r"/testProject/jclouds"
kafkaPathOnMac = basicPathOnMac + r"/testProject/kafka"
pmdPathOnMac = basicPathOnMac + r"/AnalysisTools/pmd-bin-6.20.0/bin"
saveJcloudsPMDReportPathOnMac = basicPathOnMac + r"/Reports/PMD/Jclouds"
CommitListPathOnMac = r"./CommitList/Jclouds300commitList.txt"
testCommitListPathOnMac = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/Jclouds2commitList.txt"

###the Path on Ubuntu####NEED TO CHANGE
basicPathOnLinux = r"/home/ljj/test"
kafkaPathOnLinux=basicPathOnLinux+r"/Projects/kafka"
jcloudsPathOnLinux=basicPathOnLinux+r"/Projects/jclouds"
pmdPathOnLinux =basicPathOnLinux +  r'/AnalyzeTools/pmd-bin-6.20.0/bin'

CommitListPathOnLinux = r"./CommitList/Kafka2000commitList.txt"
testCommitListPathOnLinux = r"testCommitList.txt"
jcloudsPathOnLinux = basicPathOnLinux + r"/Projects/jclouds"
saveJcloudsPMDReportPathOnLinux = basicPathOnLinux + r"/Reports/PMD/jclouds"
ruleSetPath = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\ruleset\rulesets.xml'
pmdPathWin =r"D:\ThesisProject\pmd-bin-6.24.0\pmd-bin-6.24.0\bin"
spotbugsPathWin =r"D:\ThesisProject\spotbugs\spotbugs\build\distributions\spotbugs-4.0.6-SNAPSHOT\spotbugs-4.0.6-SNAPSHOT\lib"

kafkaPathWin = r"D:\ThesisProject\trackingProjects\kafka"
saveKafkaSpotbugsWin= r"D:\ThesisData\kafkaSpotbugsReports9.27"
saveKafkaPMDWin = r"D:\ThesisData\1\kafka\PMD"
###Parameter set
commitListPath = CommitListPathOnLinux
projectPath = kafkaPathWin
saveSPReportPath = saveKafkaSpotbugsWin
savePMDReportPath = saveKafkaPMDWin

SpotbugsPath = spotbugsPathWin
PMDPath = pmdPathWin

projectBuilder = Kafka.buildKafka

spotbugsRunner = Spotbugs.runSpotbugs
pmdRunner = PMD.runPMD

ruleSetPath = ruleSetPath

###start to generate report
f=open(commitListPath)
lines = f.readline()
commitList=[]
while lines:
    if lines[-1]=='\n':
        lines=lines[:-1]
    commitList.append(lines)
    lines = f.readline()
f.close()
startTime=time.time()
for i,j,k in os.walk(saveSPReportPath):
        reportSPList = k
# PMD
######
# for i,j,k in os.walk(savePMDReportPath):
#         reportPMDList = k
count = 0
for line in commitList:
    flag = False
    for name in reportSPList:
        if line + ".xml" == name:
            print(f"commit:{line} has done")
            flag = True
    if flag:
        print(f"SP:{line[0:7]} has saved")
    else:
        #os.chdir(projectPath)
        #os.system('git checkout -f ' + line)

        projectBuilder(projectPath, line)
        spotbugsRunner(SpotbugsPath,saveSPReportPath,projectPath,line)
    #PMD
    # flag = False
    # for name in reportPMDList:
    #     if line + ".xml" == name:
    #         flag = True
    # if flag:
    #     print(f"PMD:{line} has saved")
    # else:
    #     pmdRunner(PMDPath,savePMDReportPath,projectPath,ruleSetPath,line)
    count += 1
    print(f"end {line}: {count}/{len(commitList)}")


endTime=time.time()


print("Compile {0} commits on  and spend {1} sec".format(len(commitList),endTime-startTime))