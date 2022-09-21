import os
import time
import ProjectsBuilder.GuavaBuilder as Guava
import ProjectsBuilder.JcloudsBuilder as Jclouds
import ToolsRunner.SpotbugsRunner as Spotbugs
import ToolsRunner.PMDRunner as PMD




###Parameter set
commitListPath =  r"D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Guava2000commitList1.txt"
projectPath = r"D:\ThesisProject\trackingProjects\guava"
saveSPReportPath = r"D:\ThesisData\Reports\Spotbugs\guava"
savePMDReportPath = r"D:\ThesisData\Reports\PMD\guava"

SpotbugsPath = r"D:\ThesisProject\spotbugs\spotbugs\build\distributions\spotbugs-4.0.6-SNAPSHOT\spotbugs-4.0.6-SNAPSHOT\lib"
PMDPath = r"D:\ThesisProject\pmd-bin-6.24.0\pmd-bin-6.24.0\bin"

projectBuilder = Guava.buildGuava

spotbugsRunner = Spotbugs.runSpotbugs
pmdRunner = PMD.runPMD

ruleSetPath = r"D:\ThesisProject\findbugsanalysis\FixPatternMining\ruleset\rulesets.xml"

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
for i,j,k in os.walk(savePMDReportPath):
        reportPMDList = k
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
    flag = False
    for name in reportPMDList:
        if line + ".xml" == name:
            flag = True
    if flag:
        print(f"PMD:{line} has saved")
    else:
        pmdRunner(PMDPath,savePMDReportPath,projectPath,ruleSetPath,line)
    count += 1
    print(f"end {line}: {count}/{len(commitList)}")


endTime=time.time()


print("Compile {0} commits on  and spend {1} sec".format(len(commitList),endTime-startTime))