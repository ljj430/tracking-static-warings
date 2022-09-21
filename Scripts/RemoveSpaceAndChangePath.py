

def stripFile(file, old_str_list, new_str_list):
    '''remove space in <>'''
    file_data = ""
    with open(file, "r", encoding = "utf-8") as f:
        for line in f:
            if old_str_list[0] in line:
                line = line.replace(old_str_list[0], new_str_list[0])
            elif old_str_list[1] in line:
                line = line.replace(old_str_list[1], new_str_list[1])
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)
def changePath(file):
    '''xxx/xxx/java/org/xxx  -> org/xxx'''



if __name__ == "__main__":
    old_str_list = ["Matched Pairs List","Matched Pair"]
    new_str_list = ["MatchedPairsList","MatchedPair"]
    stripFile(r"D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\test.xml", old_str_list,new_str_list)