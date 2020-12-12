'''
    Instructions to use:
        python3.7 insert_q2md.py

    Note:
        you can modify the variable in the file:  eye_test_csv = 'Chat bot testing - Chat bot answers.csv'

purpose is to convert the test questions in 'Chat bot testing - Chat bot answers.csv' to nlu.md

'''

import yaml
from datetime import datetime
import os
import pandas as pd
import numpy as np
import copy
import math

VERSION = "0.1"


def intent_string_processing(input_str):
    # consider how to hand ' ' & ' and ' & ()
    lower_str = (str(input_str).strip()).lower()
    filter_str = lower_str.replace(' and ', '_')
    filter_str = filter_str.replace('(', '_')
    filter_str = filter_str.replace(')', '')
    filter_str = filter_str.replace(' ', '')
    filter_str = filter_str.replace('-', '')
    filter_str = filter_str.replace('/', '_')
    return filter_str

def answer_string_processing(input_str):
    # answer cannot have ':'
    lower_str = input_str
    filter_str = lower_str.replace(':', '')
    filter_str = filter_str.replace('*', '')
    filter_str = filter_str.replace('"', "'")
    filter_str = filter_str.replace('“', "'")
    import re
    filter_str = re.sub(r'[^\x00-\x7F]', '', filter_str)
    filter_str = filter_str.replace('\r\n', '\n')
    # filter_str = filter_str.replace('\n', '\n\t\t')
    filter_str = '"' + filter_str + '"'
    return filter_str

def get_intent_from_3columns(Category, Sub_Category, Disease_Cate):
    column_separator = '-'
    intent = intent_string_processing(Category) + column_separator + \
             intent_string_processing(Sub_Category) + column_separator + \
             intent_string_processing(Disease_Cate)
    return intent


def nlu_write(intent_dict, nlu_md):
    '''
    Args:
        intent_name:
        storys_md:

    Returns:
        ## intent:affirm
        - yes
        - yes sure
    '''

    # dict_sample = {'intent_1': {'questions': ['a', 'b', 'c'], 'answer': 'answer1', 'QuestionID': '1'}}
    train_file = nlu_md
    if os.path.isfile(train_file):
        C = open(train_file, 'w')   # 'a+'
    else:
        C = open(train_file, 'w')

    for intent_name in intent_dict.keys():
        arg_str = ""
        # for the header
        arg_str += ("\n## intent: %s\n" % (intent_name))
        question_list = intent_dict[intent_name]['questions']
        for question in question_list:
            arg_str += ("- %s\n" %(question))

        C.write(arg_str)


# main entry
if __name__ == "__main__":
    # with a existing folder as a default
    seed_data_root = './'
    eye_test_csv = 'Chat bot testing - Chat bot answers.csv'
    nlu_file = 'nlu_new.md'
    orig_nlu_file = 'nlu.md'

    meta_path = os.path.join(seed_data_root, '../', eye_test_csv)
    # meta = pd.read_excel(meta_path)
    meta = pd.read_csv(meta_path)

    # list_file = df_master['Image location']
    list_question = meta['Question']
    list_true_ques = meta["the query's corresponding  standar question of the buildded dataset"]
    list_checkID = meta['Question in standar DatatSet (YES=1 or NO=0)']

    orig_nlu_path = os.path.join(seed_data_root, 'data', orig_nlu_file)
    print("read the original md file: ", orig_nlu_path)

    record_num = len(list_question)
    print("there are {} test questions in {} file" .format(record_num, meta_path))

    intents_dict = {}
    # dict_sample = {'intent_1': {'questions': ['a', 'b', 'c'], 'answer': 'answer1', 'QuestionID': '1'}}


    input = open(orig_nlu_path)
    nlu_path = os.path.join(seed_data_root, 'data', nlu_file)
    C = open(nlu_path, 'w')
    line_num = 0
    insert_num = 0
    for line in input:
        line_num += 1
        arg_str = ""
        arg_str += line
        # every question will show once
        # example: '- Will astigmatism heal by itself?'
        insert_flag = False
        for idx, correct_question in enumerate(list_true_ques):
            if math.isnan(list_checkID[idx]) is False and list_question[idx] is not np.nan and str(list_question[idx]).strip() != '':
                # print(list_checkID[idx])
                if int(list_checkID[idx]) == 1:
                    continue
                if correct_question in line:
                    insert_num += 1
                    arg_str += ("- %s\n" % (list_question[idx]))
                    insert_flag = True
        if insert_flag:
            print(arg_str)

        C.write(arg_str)

    # write intents_dict to files
    nlu_write(intents_dict, nlu_file)
    print("there are {} lines in {} file".format(line_num, orig_nlu_path))
    print("Insert {} lines to {} file".format(insert_num, nlu_path))

    print("\nend of the program!!!")
