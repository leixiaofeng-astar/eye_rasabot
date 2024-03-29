import os
import pandas as pd
import requests
import csv
import re
import ast
import spacy
import re
import yaml
import argparse
from find_actions import action_find_information,action_find_symptoms_information,action_find_disease_causes,action_find_disease_treatment,action_find_surgical_treatment

'''
Rasa test file with --input as trainfile, --test as testfile, --get_acc as top1/top3 acc output

Please first start by  rasa run action and rasa run -m models --enable-api --cors * --debug

and run python test_rasa.py to start testing
'''


def arg_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='train_file',
                        help='the train database csvfile',
                        type=str, default="Eye_update_16Jun2021.csv")
    parser.add_argument('--test', dest='test_file',
                        help='the test csv file',
                        type=str, default="dreye_test_16Jun21.csv")
    parser.add_argument('--yamlfile', dest='yamlfile',
                        help='the nlu yaml file',
                        type=str, default="../domain.yml")
    parser.add_argument('--get_acc', dest='get_acc',
                        help='ger top1 or top3 acc',
                        type=str, default="top1")
    return parser.parse_args()

def get_expect_answer(test_expect_questions, train_Q_list, train_A_list):
    total_Q = len(train_Q_list)
    assert(total_Q == len(train_A_list))
    for idx, q in enumerate(train_Q_list):
        if q == test_expect_questions:
            return train_A_list[idx]

    print("Wrong corresponding standard question: ", test_expect_questions)
    return 'NA'
    
def generate_sender(question):
    # generate sender loops
    num_question = len(question)
    sender = range(0,num_question)
    print(type(sender))
    return sender

def select_text(ans_text):
    index=[i.start() for i in re.finditer('"', ans_text)]
    print(index)
    return index[6]

def parse_answer(sender,question):
    payload = {"sender": sender, "message": question}
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:5005/webhooks/rest/webhook', json=payload, headers=headers)
    print(r.text)
    if len(r.text)>=7:
        print('yes')
        ans_start = select_text(r.text)
        ans = r.text[ans_start+1 : -4]
        print(ans)
    else:
        ans = 'empty'
    return ans

def parse_confidence(question):
    payload = {'text':question}
    headers = {'content-type': 'application/json'}
    r = requests.post('http://localhost:5005/model/parse', json=payload, headers=headers)
    return r.text
    
def get_answer(question_list):
    sender=generate_sender(question_list)
    answers = []
    for i,j in zip(sender,question_list):
        print(j)
        ans=parse_answer(i,j)
        answers.append(ans)
    return answers

def get_confidence(question_list):
    confidences = []
    for i in question_list:
        conf=parse_confidence(i)
        confidences.append(conf)
    return confidences

def clean_text(text):
    comp = re.compile('[^A-Z^a-z^0-9^ ]')
    return comp.sub('', text)


def load_yaml(yamlfile):
    with open(yamlfile, 'r') as f:
        nlufile = yaml.load(f.read())['responses']
    return nlufile

def get_top_3_answer(nlufile, intent_list):
    action_list = ['find_condition_definitions', 'find_medical_symptoms', 'find_disease_causes',
                'find_disease_treatment', 'find_surgical_treatment']
    top_3_answer_list = []
    #import pdb;pdb.set_trace()
    nlu_keys = [key[6:] for key in nlufile.keys()]
    for intent in intent_list:
        if intent in action_list:
            if intent == 'find_condition_definitions':
                ans_content = action_find_information()
            if intent == 'find_medical_symptoms':
                ans_content = action_find_symptoms_information()
            if intent == 'find_disease_causes':
                ans_content = action_find_disease_causes()
            if intent == 'find_disease_treatment':
                ans_content = action_find_disease_treatment()
            if intent == 'find_surgical_treatment':
                ans_content = action_find_surgical_treatment()
        if intent in nlu_keys:
            nlu_ans = nlufile['utter_'+intent][0]
            ans_content = nlu_ans['text']
        else:
            ans_content = str('none')
        print(ans_content)
        top_3_answer_list.append(clean_text(ans_content))
    return top_3_answer_list

def vector_similarity(vector1, vector2):
    from scipy.spatial import distance
    result = 1-distance.cosine(vector1, vector2)
    return result

def nlp_handle_get():
    spacy_pipeline = "en_core_web_lg"
    # Note: install it with "python3 -m spacy download en_core_web_lg"
    nlp = spacy.load(spacy_pipeline)
    return nlp

def clacluateDistance(nlp, txt1, txt2):
    vector1 = nlp(txt1).vector
    vector2 = nlp(txt2).vector
    ret = vector_similarity(vector1, vector2)
    #print("similarity: {}" .format(ret))
    return ret


def cal_levenshtein_acc(nlp, chatbot_ans, standard_ans):
    count = 0
    lev_label = []
    greeting_answer_count = 0
    for i,j in zip(chatbot_ans, standard_ans):
        ret = clacluateDistance(nlp, i,j)
        if ret>0.99:
            count += 1
            lev_label.append('correct')
        else:
            lev_label.append('incorrect')
        greeting_answer = check_greeting_answer(i)
        greeting_answer_count += greeting_answer
    return count, lev_label, greeting_answer_count


def cal_top3_levenshtein_acc(nlp, chatbot_ans, standard_ans_list):
    count = 0
    lev_label = []
    all_score = []
    max_score_id = []
    greeting_answer_count = 0
    #import pdb;pdb.set_trace()
    for i_list, j in zip(chatbot_ans, standard_ans_list):
        score = []
        for i in i_list:
            ret = clacluateDistance(nlp, i,j)
            score.append(ret)
        if max(score) > 0.99:
            count += 1
            lev_label.append('correct')
            i_list[score.index(max(score))]
        else:
            lev_label.append('incorrect')
        greeting_answer = check_greeting_answer(i_list[score.index(max(score)])
        greeting_answer_count += greeting_answer
        max_score_id.append(score.index(max(score)))
        all_score.append(max(score))
    return all_score, count, lev_label, max_score_id, greeting_answer_count

def check_greeting_answer(answer):
    greeting_answer = 0
    greeting_answer = ["Dr.Eye here, I'm sorry, Please help to check your question and enter it again",
                       "Please check your question and enter it again",
                       "I'm sorry, I didn't quite understand that. Could you rephrase",
                       "Thank you for contacting us! Your question is beyond the range of this bot, could you enter your question again",
                       ]
    if answer in greeting_answer:
        greeting_answer=1
    
    return greeting_answer


if __name__ == '__main__':
    args = arg_parse()
    train_file = args.train_file
    test_file = args.test_file
    yamlfile = args.yamlfile
    get_acc = args.get_acc
    
    train_data = pd.read_csv(train_file)
    train_data.dropna(axis=0, how='all', inplace=True)
    test_data = pd.read_csv(test_file)
    test_expect_question = test_data['corresponding standard question'].tolist()
    question_list = test_data['Question'].tolist()
    
    test_expect_question = test_expect_question
    question_list = question_list
    train_Q_list = train_data['Question'].tolist()
    train_A_list = train_data['Answer'].tolist()

    
    nlufile = load_yaml(yamlfile)
    nlp = nlp_handle_get()
    clean_expect_answer = [clean_text(get_expect_answer(i, train_Q_list, train_A_list)) for i in test_expect_question]
    #clean_expect_answer = [clean_text(i) for i in expect_answer]
    

    question_list = question_list
    clean_expect_answer = clean_expect_answer

 
    if get_acc == 'top1':
        answer_list = get_answer(question_list)
        clean_answer = [clean_text(i) for i in answer_list]
        levenshtein_count,lev_label, greeting_answer_count = cal_levenshtein_acc(nlp, clean_answer, clean_expect_answer)
        result_top1 = {'question': question_list, 'chatbot_answer': clean_answer, 'expect_answer': clean_expect_answer}
        df = pd.DataFrame(result_top1, columns = ['question', 'chatbot_answer', 'expect_answer'])
        df.to_csv('result_top1.csv')
        print('Accuracy of TOP1 test:{} --[{}:{}]'.format(levenshtein_count/len(answer_list), levenshtein_count,
                                                              len(answer_list) - levenshtein_count))
        print('Accuracy of real answer test:{} --[{}:{}]'.format(levenshtein_count /(len(answer_list) - greeting_answer_count),
                                                          levenshtein_count,
                                                          len(answer_list) - greeting_answer_count -levenshtein_count))
    if get_acc == 'top3':
        confidences = get_confidence(question_list)
        confidence_1 = []
        confidence_2 = []
        confidence_3 = []
        answer_list = []
        intent_1 = []
        intent_2 = []
        intent_3 = []
        for confidence in confidences:
            print()
            print(confidence)
            confidence = confidence.replace('null', '123456')
            confidence = eval(confidence)
            rank = confidence["intent_ranking"]
            intent_sub_list = []
            confidence_list = []
            #import pdb;pdb.set_trace()
            if len(rank) >= 3:
                for r in rank[0:3]:
                    intent = r['name']
                    intent_sub_list.append(intent)
                    score = r['confidence']
                    confidence_list.append(score)
            else:
                for r in rank:
                    intent = r['name']
                    intent_sub_list.append(intent)
                    score = r['confidence']
                    confidence_list.append(score)

            top_3_answer_list = get_top_3_answer(nlufile, intent_sub_list)
            answer_list.append(top_3_answer_list)
            intent_1.append(intent_sub_list[0])
            intent_2.append(intent_sub_list[1])
            intent_3.append(intent_sub_list[2])
            confidence_1.append(confidence_list[0])
            confidence_2.append(confidence_list[1])
            confidence_3.append(confidence_list[2])

        top_1 = [ans[0] for ans in answer_list]
        top_2 = [ans[1] for ans in answer_list]
        top_3 = [ans[2] for ans in answer_list]
        #import pdb;pdb.set_trace()
        print(len(answer_list))
        score, levenshtein_count, lev_label, max_score_id, greeting_answer_count = cal_top3_levenshtein_acc(nlp, answer_list, clean_expect_answer)
        print('Accuracy of TOP3 test:{} --[{}:{}]'.format(levenshtein_count/len(answer_list),levenshtein_count,len(answer_list) - levenshtein_count))
        print('Accuracy of real answer test:{} --[{}:{}]'.format(levenshtein_count /(len(answer_list) - greeting_answer_count),
                                                          levenshtein_count,
                                                          len(answer_list) - greeting_answer_count -levenshtein_count))
        print(len(question_list), len(score), len(clean_expect_answer)) 

        result_top3 = {'question': question_list,
                       'score': score,
                       'max_score_id': max_score_id, 
                       'top_1_answer': top_1, 'intent_1': intent_1, 'confidence_1': confidence_1, 
                       'top_2_answer': top_2, 'intent_2': intent_2, 'confidence_2': confidence_2, 
                       'top_3_answer': top_3, 'intent_3': intent_3, 'confidence_3': confidence_3, 
                       'expect_answer': clean_expect_answer}
        df = pd.DataFrame(result_top3, columns = ['question',
                                                  'score',
                                                  'max_score_id',
                                                  'top_1_answer',
                                                  'intent_1',
                                                  'confidence_1',
                                                  'top_2_answer',
                                                  'intent_2',
                                                  'confidence_2',
                                                  'top_3_answer',
                                                  'intent_3',
                                                  'confidence_2',
                                                  'expect_answer'])
        df.to_csv('result_top3.csv')