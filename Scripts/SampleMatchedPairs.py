import xml.sax
from BugInstance import BugInstance as BugIns
import os
from xml.dom.minidom import Document
from random import sample

class MatchedPair:
    def __init__(self):
        self.commit = ""
        self.number = ""
        self.project = ""
        self.SAtool = ""

        self.paBugDescription = ""
        self.paClass = ""
        self.paMethod =""
        self.paField = ""
        self.paSourcePath = ""
        self.paStart = ""
        self.paEnd = ""

        self.chBugDescription = ""
        self.chClass = ""
        self.chMethod = ""
        self.chField = ""
        self.chSourcePath = ""
        self.chStart = ""
        self.chEnd = ""


    def setNumber(self,number):
        self.number = number
    def setOthers(self,commit, project, SAtool):
        self.commit = commit
        self.project = project
        self.SAtool = SAtool


    def setPa(self,paBugDescription, paClass,paMethod,paField,paSourcePath,paStart,paEnd):
        self.paBugDescription = paBugDescription
        self.paClass = paClass
        self.paMethod = paMethod
        self.paField = paField
        self.paSourcePath = paSourcePath
        self.paStart = paStart
        self.paEnd = paEnd

    def setCh(self, chBugDescription, chClass, chMethod, chField, chSourcePath , chStart, chEnd):
        self.chBugDescription =chBugDescription
        self.chClass = chClass
        self.chMethod = chMethod
        self.chField = chField
        self.chSourcePath = chSourcePath
        self.chStart = chStart
        self.chEnd = chEnd
    def __str__(self):
        return f"Matched Pair\ncommit:{self.commit}\tnumber:{self.number}\tproject:{self.project}\tSAtool:{self.SAtool}\n" \
            f"parent warning:\npaBugDescription:{self.paBugDescription}\npaClass:{self.paClass}\tpaMethod:{self.paMethod}\t" \
            f"paField:{self.paField}\npaStart:{self.paStart}\tpaEnd:{self.paEnd}\n" \
            f"child warning:\nchBugDescription:{self.chBugDescription}\nchClass:{self.chClass}\tchMethod:{self.chMethod}\t" \
            f"chField:{self.chField}\nchStart:{self.chStart}\tchEnd:{self.chEnd}"

class MatchedPairsHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.CurrentData = ""

        self.paBugDescription= ""
        self.paClassName = ""
        self.paMethodName = ""
        self.paFieldName = ""
        self.paSourcePath = ""
        self.paStart = ""
        self.paEnd = ""

        self.chBugDescription = ""
        self.chClassName = ""
        self.chMethodName = ""
        self.chFieldName = ""
        self.chSourcePath = ""
        self.chStart = ""
        self.chEnd = ""

        self.number =""
        self.matchedPairsList = []
        self.matchedPair = MatchedPair()
        self.inPa = False
        self.inCh = False
        # process beginning of elements

    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "MatchedPair":
            self.matchedPair = MatchedPair()
        elif tag == "ParentWarning":  ###extract class information
            self.inPa = True
            self.inCh = False
        elif tag == "ChildWarning":  ###extract class information
            self.inCh = True
            self.inPa = False

    # process end of elements
    def endElement(self, tag):
        self.CurrentData = tag
        if self.CurrentData == "MatchedPair":
            self.matchedPair.setPa(self.paBugDescription,self.paClassName,self.paMethodName,self.paFieldName,self.paSourcePath,self.paStart,self.paEnd)
            self.matchedPair.setCh(self.chBugDescription, self.chClassName, self.chMethodName, self.chFieldName,self.chSourcePath,
                                   self.chStart, self.chEnd)
            self.matchedPair.setNumber(self.number)

            self.matchedPairsList.append(self.matchedPair)
            self.paClassName = ''
            self.paMethodName = ''
            self.paSourcePath = ''
            self.paFieldName = ''
            self.paStart = ''
            self.paEnd = ''
            self.inCh = False
            self.inPa = False
        self.CurrentData = ""

    # process event content
    def characters(self, content):
        # print("content",content)
        # print("CurrentData",self.CurrentData)
        if self.CurrentData == "Number":
            self.number = content
        elif self.CurrentData == "BugDescription":
            if self.inPa:
                self.paBugDescription = content
            elif self.inCh:
                self.chBugDescription = content
        elif self.CurrentData == "Class":
            if self.inPa:
                self.paClassName = content
            elif self.inCh:
                self.chClassName = content

        elif self.CurrentData == "Method":
            if self.inPa:
                self.paMethodName = content
            elif self.inCh:
                self.chMethodName = content
        elif self.CurrentData == "Field":
            if self.inPa:
                self.paFieldName = content
            elif self.inCh:
                self.chFieldName = content
        elif self.CurrentData == "SourcePath":
            if self.inPa:
                self.paSourcePath = content
            elif self.inCh:
                self.chSourcePath = content
        elif self.CurrentData == "Start":
            if self.inPa:
                self.paStart = content
            elif self.inCh:
                self.chStart = content
        elif self.CurrentData == "End":
            if self.inPa:
                self.paEnd = content
            elif self.inCh:
                self.chEnd = content



def MatchedPairsReader(filename):  ###for the new approach
    # create a XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)
    # rewrite the ContextHandler
    Handler = MatchedPairsHandler()
    parser.setContentHandler(Handler)
    parser.parse(filename)  ####June 6 2018 commits 5104
    matchedPairs  = Handler.matchedPairsList
    return matchedPairs

def sampleMatchedPairsFromFolder(folderPath, savedPath, sampledSize, project, SAtool):
    g = os.walk(folderPath)
    matchedPairDic = {}
    sampledRecord =[]
    sampledPairs = []
    for path, dir_list,file_list in g:
        xmlFileList = []
        for file in file_list:
            if str(file).endswith(".xml"):
                xmlFileList.append(file)
                commit = str(file).replace(".xml","")
                project = "kafka"
                SAtool = "Spotbugs"

                filePath = os.path.join(folderPath,file)
                matchedPairs = MatchedPairsReader(filePath)
                length = len(matchedPairs)
                ###sample
                matchedPairDic[commit] = [length,filePath,commit,project,SAtool]
                ###start to sample
                ### matchedPair.set(commit, project,SAtool)

        for i in range(sampledSize):
            sampledFile = sample(xmlFileList, 1)[0]
            #print(f"sampledFile:{sampledFile}")
            filePath = os.path.join(folderPath, sampledFile)

            commit = str(sampledFile).replace(".xml", "")
            matchedPairs = MatchedPairsReader(filePath)
            sampledPair = sample(matchedPairs,1)[0]
            sampledPair.setOthers(commit, project, SAtool)
            if commit+str(sampledPair.number) not in sampledRecord:
                sampledPairs.append(sampledPair)
                sampledRecord.append(commit + str(sampledPair.number))
                print(sampledPair)
        wrtieToXML(sampledPairs, savedPath)


    return sampledPairs

### set format and save as a xml file
def wrtieToXML(sampledPairs,filename):  ##
    ###create dom
    doc = Document()
    ###create node
    matchedPairsList = doc.createElement('MatchedPairsList')
    doc.appendChild(matchedPairsList)
    for i in range(len(sampledPairs)):
        matchedPair = doc.createElement('MatchedPair')

        num = doc.createElement('Number')
        commit = doc.createElement("Commit")
        project = doc.createElement("Project")
        SAtool = doc.createElement("SAtool")

        num_text = doc.createTextNode(sampledPairs[i].number)
        commit_text = doc.createTextNode(sampledPairs[i].commit)
        project_text = doc.createTextNode(sampledPairs[i].project)
        SAtool_text = doc.createTextNode(sampledPairs[i].SAtool)

        num.appendChild(num_text)
        commit.appendChild(commit_text)
        project.appendChild(project_text)
        SAtool.appendChild(SAtool_text)

        matchedPair.appendChild(num)
        matchedPair.appendChild(project)
        matchedPair.appendChild(commit)
        matchedPair.appendChild(SAtool)

        pa = doc.createElement('ParentWarning')

        paBugDescription = doc.createElement('BugDescription')
        paBugDescription_text = doc.createTextNode(sampledPairs[i].paBugDescription)
        paBugDescription.appendChild(paBugDescription_text)

        paClass = doc.createElement('Class')
        paClass_text = doc.createTextNode(sampledPairs[i].paClass)
        paClass.appendChild(paClass_text)

        paMethod = doc.createElement('Method')
        paMethod_text = doc.createTextNode(sampledPairs[i].paMethod)
        paMethod.appendChild(paMethod_text)

        paField = doc.createElement('Field')
        paField_text = doc.createTextNode(sampledPairs[i].paField)
        paField.appendChild(paField_text)

        paSourcePath = doc.createElement('SourcePath')
        paSourcePath_text = doc.createTextNode(sampledPairs[i].paSourcePath)
        paSourcePath.appendChild(paSourcePath_text)

        paStart = doc.createElement('Start')
        paStart_text = doc.createTextNode(sampledPairs[i].paStart)
        paStart.appendChild(paStart_text)

        paEnd = doc.createElement('End')
        paEnd_text = doc.createTextNode(sampledPairs[i].paEnd)
        paEnd.appendChild(paEnd_text)



        pa.appendChild(paBugDescription)
        pa.appendChild(paClass)
        pa.appendChild(paMethod)
        pa.appendChild(paField)
        pa.appendChild(paSourcePath)
        pa.appendChild(paStart)
        pa.appendChild(paEnd)



        ch = doc.createElement('ChildWarning')

        chBugDescription = doc.createElement('BugDescription')
        chBugDescription_text = doc.createTextNode(sampledPairs[i].chBugDescription)
        chBugDescription.appendChild(chBugDescription_text)

        chClass = doc.createElement('Class')
        chClass_text = doc.createTextNode(sampledPairs[i].chClass)
        chClass.appendChild(chClass_text)

        chMethod = doc.createElement('Method')
        chMethod_text = doc.createTextNode(sampledPairs[i].chMethod)
        chMethod.appendChild(chMethod_text)

        chField = doc.createElement('Field')
        chField_text = doc.createTextNode(sampledPairs[i].chField)
        chField.appendChild(chField_text)

        chSourcePath = doc.createElement('SourcePath')
        chSourcePath_text = doc.createTextNode(sampledPairs[i].chSourcePath)
        chSourcePath.appendChild(chSourcePath_text)

        chStart = doc.createElement('Start')
        chStart_text = doc.createTextNode(sampledPairs[i].chStart)
        chStart.appendChild(chStart_text)

        chEnd = doc.createElement('End')
        chEnd_text = doc.createTextNode(sampledPairs[i].chEnd)
        chEnd.appendChild(chEnd_text)

        ch.appendChild(chBugDescription)
        ch.appendChild(chClass)
        ch.appendChild(chMethod)
        ch.appendChild(chField)
        ch.appendChild(chSourcePath)
        ch.appendChild(chStart)
        ch.appendChild(chEnd)

        matchedPair.appendChild(pa)
        matchedPair.appendChild(ch)

        matchedPairsList.appendChild(matchedPair)
    with open(filename,'wb') as f:
        f.write(doc.toprettyxml(indent='\t', encoding='utf-8'))
    return
###1.read matched pairs
#matchedPairs = MatchedPairsReader(r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/test.xml")



###2.sample process
####1) scan len of files:
def main():
    kafkaSpfolderPath = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList"
    kafkaPMDfolderPath =r""
    jcloudsSpfolderPath = r""
    jcloudsPMDfolderPath = r""
    sampledSavePath = r"/Users/lijunjie/Desktop/Git/FixPatternMining/master/FixPatternMining/CommitList/sampledMatchedPairs"
    sampledNumber = 3
    kafka = "kafka"
    jclouds = "jclouds"
    Spotbugs = "Spotbugs"
    PMD = "PMD"


    infoDic = {"kafka_Spotbugs":[kafkaSpfolderPath,kafka, Spotbugs],"kafka_PMD":[kafkaPMDfolderPath,kafka, PMD],"jclouds_Spotbugs":[jcloudsSpfolderPath,jclouds, Spotbugs],"jclouds_PMD":[jcloudsPMDfolderPath,jclouds, PMD]}
    sampleMatchedPairsFromFolder(infoDic["kafka_Spotbugs"][0], sampledSavePath, sampledNumber, infoDic["kafka_Spotbugs"][1], infoDic["kafka_Spotbugs"][2])



####2) scan len matched pairs of each file:
####3)pick up one file and one matched pairs

###3.write to the file

main()

