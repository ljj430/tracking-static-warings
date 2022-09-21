import re
import shutil as st
import os
def Divide(path_dict):
    for key, value in saveResultPathOnLinux.items():
        targetNewPath = value+'/NewUnmatchedViolations'
        targetGonePath = value+'/GoneUnmatchedViolations'
        if not os.path.exists(targetGonePath):
            os.makedirs(targetGonePath)
        if not os.path.exists(targetNewPath):
            os.makedirs(targetNewPath)
        files = os.listdir(value)
        fileCount = 0
        violationCount = 0
        violationCountEachFile = []
        for file in files:
            if "gone_warnings" in file:
                #move to Gone warnings
                st.move(value+"/"+file,targetGonePath+'/'+file)
            elif "new_warnings" in file:
                # move to New warnings
                st.move(value+"/"+file,targetNewPath+'/'+file)

            else:
                ###no matched
                print(file,"is not matched")

#step1 path set



#step2 matching name

#step3 move file in a new folder



if __name__ =="__main__":
    jcloudsSpotbugsPath = "/Users/lijunjie/Desktop/Master/Thesis/Manual analysis/PMDjclouds/Results/"
    jcloudsPMDPath = "/Users/lijunjie/Desktop/Master/Thesis/Task/Week9/5 commits/results/"
    jcloudsSpotbugsPath = "/Users/lijunjie/Desktop/Master/manual work/resultsLJJ/Spotbugs/jclouds"

    #
    basicPath = "/home/ljj/test/resultsLJJ/"
    jcloudsSpotbugsPath = basicPath + "Spotbugs/jclouds"
    jcloudsPMDPath = basicPath + "PMD/jclouds"
    kafkaSpotbugsPath = basicPath + "Spotbugs/kafka"
    kafkaPMDPath = basicPath + "PMD/kafka"
    jcloudsSpotbugsPath = "/Users/lijunjie/Desktop/Master/manual work/resultsLJJ/Spotbugs/jclouds"
    saveResultPathOnLinux = {"jclouds_Spotbugs":jcloudsSpotbugsPath}
    #saveResultPathOnLinux = {"jclouds":"/Users/lijunjie/Desktop/Master/Thesis/Results/original_result"}

    Divide(saveResultPathOnLinux)