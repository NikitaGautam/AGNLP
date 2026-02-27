
from __future__ import print_function
from email import message
from re import search
import time
from tkinter import E
from types import NoneType
import woslite_client
from woslite_client.rest import ApiException
from pprint import pprint

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from collections import Counter
import re 
import concurrent.futures
        
#FOR WOS - From Rob 
from WOS import woseAPIclientQuery
from WOS import woseclient
import csv


#FOR WOS
import argparse
import pandas as pd 
from pyscopus import Scopus
import os
import pandas as pd
import time
import subprocess
import langid
import torch
from transformers import BertForSequenceClassification, BertTokenizer
from google import Scholar
import threading


import transformers
import torch
import os

class GetAllUrl:
    def __init__(self, keyword, alias, scopus_count, science_count, start, end, scholar_option, wos_count,all_words):
        self.base_url = "https://www.scopus.com/search/form.uri?display=advanced"
        self.keyword = keyword
        self.alias = alias
        self.scopus_count = int(scopus_count)
        self.science_count = int(science_count)
        self.scholar_option = int(scholar_option)
        self.script_path = 'run_scholar.sh'
        self.start = int(start)
        self.end =int(end)
        self.script_arguments = [self.keyword, self.alias, self.end, self.start]
        self.scholar_path = self.alias + "/DataYear"
        self.combined_path = self.alias+"/scholarall.csv"
        self.scholar_fil_path = self.alias+"/fil_scholarall.csv"
        self.scopus_files = self.alias + "/scopus-" + "abstracts.csv"
        self.sciencedirect_files = self.alias + "/sciencedirect-" + "abstracts.csv"
        self.final_path = self.alias + "/final_with_classifications.tsv"
        self.selected_files = self.alias + "/selected.tsv"

        self.selected_files_scopus = self.alias + "/scopus-selected.tsv"
        self.selected_files_scholar = self.alias + "/scholar-selected.tsv"
        self.selected_files_sciencedirect = self.alias + "/sciencedirect-selected.tsv"
        self.selected_files_wos = self.alias + "/wos-selected.tsv"
        
        self.wos_count = int(wos_count)
        self.url =  "https://www.webofscience.com/wos/woscc/full-record/"
        self.wos_files = self.alias + "/wos-" + "abstracts.csv"

        self.all_words = all_words

    def func1(self,):
        try:
            with open(self.wos_files, 'w') as fp:
                pass
            print("--------STARTING EXECUTION - Getting data from WOS--------")
            self.get_data_from_wos()
            print("--------WOS - Completed--------")

            # with open(self.selected_files_wos, 'w') as fp:
            #     pass
            # print("-----------FILTERING WOS DATA USING BERT MODEL---------")
            # self.filter_using_model_wos()
            return
        except Exception as ex:
            print("Error in web of science ---", ex)
            errors = "WOS="+str(ex)
            return errors
            errors.append("WOS="+str(ex))

    def func2(self,):
        try:
            with open(self.sciencedirect_files, 'w') as fp:
                pass 
            print("------STARTING EXECUTION - Getting data from Science Direct----")
            self.get_data_from_sciencedirect()
            print("--------SCIENCE DIRECT  - Completed--------")

            # with open(self.selected_files_sciencedirect, 'w') as fp:
            #     pass 
            # print("-----------FILTERING SCIENCE DIRECT DATA USING BERT MODEL---------")
            # self.filter_using_model_sciencedirect()
            return 

        except Exception as ex:
            print("Error in Science Direct")
            errors = "Science Direct="+ str(ex)
            return errors
            errors.append("Science Direct="+ str(ex))

    def func3(self,):
        try:
            with open(self.scopus_files, 'w') as fp:
                pass
            print("-----------STARTING EXECUTION - Getting data from SCOPUS--------------")
            self.get_data_from_scopus()
            print("--------SCOPUS - Completed--------")
            
            # with open(self.selected_files_scopus, 'w') as fp:
            #     pass 
            # print("-----------FILTERING SCOPUS DATA USING BERT MODEL---------")
            # self.filter_using_model_scopus()

            return 
        except Exception as ex:
            print("Error in scopus ---", ex)
            errors = "Scopus="+str(ex)
            return errors
            errors.append("Scopus="+str(ex))


    def start_execution(self,):
        fol_path = self.alias
        if not os.path.exists(fol_path):
            try:
                os.makedirs(fol_path)
            except OSError as e:
                print(f"Error: {e}")

        if self.scholar_option == 1:     
            fol_path = self.alias+"/DataYear"
            if not os.path.exists(fol_path):
                try:
                    os.makedirs(fol_path)
                except OSError as e:
                    print(f"Error: {e}")
                
            with open(self.scholar_fil_path, 'w') as fp: 
                pass
            
            with open(self.selected_files_scholar, 'w') as fp:
                pass
    

        errors = []  


        with concurrent.futures.ProcessPoolExecutor() as executor:
            futures = [executor.submit(self.func1), executor.submit(self.func2), executor.submit(self.func3)]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    result = future.result()  
                    if result:  
                        errors.append(result)
                except Exception as e:
                        errors.append(str(e)) 


        try:
            if self.scholar_option == 1:
                if self.end >= self.start:
                    try:
                        scholar = Scholar(self.start, self.end, self.keyword, self.alias)
                        scholar.scrapper_code()
                        time.sleep(10)
                
                    except Exception as ex:
                        print(ex)
                        # print("-------SLEEPING for 2 hours--------")
                        # time.sleep(7200)  
                    self.end -= 1
                    
                    self.post_process_scholar()
                    self.filter_using_model_scholar()  
                    
                    self.end = self.start - 1 
                        
                # print("-----------PROCESSING COLLECTED DATA---------")
                # self.post_process_collected_data()
                # print("-----------FILTERING USING BERT MODEL---------")
                
                self.filter_doi_combine_all()
                self.filter_using_model()
            print(f"-----------COMPLETED ALL PROCESS FOR KEYWORD: {self.keyword}---------")
        except Exception as ex:
            print("Error in Google Scholar ---", ex)
            errors.append("Google Scholar="+str(ex))

        ret = False
        message = f"Some Errors in the application: {errors}"
        if len(errors) == 0:
            message = "AllCompleted"
            ret = True

        # with open(self.selected_files, 'w') as fp:
        #     pass

        # with open(self.final_path, 'w') as fp:
        #     pass


        # self.combine_and_filter_data()
        return (ret, message)


    def combine_and_filter_data(self,):
        file1 =  self.alias + "/scopus-" + "abstracts.csv"
        file2 =  self.alias + "/sciencedirect-" + "abstracts.csv"
        file3 =  self.alias + "/wos-" + "abstracts.csv"

        df1 = pd.read_csv(file1, sep='\t')
        df2 = pd.read_csv(file2, sep='\t')

        merged_1_2 = pd.concat([df1, df2], ignore_index=True)
        merged_1_2.drop_duplicates(subset='scopus_id', inplace=True)

        print(merged_1_2.columns)

        df3 = pd.read_csv(file3, sep='\t')
        df3.rename(columns={'Item Title': 'title'}, inplace=True)
        df3.rename(columns={'Abstract': 'abstract'}, inplace=True)
        df3.rename(columns={'DOI': 'doi'}, inplace=True)

        final_merge = pd.concat([merged_1_2, df3], ignore_index=True)
        final_merge['title'] = final_merge['title'].str.lower()
        final_merge.drop_duplicates(subset='title', inplace=True)

        columns = ['title', 'abstract', 'doi', 'authors', 'count']
        final_df = final_merge[columns]

        #-----------Filter Using LLAMA2
        df = final_df
        df['text_to_classify'] = df['abstract'].fillna(df['title'])

        # Initialize the model pipeline
        model_id = "meta-llama/Llama-2-7b-chat-hf"
        os.environ["CUDA_VISIBLE_DEVICES"] = "0"
        device = "cuda" if torch.cuda.is_available() else "cpu"

        pipeline = transformers.pipeline(
            "text-generation",
            model=model_id,
            model_kwargs={"torch_dtype": torch.float16}, 
            device=device,
        )

        # Define the system and user prompt
        def create_prompt(text):
            messages = [
                {"role": "system", "content": "You are an expert in agriculture and an excellent text classifier."},
                {"role": "user", "content": f'''You are given a search equation and a text. Your task is to determine if the text contains information relevant to the search equation.
                Focus on finding as many keywords from the search equation as possible in the text. 
                If the text contains multiple relevant keywords, respond with RELATED. If it does not contain relevant keywords or only a few, respond with UNRELATED.
                Only respond with RELATED or UNRELATED no other text required.
                Search Equation: {self.keyword}
                Text: {text}
                Result:'''}
            ]
            
            prompt = pipeline.tokenizer.apply_chat_template(
                messages,
                tokenize=False,
                add_generation_prompt=True
            )
            return prompt

        terminators = [
            pipeline.tokenizer.eos_token_id,
            pipeline.tokenizer.convert_tokens_to_ids("<|eot_id|>")
        ]

        def classify_text(text):
            prompt = create_prompt(text)
            outputs = pipeline(
                prompt,
                max_new_tokens=32,
                eos_token_id=terminators,
                do_sample=True,
                temperature=0.6,
                top_p=0.9,
            )
            result_text = outputs[0]["generated_text"][len(prompt):]
            # print(result_text)
            return result_text.strip()

        for index, row in df.iterrows():
            result = classify_text(row['text_to_classify'])
            df.at[index, 'classification_result'] = result
            # print(f"Processed row {index}: Classification = {result}")

        df.drop(columns=['text_to_classify'], inplace=True)
        df.to_csv(self.final_path, sep='\t', index=False)

        print(f"Updated CSV saved to: {self.final_path}")

        # final_df.to_csv(self.final_path, sep='\t', index=False)

        
    def filter_using_model_scopus(self):
        model_class = BertForSequenceClassification
        tokenizer_class = BertTokenizer

        model = model_class.from_pretrained('bert-base-uncased')
        tokenizer = tokenizer_class.from_pretrained('bert-base-uncased')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        state_dict_path = dir_path + '/bert_classification_model.pth'
        
        print("STATE DICT --------",state_dict_path )
        state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))

        model.load_state_dict(state_dict)
        model.eval()
        
        df = pd.read_csv(self.scopus_files, sep="\t", header=None)
        # titles = df[1].to_list()
        # titles = [title.lower() for title in titles]

        abstract = df.iloc[:, -1].to_list()
        title = df[1].to_list()
        titles = []
        for index, item in enumerate(title):
            if not abstract[index]:
                titles.append(str(item).lower())
            else:
                titles.append(str(abstract[index]).lower())
        
        batch_size = 8  
        created_header = True
        for i in range(0, len(titles), batch_size):
            selected_articles = []
            selected_titles = set()
            selected_probs = []
            batch_texts = titles[i:i+batch_size]
            tokens = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                logits = model(**tokens).logits
            
            probs = torch.nn.functional.softmax(logits, dim=1)
            max_prob = torch.max(probs, dim=1)[0]
            predicted_labels = torch.argmax(probs, dim=1).tolist()
            
            for j, text in enumerate(batch_texts):
                index = i + j 
                if predicted_labels[j] == 1:
                    items= df.iloc[index].copy()
                    length = len(items)
                    items[length] = max_prob[j].item()
                    selected_articles.append(items)
                    selected_titles.add(text)


            df_out = pd.DataFrame(selected_articles)
            if len(df_out) > 0 and created_header:           
                header = ["scopus_id", "title", "publication_name", "issn", "isbn", "eissn", "volume", "page_range", "cover_date", "doi", "citation_count", "affiliation", "aggregation_type", "subtype_description", "authors", "full_text", "abstract", "probability"]
                df_out.to_csv(self.selected_files_scopus, sep="\t", header=header, index=None, mode="a")
                created_header = False
            else:
                df_out.to_csv(self.selected_files_scopus, sep="\t", header=None, index=None, mode="a")

    
    def filter_using_model_sciencedirect(self):
    
        model_class = BertForSequenceClassification
        tokenizer_class = BertTokenizer

        model = model_class.from_pretrained('bert-base-uncased')
        tokenizer = tokenizer_class.from_pretrained('bert-base-uncased')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        state_dict_path = dir_path + '/bert_classification_model.pth'
        
        print("STATE DICT --------",state_dict_path )
        state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))

        model.load_state_dict(state_dict)
        model.eval()
        
        df = pd.read_csv(self.sciencedirect_files, sep="\t", header=None)
        # titles = df[1].to_list()
        # titles = [title.lower() for title in titles]

        abstract = df.iloc[:, -1].to_list()
        title = df[1].to_list()
        titles = []
        for index, item in enumerate(title):
            if not abstract[index]:
                titles.append(str(item).lower())
            else:
                titles.append(str(abstract[index]).lower())
        
        batch_size = 8  
        created_header = True
        for i in range(0, len(titles), batch_size):
            selected_articles = []
            selected_titles = set()
            batch_texts = titles[i:i+batch_size]
            tokens = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                logits = model(**tokens).logits
            
            probs = torch.nn.functional.softmax(logits, dim=1)
            predicted_labels = torch.argmax(probs, dim=1).tolist()
            max_prob = torch.max(probs, dim=1)[0]
            
            for j, text in enumerate(batch_texts):
                index = i + j 
                if predicted_labels[j] == 1:
                    items= df.iloc[index].copy()
                    length = len(items)
                    items[length] = max_prob[j].item()
                    selected_articles.append(items)
                    # selected_articles.append(df.iloc[index])
                    selected_titles.add(text)

            df_out = pd.DataFrame(selected_articles)
            if len(df_out) > 0 and created_header: 
                header = ["scopus_id", "title", "publication_name", "issn", "isbn", "eissn", "volume", "page_range", "cover_date", "doi", "citation_count", "affiliation", "aggregation_type", "subtype_description", "authors", "full_text", "abstract", "probability"]
                df_out.to_csv(self.selected_files_sciencedirect, sep="\t", header=header, index=None, mode="a")
                created_header = False
            else:
                df_out.to_csv(self.selected_files_sciencedirect, sep="\t", header=None, index=None, mode="a")
      

    def filter_using_model_wos(self,):
        model_class = BertForSequenceClassification
        tokenizer_class = BertTokenizer

        model = model_class.from_pretrained('bert-base-uncased')
        tokenizer = tokenizer_class.from_pretrained('bert-base-uncased')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        state_dict_path = dir_path + '/bert_classification_model.pth'
        
        print("STATE DICT --------",state_dict_path )
        state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))

        model.load_state_dict(state_dict)
        model.eval()
        
        df = pd.read_csv(self.wos_files)

        abstract = df['Abstract'].to_list()
        title = df['Item Title'].to_list()
        titles = []
        header = df.columns

        for index, item in enumerate(title):
            if not abstract[index]:
                titles.append(str(item).lower())
            else:
                titles.append(str(abstract[index]).lower())
        
        batch_size = 8  
        created_header = True
        for i in range(0, len(titles), batch_size):
            selected_articles = []
            selected_titles = set()
            batch_texts = titles[i:i+batch_size]
            tokens = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                logits = model(**tokens).logits
            
            probs = torch.nn.functional.softmax(logits, dim=1)
            predicted_labels = torch.argmax(probs, dim=1).tolist()
            max_prob = torch.max(probs, dim=1)[0]
            
            for j, text in enumerate(batch_texts):
                index = i + j 
                if predicted_labels[j] == 1:
                    items= df.iloc[index].copy()
                    length = len(items)
                    items[length] = max_prob[j].item()
                    selected_articles.append(items)
                    selected_titles.add(text)

            df_out = pd.DataFrame(selected_articles)
            if len(df_out) > 0 and created_header: 
                df_out.to_csv(self.selected_files_wos, sep="\t", header=header, index=None, mode="a")
                created_header = False
            else:
                df_out.to_csv(self.selected_files_wos, sep="\t", header=None, index=None, mode="a")


    def filter_using_model_scholar(self):
    
        model_class = BertForSequenceClassification
        tokenizer_class = BertTokenizer

        model = model_class.from_pretrained('bert-base-uncased')
        tokenizer = tokenizer_class.from_pretrained('bert-base-uncased')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        state_dict_path = dir_path + '/bert_classification_model.pth'
        
        print("STATE DICT --------",state_dict_path )
        state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))

        model.load_state_dict(state_dict)
        model.eval()
        
        df = pd.read_csv(self.scopus_files, sep="\t", header=None)
        titles = df[1].to_list()
        titles = [title.lower() for title in titles]
        
        batch_size = 8  
        
        for i in range(0, len(titles), batch_size):
            selected_articles = []
            selected_titles = set()
            batch_texts = titles[i:i+batch_size]
            tokens = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                logits = model(**tokens).logits
            
            probs = torch.nn.functional.softmax(logits, dim=1)
            predicted_labels = torch.argmax(probs, dim=1).tolist()
            max_prob = torch.max(probs, dim=1)[0]
            
            for j, text in enumerate(batch_texts):
                index = i + j 
                if predicted_labels[j] == 1:
                    items= df.iloc[index].copy()
                    length = len(items)
                    items[length] = max_prob[j]
                    # selected_articles.append(df.iloc[index])
                    selected_articles.append(items)
                    selected_titles.add(text)

            df_out = pd.DataFrame(selected_articles)
            df_out.to_csv(self.selected_files_scholar, sep="\t", header=None, index=None, mode="a")
            

    def filter_using_model(self):
        model_class = BertForSequenceClassification
        tokenizer_class = BertTokenizer

        model = model_class.from_pretrained('bert-base-uncased')
        tokenizer = tokenizer_class.from_pretrained('bert-base-uncased')

        dir_path = os.path.dirname(os.path.realpath(__file__))
        
        state_dict_path = dir_path + '/bert_classification_model.pth'
        
        print("STATE DICT --------",state_dict_path )
        state_dict = torch.load(state_dict_path, map_location=torch.device('cpu'))

        model.load_state_dict(state_dict)
        model.eval()
        
        df = pd.read_csv(self.final_path, sep="\t", header=None)
        titles = df[0].to_list()
        titles = [title.lower() for title in titles]
        
        batch_size = 8  
        
        for i in range(0, len(titles), batch_size):
            selected_articles = []
            selected_titles = set()
            batch_texts = titles[i:i+batch_size]
            tokens = tokenizer(batch_texts, return_tensors='pt', padding=True, truncation=True)
            with torch.no_grad():
                logits = model(**tokens).logits
            
            probs = torch.nn.functional.softmax(logits, dim=1)
            predicted_labels = torch.argmax(probs, dim=1).tolist()
            
            for j, text in enumerate(batch_texts):
                index = i + j 
                if predicted_labels[j] == 1:
                    selected_articles.append(df.iloc[index])
                    selected_titles.add(text)

            df_out = pd.DataFrame(selected_articles)
            df_out.to_csv(self.selected_files, sep="\t", header=None, index=None, mode="a")
            

    def count_keywords(self,keywords, text):
        if text:
            text = str(text).lower()
            keyword_counts = Counter()

            for keyword in keywords:
                count = len(re.findall(r'\b' + re.escape(keyword.lower()) + r'\b', text))
                keyword_counts[keyword] = count

            return str(keyword_counts)
        return ""

    def get_data_from_scopus(self,):
        # try:
        fol_key = self.alias + "/scopus-"
        kw = self.keyword
        key = '' #socups API Key
        scopus = Scopus(key)
        search_df = scopus.search(kw,count=self.scopus_count-1,view='STANDARD')
        # search_df.to_csv(fol_key+"data.csv", sep='\t',index=False, mode="a")
        # df = pd.read_csv(fol_key+"data.csv", sep='\t')
        df = search_df
        
        for index,row in df.iterrows():
            id = row['scopus_id']
            row['abstract'] = ""
            try:
                pub_info = scopus.retrieve_abstract(id)
                row['abstract'] = pub_info['abstract']
            except Exception as ex:
                print(ex)
                # continue
            new_df = pd.DataFrame([row.tolist()])
            # new_df.to_csv(fol_key+"abstracts-temp.csv", sep='\t', header=None, index=None, mode="a")
            new_df.to_csv(fol_key+"abstracts.csv", sep='\t', header=None, index=None, mode="a")

        header = ["scopus_id", "title", "publication_name", "issn", "isbn", "eissn", "volume", "page_range", "cover_date", "doi", "citation_count", "affiliation", "aggregation_type", "subtype_description", "authors", "full_text", "abstract"]
        udf = pd.read_csv(fol_key+"abstracts.csv",sep='\t', header=None)

        #Adding the count of each keyword in the header - Remember to do this in the filtering step as well
        header.append("count")
        last_column = udf.iloc[:, -1]
        udf[udf.shape[1]] = last_column.apply(lambda x: self.count_keywords(self.all_words, x))


        udf.to_csv(fol_key+"abstracts.csv", sep='\t', header=header, index=None)
    
    def generate_combinations_for_groups(self, mainkey, max_connectors):
        from itertools import product
        keyword_groups = {
            'Fertilizers': ['Fertilization', 'Fertilizer'],
            'Rates': ['Rates', 'Doses'],
            'Sulfur': ['Sulfur', 'Sulphur']
        }
        results = []
        keywords = list(keyword_groups.values())
        
        for combination in product(*keywords):
            keywords_part = ' OR '.join(combination)
            result_key = mainkey+f' AND (Nutrient OR {keywords_part} OR Nitrogen OR Phosphorus OR Potassium) AND Yield'
            results.append(result_key)

        return results
      
    def get_data_from_sciencedirect(self,):
         
        # Something that is done for the African dataset generation can be ignored for the others
        # main = self.keyword.split(" ")[0]
        # combinations = self.generate_combinations_for_groups(main, max_connectors=8)

        # Uncomment this line instead
        kw = self.keyword
         
        fol_key = self.alias + "/sciencedirect-"

        # for kw in combinations:
        count = 0
        while count < 5:
            try:
                print("Processing --- ", kw)
                key = '94c2e7cb56c5631b9a979f29fbae424b'
                scopus = Scopus(key)
                search_df = scopus.search_science(kw,count=self.science_count,view='STANDARD')
                # search_df.to_csv(fol_key+"data.csv", sep='\t',index=False, mode="a")
                # df = pd.read_csv(fol_key+"data.csv", sep='\t')

                df = search_df
                
                for index,row in df.iterrows():
                    id = row['scopus_id']
                    row['abstract'] = ""
                    try:
                        pub_info = scopus.retrieve_abstract_science(id)
                        row['abstract'] = pub_info['abstract']
                    except Exception as ex:
                        continue
                    finally:
                        new_df = pd.DataFrame([row.tolist()])
                        new_df.to_csv(fol_key+"abstracts.csv", sep='\t', header=None, index=None, mode="a")

                count = 5
            except Exception as ex:
                print(ex)
                count +=1

        header = ["scopus_id", "title", "publication_name", "issn", "isbn", "eissn", "volume", "page_range", "cover_date", "doi", "citation_count", "affiliation", "aggregation_type", "subtype_description", "authors", "full_text", "abstract"]
        udf = pd.read_csv(fol_key+"abstracts.csv", sep='\t', header=None)

        #Filtering data with duplicate scopus_id
        # udf = udf[udf.duplicated(0, keep=False)]

        #Adding the count of each keyword in the header - Remember to do this in the filtering step as well
        header.append("count")
        last_column = udf.iloc[:, -1]
        udf[udf.shape[1]] = last_column.apply(lambda x: self.count_keywords(self.all_words, x))

        udf.to_csv(fol_key+"abstracts.csv", sep='\t', header=header, index=None)


    def get_data_from_wos(self,):

        fol_key = self.alias + "/wos-"
        apikey = "" #WOS Expanded API Key, Just 1M data per year

        params = {'databaseId': 'WOS',
          'usrQuery': f'TS=({self.keyword})',
          'firstRecord': 1,
          'count': self.wos_count,
          'sortField': 'TC+D',
          #'tcModifiedTimeSpan': '2023-09-01+2023-11-14'
          }

        if apikey and apikey != '':
            data = woseclient.get_all_records(apikey, params, params['firstRecord'], params['count'])
        else:
            raise ValueError('No API key was supplied')

        if len(data) > 0:
            with open(fol_key+"abstracts.csv", 'w', newline = '') as f:
                print("Mapping {} records to CSV.".format(len(data)))
                csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                header = ['WoS UT', 'Pub Year', 'Early Access Year', 'Sort Date', 'Cover Date', 'DOAJ OA', 'Has Abstract', 'Abstract', 'Pub Type', 'Doc Type', 'Collection Edition', 'DOI', 'PMID', 'ISSN', 'eISSN', 'Source Title', 'Source Title Abbreviation', 'Item Title', 'Macro Citation Topic', 'Meso Citation Topic', 'Micro Citation topic', 'SDGs', 'WoS Subject Headings', 'WoS Subject Subheadings', 'WoS Subject Categories', 'WoS Research Areas', 'Acknowledgements', 'WOS Times Cited']
                csv_writer.writerow(header)

                for rec in data:
                    row = []
                    row.append(woseAPIclientQuery.safeget(rec, 'UID'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'pubyear'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'early_access_year'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'sortdate'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'coverdate'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'journal_oas_gold'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'has_abstract'))
                    row.append(woseAPIclientQuery.parse_abstract(rec))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'pub_info', 'pubtype'))
                    row.append(woseAPIclientQuery.safeget(rec, 'static_data', 'summary', 'doctypes', 'doctype'))
                    row.append(woseAPIclientQuery.parse_editions(rec))
                    row.append(woseAPIclientQuery.parse_dois(rec))
                    row.append(woseAPIclientQuery.parse_pmids(rec))
                    row.append(woseAPIclientQuery.parse_issns(rec))
                    row.append(woseAPIclientQuery.parse_eissns(rec))
                    row.append(woseAPIclientQuery.parse_sourcetitle(rec))
                    row.append(woseAPIclientQuery.parse_sotitleabbrev(rec))
                    row.append(woseAPIclientQuery.parse_itemtitle(rec))
                    row.append(woseAPIclientQuery.parse_tmac(rec))
                    row.append(woseAPIclientQuery.parse_tmes(rec))
                    row.append(woseAPIclientQuery.parse_tmic(rec))
                    row.append(woseAPIclientQuery.parse_sdgs(rec))
                    row.append(woseAPIclientQuery.parse_woshead(rec))
                    row.append(woseAPIclientQuery.parse_wossubhead(rec))
                    row.append(woseAPIclientQuery.parse_ascatrad(rec))
                    row.append(woseAPIclientQuery.parse_ascaext(rec))
                    row.append(woseAPIclientQuery.parse_acknowledgements(rec))
                    # row.append(woseAPIclientQuery.parse_woscitations(rec))
                        
                    csv_writer.writerow(row)

            print(f"CSV written to {fol_key}abstracts.csv")
        else:
            print("*** No data to write :( ***".format(self.keyword))

    
        #Adding the count of each keyword in the header - Remember to do this in the filtering step as well _ this is only applicable for wos getting the headername
        udf = pd.read_csv(fol_key+"abstracts.csv",sep=',')
        header = list(udf.columns)
        header.append("count")
        last_column = udf['Abstract']
        udf[udf.shape[1]] = last_column.apply(lambda x: self.count_keywords(self.all_words, x))

        udf.to_csv(fol_key+"abstracts.csv", sep='\t', header=header, index=None)


    def process_similar_sentences(self,):
        fol_key =  self.alias + "/"
        from sentence_transformers import SentenceTransformer
        from sklearn.metrics.pairwise import cosine_similarity

        df = pd.read_csv(fol_key+"final.csv", sep='\t',header=0)
        titles = df.iloc[:,1].values.tolist()
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        title_embeddings = model.encode(titles)
        similarity_matrix = cosine_similarity(title_embeddings, title_embeddings)
        
        not_similar_indexes = []
        for index, item in enumerate(titles):
            similarity_scores = similarity_matrix[index]
            similarity_scores.sort()
            scores = similarity_scores[-2]  # Exclude the query title itself
            if scores < 0.9:
                not_similar_indexes.append(index)

        out_df = df.iloc[not_similar_indexes]
        out_df.to_csv(fol_key+"final.csv", sep='\t',index=None)


    def post_process_scholar(self, ):
        scholar_files = []
        files = os.listdir(self.scholar_path)
        for filename in files:
            if ".csv" in filename and str(self.end+1) in filename:
                scholar_files.append(self.scholar_path+ "/"+filename)
                
        self.combine_scholar(scholar_files)
        self.filter_english()
        
    def post_process_collected_data(self,):
        scholar_files = []
        files = os.listdir(self.scholar_path)
        for filename in files:
            if ".csv" in filename:
                scholar_files.append(self.scholar_path+ "/"+filename)
        
        self.combine_scholar(scholar_files)
        self.filter_english()
        self.filter_doi_combine_all()
              
    
    def combine_scholar(self, scholar_files):
        for file in scholar_files:
            data = pd.read_csv(file, header=None, sep="\t") 
            data.to_csv(self.combined_path, mode="a", sep="\t", header=None, index=None)
       
          
    def detect_language(self,text):
        lang, _ = langid.classify(text)
        if lang == 'en':
            return True
        else:
            return False
        
        
    def filter_english(self,):
        data = pd.read_csv(self.combined_path, header=None, sep="\t") 
        fil_data = []
        for index,row in data.iterrows():
            row2 = row[1]
            flag = self.detect_language(row2)
            if flag:
                fil_data.append(row)
        
        df = pd.DataFrame(fil_data)
        df.to_csv(self.scholar_fil_path, sep="\t", header=None, index=None)
      

    def filter_doi_combine_all(self, ):
        scholar = pd.read_csv(self.scholar_fil_path, header=None, sep="\t")
        scopus =  pd.read_csv(self.scopus_files, header=None, sep="\t")
        
        title, doi, abstract, authors = [], [], [], []
        
        for index, rows in scholar.iterrows():
            title.append(str(rows[1]).lower())
            authors.append(str(rows[2]).lower())
            doi.append("")
            abstract.append(str(rows[5]).lower())  
            
        for index, rows in scopus.iterrows():
            title.append(str(rows[1]).lower())
            authors.append(str(rows[11]).lower())
            doi.append(str(rows[9]).lower())
            abstract.append(str(rows[16]).lower())
        
        if self.webofscience_files:    
            wos = pd.read_csv(self.webofscience_files, header=None, sep="\t")
            
            for index, rows in wos.iterrows():
                title.append(str(rows[1]).lower())
                authors.append(str(rows[3]).lower())
                doi.append(str(rows[2]).lower())
                abstract.append(str(rows[4]).lower())
            

        unique_indices = []
        unique_title = set()
        unique_doi = set()
        for index, value in enumerate(title):
            if value not in unique_title:
                if doi[index] not in unique_doi:
                    unique_doi.add(doi[index])
                    unique_title.add(value)
                    unique_indices.append(index)
                if doi[index] == "":
                    unique_title.add(value)
                    unique_indices.append(index)

        fil_abs = [abstract[index] for index in unique_indices]
        fil_doi = [doi[index] for index in unique_indices]
        fil_authors = [authors[index] for index in unique_indices]
        fil_title = [title[index] for index in unique_indices]

        final_data = []
        for index, item in enumerate(unique_indices):
            final_data.append([fil_title[index], fil_authors[index], fil_abs[index], fil_doi[index]])
        
        final_df = pd.DataFrame(final_data)
        final_df.to_csv(self.final_path, header=None, index=None, sep="\t")




        # configuration = woslite_client.Configuration()
        # configuration.api_key['X-ApiKey'] = 'bd715fc8665ba2072e5fbc5697164aaa8bc49bb6'
        # fol_key = self.alias + "/wos-"
        # kw = self.keyword
        # response = []
        # i = 1
        # while i < self.wos_count:
        #     integration_api_instance = woslite_client.IntegrationApi(woslite_client.ApiClient(configuration))
        #     api_instance = woslite_client.SearchApi(woslite_client.ApiClient(configuration))
        #     database_id = 'WOK' # str | Database to search. Must be a valid database ID, one of the following: BCI/BIOABS/BIOSIS/CCC/DCI/DIIDW/MEDLINE/WOK/WOS/ZOOREC. WOK represents all databases.
        #     usr_query = f'TS=({kw})' # str | User query for requesting data, ex: TS=(cadmium). The query parser will return errors for invalid queries.
        #     count = 100 # int | Number of records to return, must be 0-100.
        #     first_record = i # int | Specific record, if any within the result set to return. Cannot be less than 1 and greater than 100000.
        #     try:
        #         api_response = api_instance.root_get(database_id, usr_query, count, first_record)
                
        #         response.append(api_response.data)
        #         ids = []
        #         all_data = []
        #         for data in api_response.data:
        #             id = data.ut
        #             ids.append(id)
        #             final = {'id': "",
        #                     'author': "",
        #                     'doctype': "",
        #                     'doi': "",
        #                     'source': "",
        #                     'title': "",
        #                     'abstract': ""
        #                     }
        #             final['id'] =  data.ut
        #             final['author'] =  data.author.authors if data.author.authors else ""
        #             final['doctype'] = data.doctype if data.doctype else ""
        #             final['doi'] =  data.other.identifier_doi[0] if data.other.identifier_doi else ""
        #             final['source'] = data.source if data.source else ""
        #             final['title'] = data.title.title[0] if data.title.title else ""

        #             # check = True
        #             # if check:
        #             #     browser = webdriver.Chrome()
        #             #     browser.get(self.url+id)
        #             #     element = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.CLASS_NAME, "abstract--instance"))
        #             #     soup = BeautifulSoup(browser.page_source, features="html.parser")
        
        #             #     all_abstract = soup.find("div", class_="abstract--instance")
                        
        #             #     if all_abstract is not None:
        #             #         paragraph = all_abstract.find("p").get_text()
        #             #         final['abstract'] = paragraph
                        
        #             all_data.append(final)
                    
        #             new_df = pd.DataFrame([[final['id'],  final['title'], final['author'], final['doi'], final['abstract']]])
        #             new_df.to_csv(fol_key+"abstracts.csv", sep='\t', header=None, index=None, mode="a")
                
        #     except ApiException as e:
        #         print('Exception when calling SearchApi->root_get: %s\n' % e)
            
        #     i += 100
             
 
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--keyword", help="Enter the keyword to be searched.")
#     parser.add_argument("--alias", help="Enter alias of the keyword (one-word).")
#     parser.add_argument("--count", help="Enter max number of articles to retrieve from scopus and wos (<5000)")
#     parser.add_argument("--end", help="Google scholar end year")
#     args = parser.parse_args()
#     keyword = args.keyword
#     alias = args.alias
#     count = args.count
#     end = args.end
#     GetAllUrl(keyword, alias, count, end).start_execution()
