import os


###
###read the commitList.txt
###
###4a5cba8
###05ba5aa
def runSpotbugs(spotbugsPath,saveSBReportPath,detectPath,commit):
    ###change to the path of spotbugs
    os.chdir(spotbugsPath)
    #print(detectPath)
    ##detectPath='/Users/lijunjie/Apps/java\ program/out'
    ##执行spotbugs##java - jar spotbugs.jar - textui - xml - output 123.xml /Users/lijunjie/Apps/java\ program/out
    #print(saveSBReportPath)
    os.system('java -jar spotbugs.jar -textui -xml -output '+saveSBReportPath+'/'+commit+'.xml -low '+ detectPath)

