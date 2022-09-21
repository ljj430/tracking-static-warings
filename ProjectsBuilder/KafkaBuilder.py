import os


def buildKafka(kafkaPath,commit):
    print(commit)
    os.chdir(kafkaPath)
    os.system('git checkout -f ' + commit)

    with open(r"build.gradle","r+") as f:
        text = f.readlines()
        flag = False

        for i in range(len(text)):
            if ('classpath "org.scoverage:gradle-scoverage:$versions.scoveragePlugin"' in text[i]) or ("classpath 'org.scoverage:gradle-scoverage:$versions.scoveragePlugin'" in text[i]):
                flag = True
                break
            elif ("classpath 'org.scoverage:gradle-scoverage:" in text[i]) or ('classpath "org.scoverage:gradle-scoverage:' in text[i]):
                flag = True
                text[i] = "    classpath 'org.scoverage:gradle-scoverage:2.5.0'\n"
                break

        if flag == False:
            print(f"No matched line in Commit:{commit}")
            with open(r"D:\ThesisData\abnormal_kafkaSpotbugs.txt", "a+") as ff:
                ff.writelines(commit)
        else:
            with open(r"build.gradle", "w+") as f:
                f.writelines(text)



    os.system("gradle")
    # os.system("./gradlew clean")
    # os.system("./gradlew releaseTarGzAll -x signArchives")
    os.system("gradlew clean")
    os.system("gradlew releaseTarGzAll -x signArchives")
