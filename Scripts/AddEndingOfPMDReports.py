import os

####set your PMD repots Path
testPath = r'D:\tmp\test'
PMDPath = r"D:\ThesisData\Reports\PMD\guava"
g = os.walk(testPath)



addPMDList = []
addFileandPMDList = []
replacedList = [b"\xa2\xe2"]

for path,dir_list,file_list in g:
    count = 1
    for file_name in file_list:
        xmlPath = os.path.join(path, file_name)
        print(f"start to read {xmlPath} {count}/{len(file_list)}")
        count+=1
        with open(xmlPath, 'rb') as f1, open(f"{xmlPath}.bak", "wb") as f2:
            lines = f1.readlines()
            length = len(lines)
            for i in range(length):
                for token in replacedList:
                    lines[i] = lines[i].replace(token,b"")
                f2.write(lines[i])
                if i ==  (length-1):
                    if lines[i] != b'</pmd>\r\n' and lines[i] != b'</file>\r\n':
                        f2.write(b'</file>\r\n</pmd>\r\n')
                    elif lines[i] != b'</pmd>\r\n':
                        f2.write(b'</pmd>\r\n')
            # if last_line != b'</pmd>\r\n' and last_line != b'</file>\r\n':
            #     print(xmlPath)
            #     print(last_line)
            #     addFileandPMDList.append(xmlPath)
            # elif last_line != b'</pmd>\r\n':
            #     addPMDList.append(xmlPath)
        os.remove(xmlPath)
        os.rename(f"{xmlPath}.bak",xmlPath)

# print("###start to add###")
# for xmlPath in addFileandPMDList:
#     print(xmlPath)
#     with open(xmlPath,'ab') as f:
#         f.write(b'</file>\r\n</pmd>\r\n')
# for xmlPath in addPMDList:
#     print(xmlPath)
#     with open(xmlPath,'ab') as f:
#         f.write(b'</pmd>\r\n')

