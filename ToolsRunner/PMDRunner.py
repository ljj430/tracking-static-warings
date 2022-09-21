import os



###改变到spotbugs路径

##
##detectPath='/Users/lijunjie/Apps/java\ program/out'
##执行spotbugs##java - jar spotbugs.jar - textui - xml - output 123.xml /Users/lijunjie/Apps/java\ program/out
def runPMD(pmdPath,savePmdReportPath,detectPath,ruleSetPath,commit):
    os.chdir(detectPath)
    os.system('git checkout -f ' + commit)
    os.chdir(pmdPath)
    #os.system('./run.sh pmd -d ' + detectPath +' -f xml -R '+ ruleSetPath + ' -r ' + savePmdReportPath + '/' + commit + '.xml')
    os.system('run.sh pmd -d ' + detectPath +' -f xml -R '+ ruleSetPath + ' -r ' + savePmdReportPath + '/' + commit + '.xml')
