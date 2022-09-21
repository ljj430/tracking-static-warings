import os
import pandas as pd

imporve_path = r"/Users/lijunjie/Downloads/matched_pairs/labeled_improved_approach_sampled_results"
original_path = r"/Users/lijunjie/Downloads/matched_pairs/labeled_SOA_approach_sampled_results"

project_list = ["Jclouds","Springboot","Guava","Kafka"]
project_list = ["Jclouds","Kafka"]
tool_list = ["PMD","Spotbugs"]

type_list = ["gone","new"]


def count_indepent_evaluation(improve_path):
    target_path = imporve_path
    t_count = {}
    f_count = {}
    all_count = {}
    for project in project_list:
        for tool in tool_list:
            for type in type_list:
                t_count[project + "_" + tool + "_" + type] = 0
                f_count[project + "_" + tool + "_" + type] = 0
                all_count[project + "_" + tool + "_" + type] = 0
                folder_path = os.path.join(os.path.join(target_path, project + "_" + tool), type)
                file_list = os.listdir(folder_path)
                for file in file_list:
                    file_path = os.path.join(folder_path, file)
                    data_df = pd.read_csv(file_path)

                    # t_df = data_df[(data_df['FP/TP'] == 'T') | (data_df['FP/TP'] == 't')]
                    f_df = data_df[(data_df['FP/TP'] == 'F') | (data_df['FP/TP'] == 'f')]

                    # t_count[project + "_" + tool + "_" + type] += len(t_df)
                    f_count[project + "_" + tool + "_" + type] += len(f_df)
                    all_count[project + "_" + tool + "_" + type] += len(data_df)
    # for key, value in t_count.items():
    #     print(f"{key}:{value}")
    for key, value in f_count.items():
        print(f"{key}:{value}")
    print()
    for key, value in all_count.items():
        print(f"{key}:{value}")
# count_indepent_evaluation()

def count_reason(imporve_path):
    dic_count = {}
    count_f_dic = {}
    left_count = 0
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    t5 = 0
    t6 = 0
    all = 0
    target_path = imporve_path
    for project in project_list:
        for tool in tool_list:
            for type in type_list:
                folder_path = os.path.join(os.path.join(target_path, project + "_" + tool), type)
                print(f"start: {project}:{tool}:{type}")
                count_f_dic[project + "_" + tool + "_" + type] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "1"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "2"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "3"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "4"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "5"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "6"] = 0

                file_list = os.listdir(folder_path)
                for file in file_list:
                    file_path = os.path.join(folder_path, file)
                    data_df = pd.read_csv(file_path)

                    for id, row in data_df.iterrows():
                        if row['FP/TP'] == 'f' or row['FP/TP'] == 'F':
                            count_f_dic[project + "_" + tool + "_" + type] += 1
                            # print(row["Reason"])
                            all += 1
                            if not pd.isna(row['Reason']):

                                if 'dense' in row["Reason"] or "Code_Shift" in row["Reason"] or "t4" == row["Reason"]:
                                    t4 += 1
                                    dic_count[project + "_" + tool + "_" + type + "_" + "4"] += 1


                                elif (('class' in row['Reason'] or "Class" in row["Reason"]) and "no changes" not in row[
                                    'Reason'] and "attribute" not in row['Reason'] and "Attribute" not in row[
                                    'Reason'] and "Method" not in row['Reason'] and "method" not in row[
                                    'Reason'] and 'no refactoring' not in row['Reason']) or "t1" == row["Reason"]:
                                    t1 += 1
                                    dic_count[project + "_" + tool + "_" + type + "_" + "1"] += 1

                                    # print(row['Reason'])
                                elif 'method' in row['Reason'] or "Method" in row['Reason'] or "t2" == row["Reason"]:
                                    t2 += 1


                                    dic_count[project + "_" + tool + "_" + type + "_" + "2"] += 1
                                    # print(row['Reason'])

                                elif 'attribute' in row['Reason'] or 'Attribute' in row['Reason']or 'parameter' in row['Reason'] or 'Variable' in row[
                                    'Reason'] or "t3" == row["Reason"]:
                                    t3 += 1

                                    dic_count[project + "_" + tool + "_" + type + "_" + "3"] += 1

                                elif 't5' == row['Reason']:
                                    t5+=1

                                    dic_count[project + "_" + tool + "_" + type + "_" + "5"] += 1
                                    print(file_path)
                                    print(f"id:{id}")
                                    print(row["Reason"])
                                    print()
                                elif 'code change' in row['Reason'] or 'mismatch' in row['Reason'] or "Code_Change" in \
                                        row['Reason'] or "fail to match" in row['Reason'] or 'Mismatch' in row['Reason'] \
                                        or 'Limitation' in row['Reason'] or 'No Change' in row[
                                    'Reason'] or 'no change' in row['Reason'] or 'No change' in row[
                                    'Reason'] or 'no refactoring' in row['Reason'] or 'wrong line' in row['Reason'] or "t6" == row["Reason"]:
                                    t6 += 1
                                    dic_count[project + "_" + tool + "_" + type + "_" + "6"] += 1

                                else:
                                    left_count += 1


                            else:

                                left_count +=1


                # print(f"count:{count_f_dic[project+'_'+tool+'_'+type]}")
                print()
    for key, value in dic_count.items():
        print(f"{key}:{value}")
    print(f"t1:{t1}\nt2:{t2}\nt3:{t3}\nt4:{t4}\nt5:{t5}\nt6:{t6}\nleft:{left_count}\nall:{all}")
original_path = r"/Users/lijunjie/Downloads/matched_pairs/labeled_SOA_approach_sampled_results"
project_list = ["Jclouds","Kafka"]
tool_list = ["PMD","Spotbugs"]
type_list = ["gone","new"]
imporve_path = r"/Users/lijunjie/Downloads/matched_pairs/labeled_improved_approach_sampled_results"
def updated_file(source_folder, target_folder):

    for project in project_list:
        for tool in tool_list:

            ## create a list

            for type in type_list:
                folder_path = os.path.join(os.path.join(source_folder, project + "_" + tool), type)
                print(f"start: {project}:{tool}:{type}")

                file_list = os.listdir(folder_path)
                for file in file_list:
                    file_path = os.path.join(folder_path, file)
                    data_df = pd.read_csv(file_path)
                    target_df = data_df.copy()
                    # print(target_df)
                    for id, row in data_df.iterrows():
                        if row['FP/TP'] == 'f' or row['FP/TP'] == 'F':
                            if not pd.isna(row['Reason']):
                                if 'dense' in row["Reason"] or "Code_Shift" in row["Reason"] or "t4" == row["Reason"]:
                                    reason = 't4'
                                    target_df.loc[id,'Reason'] = 't4'

                                elif (('class' in row['Reason'] or "Class" in row["Reason"]) and "no changes" not in row[
                                    'Reason'] and "attribute" not in row['Reason'] and "Attribute" not in row[
                                    'Reason'] and "Method" not in row['Reason'] and "method" not in row[
                                    'Reason'] and 'no refactoring' not in row['Reason']) or "t1" == row["Reason"]:
                                    reason = 't1'
                                    target_df.loc[id,'Reason'] = 't1'
                                elif 'method' in row['Reason'] or "Method" in row['Reason'] or "t2" == row["Reason"]:
                                    reason = 't2'
                                    target_df.loc[id, 'Reason'] = 't2'
                                elif 'attribute' in row['Reason'] or 'Attribute' in row['Reason']or 'parameter' in row['Reason'] or 'Variable' in row[
                                    'Reason'] or "t3" == row["Reason"]:
                                    target_df.loc[id,'Reason'] = 't3'
                                elif 't5' == row['Reason']:
                                    reason = 't5'
                                    target_df.loc[id,'Reason'] = 't5'
                                elif 'code change' in row['Reason'] or 'mismatch' in row['Reason'] or "Code_Change" in \
                                        row['Reason'] or "fail to match" in row['Reason'] or 'Mismatch' in row['Reason'] \
                                        or 'Limitation' in row['Reason'] or 'No Change' in row[
                                    'Reason'] or 'no change' in row['Reason'] or 'No change' in row[
                                    'Reason'] or 'no refactoring' in row['Reason'] or 'wrong line' in row['Reason'] or "t6" == row["Reason"]:
                                    reason = 't6'
                                    target_df.loc[id,'Reason'] = 't6'
                    project_path = os.path.join(target_folder, project + '_' + tool)
                    if not os.path.exists(project_path):
                        os.mkdir(project_path)
                    # tool_path = os.path.join(project_path,tool)
                    # if not os.path.exists(tool_path):
                    #     os.mkdir(tool_path)
                    type_path = os.path.join(project_path,type)
                    if not os.path.exists(type_path):
                        os.mkdir(type_path)
                    target_path = os.path.join(type_path,file)

                    target_df.to_csv(target_path,index = False)

def updated_original(source_folder, target_folder):

    #read source_file
    # read target_file
    for project in project_list:
        for tool in tool_list:

            ## create a list

            for type in type_list:
                folder_path = os.path.join(os.path.join(source_folder, project + "_" + tool), type)
                print(f"start: {project}:{tool}:{type}")

                file_list = os.listdir(folder_path)
                for file in file_list:

                    # open target_file
                    target_path = os.path.join(os.path.join(target_folder, project + "_" + tool), os.path.join(type,file))
                    if not os.path.exists(target_path):
                        continue
                    else:
                        target_df = pd.read_csv(target_path)

                        file_path = os.path.join(folder_path, file)
                        data_df = pd.read_csv(file_path)
                        # print(target_df)
                        for id, row in data_df.iterrows():
                            if row['FP/TP'] == 'f' or row['FP/TP'] == 'F':
                                for t_id,t_row in target_df.iterrows():
                                    if t_row['Bug'] == row['Bug'] and t_row['class name'] == row['class name'] and t_row['method name'] == row['method name'] and t_row['field name'] == row['field name'] and t_row['source path'] == row['source path'] and  t_row['start'] == row['start'] and t_row['end'] == row['end']:
                                        print(file_path)
                                        data_df.loc[id,'Reason'] = t_row['Reason']
                    data_df.to_csv(file_path, index=False)
def another_count(imporve_path):
    dic_count = {}
    count_f_dic = {}
    left_count = 0
    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0
    t5 = 0
    t6 = 0
    all = 0
    target_path = imporve_path
    for project in project_list:
        for tool in tool_list:
            for type in type_list:
                folder_path = os.path.join(os.path.join(target_path, project + "_" + tool), type)
                print(f"start: {project}:{tool}:{type}")
                count_f_dic[project + "_" + tool + "_" + type] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "1"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "2"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "3"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "4"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "5"] = 0
                dic_count[project + "_" + tool + "_" + type + "_" + "6"] = 0

                file_list = os.listdir(folder_path)
                for file in file_list:
                    file_path = os.path.join(folder_path, file)
                    data_df = pd.read_csv(file_path)

                    for id, row in data_df.iterrows():
                        if row['FP/TP'] == 'f' or row['FP/TP'] == 'F':
                            count_f_dic[project + "_" + tool + "_" + type] += 1
                            # print(row["Reason"])
                            all += 1
                            if "FPs' category" in data_df.columns:
                                if not pd.isna(row["FPs' category"]):

                                    if row["FPs' category"] == 4:
                                        t4 += 1
                                        # data_df.loc[id,"Reason"] = 't4'
                                        dic_count[project + "_" + tool + "_" + type + "_" + "4"] += 1


                                    elif row["FPs' category"] == 1:
                                        t1 += 1
                                        # data_df.loc[id, "Reason"] = 't1'
                                        dic_count[project + "_" + tool + "_" + type + "_" + "1"] += 1

                                        # print(row['Reason'])
                                    elif row["FPs' category"] == 2:
                                        t2 += 1
                                        # data_df.loc[id, "Reason"] = 't2'
                                        dic_count[project + "_" + tool + "_" + type + "_" + "2"] += 1
                                        # print(row['Reason'])

                                    elif row["FPs' category"] == 3:
                                        t3 += 1
                                        # data_df.loc[id, "Reason"] = 't3'
                                        dic_count[project + "_" + tool + "_" + type + "_" + "3"] += 1
                                    elif row["FPs' category"] == 5:
                                        t5 += 1
                                        # data_df.loc[id, "Reason"] = 't5'
                                        dic_count[project + "_" + tool + "_" + type + "_" + "5"] += 1
                                    elif row["FPs' category"] == 6:
                                        t6 += 1
                                        # data_df.loc[id, "Reason"] = 't6'
                                        dic_count[project + "_" + tool + "_" + type + "_" + "6"] += 1

                                    else:
                                        left_count += 1
                                        print(file_path)
                                        print(f"id:{id}")
                                        print(row["Reason"])
                                        print()

                                else:
                                    print(file_path)
                                    print(f"id:{id}")
                                    print(row["Reason"])
                                    print()
                                    left_count += 1
                    # data_df.to_csv(file_path,index=False)
                # print(f"count:{count_f_dic[project+'_'+tool+'_'+type]}")
                print()
    for key, value in dic_count.items():
        print(f"{key}:{value}")
    print(f"t1:{t1}\nt2:{t2}\nt3:{t3}\nt4:{t4}\nt5:{t5}\nt6:{t6}\nleft:{left_count}\nall:{all}")
source_folder = r"/Users/lijunjie/Apps/static_replication/updated_pairs"
target_folder = r"/Users/lijunjie/Apps/static_replication/updated_pairs_improved"
# updated_file(source_folder, target_folder)
# count_indepent_evaluation(target_folder)
# count_reason(target_folder)
# updated_original(source_folder, target_folder)
# another_count(source_folder)
count_reason(source_folder)