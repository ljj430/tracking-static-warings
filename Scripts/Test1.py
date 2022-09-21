#import ToolsRunner.PMDRunner as pRunner

import os
import sys
sys.path.append('../')
from Utils import checkout as checkout
import Utils as utils
import XMLreader as xmlreader
from BugInstance import BugInstance
from random import sample
import jpype
from git import Repo
from git.compat import defenc
import re
from BugInstance import BugInstance

import os
import XMLreader as xmlreader
import hashlib
from Utils import Diff

from hungarian_algorithm import algorithm
from munkres import Munkres, print_matrix
import sys,os
import numpy as np

###1.using an example to generate matrix
####1) pick up an example(one from spotbugs one from PMD)
####2) implement the matrix generator
###2.apply Munkres on the matrix in improved algorithm(only on location matching )
####1) ensure matrix generator that works well and remove exact matching.
###3.measure time on different matching orderings
####1) record time consumption(original and improved ALG)




if __name__ == "__main__":
    #"classpath 'org.scoverage:gradle-scoverage:2.1.0'"->"classpath 'org.scoverage:gradle-scoverage:2.5.0'"
    os.chdir(r"D:\ThesisProject\trackingProjects\kafka")
    with open(r"build.gradle","r+") as f:
        text = f.readlines()

        for i in range(len(text)):
            if "classpath 'org.scoverage:gradle-scoverage:2.1.0'" in text[i]:
                print(i)
                text[i] = "    classpath 'org.scoverage:gradle-scoverage:2.5.0'\n"
    with open(r"build.gradle","w+") as f:
        f.writelines(text)
    with open(r"a.txt", "a+") as ff:
        ff.writelines('123')
###MUNKRES
# m = Munkres()
# indexes = m.compute(cost_matrix)
# print_matrix(matrix,msg='Lowest cost through this matrix:')
# total = 0
# for row, column in indexes:
# 	value = matrix[row][column]
# 	total += value
# 	print(f'({row},{column}) -> {value}')
# print(f'total cost:{total}')






