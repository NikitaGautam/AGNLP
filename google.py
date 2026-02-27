
from scholarly import scholarly
from scholarly import ProxyGenerator
import pandas as pd
import sys
import os 
keys = ['author_id','title', 'author', 'pub_year', 'venue', 'abstract', 'bib','citedby_url','eprint_url','filled', 'gsrank', 'num_citations', 'pub_url', 'source', 'url_add_sclib', 'url_scholarbib']

class Scholar():
    def __init__(self, start, end, keyword, alias) -> None:
        self.start_year = start
        self.end_year =  end
        self.keyword = keyword
        self.alias = alias
        
        
    def scrapper_code(self,):
        key = self.keyword
        print("Scrapping data from Google Scholar for Year= ", self.end_year)
        try:
            full_year_data = []
            search_query = scholarly.search_pubs(key, year_low=str(self.end_year), year_high=str(self.end_year))
            l_iter = iter(search_query) 
            while True:
                item = next(l_iter, "end")
                if item == "end":
                    break
                bib = item.get('bib', "")
                single_data =  [
                    item.get('author_id', ""),
                    bib.get("title", ""),
                    bib.get("author", ""),
                    bib.get("pub_year", ""),
                    bib.get("venue", ""),
                    bib.get("abstract", ""),
                    item.get('citedby_url', ""),
                    item.get('eprint_url', ""),
                    item.get('filled', ""),
                    item.get('gsrank', ""),
                    item.get('num_citations', ""),
                    item.get('pub_url', ""),
                    item.get('source', ""),
                    item.get('url_add_sclib', ""),
                    item.get('url_scholarbib', "")
                ]     
                full_year_data.append(single_data)
                df = pd.DataFrame(full_year_data)
                df.to_csv(self.alias+"/DataYear/data-"+str(self.end_year) +".csv", sep="\t", mode="a", header=None,index=None)
                full_year_data = [] 
        
        except Exception as ex:
            print("EXCEPTION OCCURED WHILE COLLECTING DATA FROM GOOGLE SCHOLAR")
            
            
# if __name__ == "__main__":
#     scrapper_code(sys.argv[2], sys.argv[3], sys.argv[4])