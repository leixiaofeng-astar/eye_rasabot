'''

    Generates rasa training data from eye bot csv or excel table
    1) convert eye bot questions to train meta -- nlu.md
    2) add intent, actions and response to domain.yml
    2) add story for each question%answer -- stories.md

    Instructions to use:
        python3.7 table_2_mdyml.py

    Note:
        the FAQ file is hard-code in './eye_update_1020.csv'
        you can modify the variable in the file:  eye_faq_csv = 'eye_update_1020.csv'

purpose is to update 3 rasa support documents for training
task 1:
add intent by -- Answer	Category	Sub_Category	Disease_Cate
list all the Question in nlu-add.md
## intent:affirm
- yes
- yes sure

task 2:
add intents in domain-add.md
intents:
- search_information

list actions with utter_xxx  xxx is intent
actions:
- utter_search_information

list responses with utter_xxx  xxx is intent
put actions and answer as below
responses:
  utter_search_information:
  - text: The address is {facility_address}.

task 3:
add conversation in stories-add.md
conversation name with story_xxx  xxx is intent
## story_search_information
* search_information
    - utter_search_information


'''

import yaml
from datetime import datetime
import os
import pandas as pd
import copy

VERSION = "0.2"


# with a existing folder as a default
seed_data_root = './'
eye_faq_csv = 'eye_update_1020.csv'
nlu_file = 'nlu_add.md'
story_file = 'storys_add.md'
domain_file = 'domain_add.md'


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

def save_to_excel(DATA_CSV_TABLE):
    # df2 = pd.DataFrame({"ID": patient_id,
    #                     "RL": RL,
    #                     "ID_RL": id_rl,
    #                     })
    # ## still have to group by to select one out of mulitple images if they exist
    # df2.to_csv(DATA_CSV_TABLE, index=False)
    print("write excel here!")


def header_arg2():
    # to print the main()
    arg_str = ""
    # for the header
    arg_str += ("\nif __name__ == \"__main__\":\n")
    arg_str += ("    args = parse_args()\n")
    arg_str += ("    print(args)\n\n")
    return arg_str


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
        C = open(train_file, 'a+')
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


def domain_write(intent_dict, domain_yml):
    '''

    Args:
        intent_name:
        storys_md:

    Returns:
        intents:
        - search_information

        actions:
        - utter_search_information

        responses:
          utter_search_information:
          - text: the answer of xxx is .
    '''

    # dict_sample = {'intent_1': {'questions': ['a', 'b', 'c'], 'answer': 'answer1', 'QuestionID': '1'}}
    train_file = domain_yml
    if os.path.isfile(train_file):
        C = open(train_file, 'a+')
    else:
        C = open(train_file, 'w')

    intent_list = intent_dict.keys()
    # for the header
    arg_str = ""
    arg_str += ("\nintents:\n")
    for intent_name in intent_list:
        arg_str += ("- %s\n" % (intent_name))
    C.write(arg_str)

    # for the header
    arg_str = ""
    arg_str += ("\n\nactions:\n")
    for intent_name in intent_list:
        arg_str += ("- utter_%s\n" % (intent_name))
    C.write(arg_str)

    # for the header
    arg_str = ""
    arg_str += ("\n\nresponses:")
    for intent_name in intent_dict.keys():
        arg_str += ("\n  utter_%s:\n" % (intent_name))
        arg_str += ("  - text: %s\n" % (intent_dict[intent_name]['answer']))

    C.write(arg_str)


def storys_write(intent_dict, storys_md):
    '''
    Args:
        intent_name:

    Returns:
        ## story_out_of_scope
        * out_of_scope
            - utter_out_of_scope
    '''
    intent_list = intent_dict.keys()
    train_file = storys_md
    if os.path.isfile(train_file):
        C = open(train_file, 'a+')
    else:
        C = open(train_file, 'w')

    for intent_name in intent_list:
        arg_str = ""
        # for the header
        arg_str += ("\n## story_%s\n" %(intent_name))
        arg_str += ("* %s\n" %(intent_name))
        arg_str += ("    - utter_%s\n" %(intent_name))
        C.write(arg_str)



# main entry
if __name__ == "__main__":
    meta_path = os.path.join(seed_data_root, eye_faq_csv)
    # meta = pd.read_excel(meta_path)
    meta = pd.read_csv(meta_path)

    nlu_file = 'nlu_add.md'
    story_file = 'storys_add.md'
    domain_file = 'domain_add.yml'
    nlu_path = os.path.join(seed_data_root, nlu_file)
    story_path = os.path.join(seed_data_root, story_file)
    domain_path = os.path.join(seed_data_root, domain_file)

    # QuestionID Question	Stander Question	Answer	Category	Sub_Category	Disease_Cate

    # list_file = df_master['Image location']
    list_question = meta['Question']
    list_answer = meta['Answer']
    list_checkID = meta['QuestionID']

    # TODO -- some answer with same Category&Sub_Category&Disease_Cate
    #  --> need to check QuestionID to distinguish intent
    list_catagory = meta['Category']
    list_sub_catagory = meta['Sub_Category']
    list_disease_catagory = meta['Disease_Cate']

    record_num = len(list_question)
    print("there are {} records in {} file" .format(record_num, meta_path))

    intents_dict = {}
    # dict_sample = {'intent_1': {'questions': ['a', 'b', 'c'], 'answer': 'answer1', 'QuestionID': '1'}}

    for idx, record in enumerate(list_question):
        questionID = str(list_checkID[idx])
        intent_answer = answer_string_processing(str(list_answer[idx]))
        intent_str = get_intent_from_3columns(list_catagory[idx], list_sub_catagory[idx], list_disease_catagory[idx])

        # import pdb
        # pdb.set_trace()
        if intent_str in intents_dict.keys():
            # Note: the intent could be same for 2 different answer
            # check if QuestionID is same for same intent
            tmp_intent_ques_list = intents_dict[intent_str]['questions']
            orig_questionID = intents_dict[intent_str]['QuestionID']
            if questionID == orig_questionID:
                tmp_intent_ques_list.append(list_question[idx])
                intents_dict[intent_str]['questions'] = tmp_intent_ques_list
            else:
                # this is a new intent or another existing intent
                new_intent_str = intent_str + "_" + str(questionID)
                if new_intent_str in intents_dict.keys():
                    tmp_intent_ques_list = intents_dict[new_intent_str]['questions']
                    tmp_intent_ques_list.append(list_question[idx])
                    intents_dict[intent_str]['questions'] = tmp_intent_ques_list
                else:
                    intents_dict[new_intent_str] = {}
                    intents_dict[new_intent_str]['answer'] = intent_answer
                    intents_dict[new_intent_str]['QuestionID'] = questionID
                    tmp_list = []
                    tmp_list.append(list_question[idx])
                    intents_dict[new_intent_str]['questions'] = tmp_list
        else:
            # add the question/answer/QuestionID to dict
            intents_dict[intent_str] = {}
            intents_dict[intent_str]['answer'] = intent_answer
            intents_dict[intent_str]['QuestionID'] = questionID
            tmp_list = []
            tmp_list.append(list_question[idx])
            intents_dict[intent_str]['questions'] = tmp_list

    # write intents_dict to files
    nlu_write(intents_dict, nlu_file)
    domain_write(intents_dict, domain_file)
    storys_write(intents_dict, story_file)

    print("there are {} intents in {} file".format(len(intents_dict.keys()), meta_path))

    print("\nend of the program!!!")
