from docx import Document
import pandas as pd
import numpy as np
import os
import re
import matplotlib.pyplot as plt
import pickle


def add_space(df):
    df['content'] = [x.lower() for x in df['content']]
    df['content'] = [re.sub('[-/]', ' ', x) for x in df['content']]
    df['content'] = [re.sub('[\,.;:▶]|\([\w\d]+\)', '', x) for x in df['content']]
    df['content'] = [re.sub('[\(\)]', '', x) for x in df['content']]
    df['content'] = [re.sub(' [b-zB-Z]{1} ', '', x) for x in df['content']]
    df['content'] = [re.sub('u s', 'us', x) for x in df['content']]
    df['content'] = [re.sub('[\'\"\&\@\”\“]', '', x) for x in df['content']]
    df['content'] = [re.sub('\n|\t|–', '', x) for x in df['content']]
    df['content'] = [re.sub('\u2002', '', x) for x in df['content']]
    df['content'] = [re.sub('\uf06f', '', x) for x in df['content']]
    # df['content']=[re.sub('$','$ ', x) for x in df['content']]
    df['content'] = [re.sub('(?<=\$)', ' ', x) for x in df['content']]
    df['content'] = [re.sub('(?<=\$)', ' ', x) for x in df['content']]
    # df['content']=[re.sub('([0-9]+)(?=h|k|km|am|)',' ', x) for x in df['content']]
    df['content'] = [re.sub('#_+', '', x) for x in df['content']]
    df['content'] = [re.sub('([0-9]+)([a-z]+)', r'\1' + ' ' + r'\2', x) for x in df['content']]
    df['content'] = [re.sub('([a-z]+)([0-9]+)', r'\1' + ' ' + r'\2', x) for x in df['content']]
    df['content'] = [re.sub('(?=%)', ' ', x) for x in df['content']]

    return df

def doc_tolist(doc,pdf_path,rules):
    batch_list=[]

    for i,d in enumerate(doc):
        for r_idx in range(1,6):
            res=re.search(rules[r_idx],d.lower())
            if res:# and len(d)>30:
                batch=[]

                if i-1>=0:# and len(doc[i-1])>30:
                    for j_idx in range(1,6):
                        if re.search(rules[j_idx],doc[i-1].lower()):
                            batch.append([i-1, doc[i-1], pdf_path, rules[j_idx]])
                            break
                    else:
                        batch.append([i - 1, doc[i - 1], pdf_path, 'other'])

                batch.append([i,d,pdf_path,rules[r_idx]])

                if i+1<len(doc):# and len(doc[i+1])>30:
                    for j_idx in range(1,6):
                        if re.search(rules[j_idx],doc[i+1].lower()):
                            batch.append([i+1, doc[i+1], pdf_path, rules[j_idx]])
                            break
                    else:
                        batch.append([i + 1, doc[i + 1], pdf_path, 'other'])

                batch_list.append(batch)

    return batch_list

def get_doc_list(dl,path):
#     print(path)
    document=None
    document = Document(path)
    doc=[x.text for x in document.paragraphs if not x.text.isspace() and len(x.text)>0]
    rules={1:'termination|terminate',
       2:'payment|pay|bill|billing',
       3:'solicitation|solicit',
       4:'insurance',
       5:'remedy'
      }
    dl+=doc_tolist(doc,path,rules)
    return dl

def main1():
    dl = []
    root_path = '../data/contract/docs'

    for d_name in os.listdir(root_path):

        if '.docx' in d_name:
            temp_path = os.path.join(root_path, d_name)
            dl = get_doc_list(dl, temp_path)


    # df = pd.DataFrame(dl, columns=['index', 'content', 'doc', 'label'])

    with open('../data/contract/df.pkl','wb') as f:
        pickle.dump(dl,f)

    with open('../data/contract/df.pkl','rb') as f:
        dl=pickle.load(f)

    batch_idx=0
    df=pd.DataFrame()
    for batch in dl:

        for d in batch:
            dd=[ [batch_idx,d[0],x,d[2],d[3]] for x in d[1].split('.') if not x.isspace() and len(x)>0]
            temp_df = pd.DataFrame(dd, columns=['batch_idx','paragrah_idx', 'content', 'doc', 'label'])
            df=df.append(temp_df)

        batch_idx+=1

    with open('../data/contract/raw_df.pkl','wb') as f:
        pickle.dump(df,f)

def main2():
    with open('../data/contract/raw_df.pkl','rb') as f:
        df=pickle.load(f)

    diction = {
        'other': 5,
        'termination|terminate': 0,
        'payment|pay|bill|billing': 1,
        'insurance': 2,
        'solicitation|solicit': 3,
        'remedy': 4
    }

    df['label'] = [diction[x] for x in df['label']]

    with open('../data/contract/clean_df.pkl','wb') as f:
        pickle.dump(df,f)

if __name__=='__main__':
    main2()