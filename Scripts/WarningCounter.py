import csv
import pandas as pd


commit_list_path = r'D:\ThesisProject\findbugsanalysis\FixPatternMining\CommitList\Guava2000commitList.txt'
pmd_results_path = r'D:\ThesisData\OriginalResults\PMD\guava'
spotbugs_results_path = r'D:\ThesisData\OriginalResults\Spotbugs\guava'



with open(commit_list_path) as commit_list_file:
    commit_list = commit_list_file.read().splitlines()


def count(results_path):
    gone_count = 0
    is_gone_count = 0
    new_count = 0
    is_new_count = 0
    fail_count = 0

    for i in range(2000 - 1):
        gone_file_path = results_path + '/gone/' + commit_list[i][:7] + '_' + commit_list[i + 1][:7] + '_gone_warnings.csv'
        new_file_path = results_path + '/new/' + commit_list[i][:7] + '_' + commit_list[i + 1][:7] + '_new_warnings.csv'

        try:
            with open(gone_file_path) as file:
                reader = csv.reader(file)
                temp_gone_count = len([line for line in reader]) - 1
                if temp_gone_count > 0:
                    gone_count += temp_gone_count
                    is_gone_count += 1

            with open(new_file_path) as file:
                reader = csv.reader(file)
                temp_new_count = len([line for line in reader]) - 1
                if temp_new_count > 0:
                    new_count += temp_new_count
                    is_new_count += 1

        except FileNotFoundError:
            fail_count += 1

    print('gone count', gone_count)
    print('commits with gone count', is_gone_count)
    print('new count', new_count)
    print('commits with new count', is_new_count)
    print('analyzed count', 2000 - fail_count)
    print('fail count', fail_count)


print('pmd')
count(pmd_results_path)
print('\nspotbugs')
count(spotbugs_results_path)
