from __future__ import print_function
import time
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

# Configure API key authorization: key
configuration = woslite_client.Configuration()
configuration.api_key['X-ApiKey'] = 'bd715fc8665ba2072e5fbc5697164aaa8bc49bb6'
# configuration.api_key['X-ApiKey'] = 'cf293c3013c195b896a7e7b650fc086137d340b7'
# Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
# configuration.api_key_prefix['X-ApiKey'] = 'Bearer'


url = "https://www.webofscience.com/wos/woscc/full-record/"

class GetWOS:
   def start_execution(self, limit=10, key=""): 
        if not key:
            # key = '((Mungbean OR Mung bean OR Vigna radiata OR Green gram) AND (Yield OR protein OR oil) AND (harvest OR fertilization OR watering OR plant density OR Planting date OR Sowing date OR Irrigation OR Row spacing OR Seeding rate OR Fertilizer rate) NOT (black gram OR Vigna mungo))'
            key = '(("mungbean" OR "mung bean" OR "vigna radiata") AND ("yield" OR "protein" OR "oil") AND ("usa" OR "united states" OR "mexico" OR "canada"))'
        response = []
        i = 1
        while i < limit:
            # create an instance of the API class
            integration_api_instance = woslite_client.IntegrationApi(woslite_client.ApiClient(configuration))
            api_instance = woslite_client.SearchApi(woslite_client.ApiClient(configuration))
            database_id = 'WOK' # str | Database to search. Must be a valid database ID, one of the following: BCI/BIOABS/BIOSIS/CCC/DCI/DIIDW/MEDLINE/WOK/WOS/ZOOREC. WOK represents all databases.
            usr_query = f'TS={key}' # str | User query for requesting data, ex: TS=(cadmium). The query parser will return errors for invalid queries.
            count = 100 # int | Number of records to return, must be 0-100.
            first_record = i # int | Specific record, if any within the result set to return. Cannot be less than 1 and greater than 100000.
            # lang = 'lang_example' # str | Language of search. This element can take only one value: en for English. If no language is specified, English is passed by default. (optional)
            # edition = 'edition_example' # str | Edition(s) to be searched. If null, user permissions will be substituted. Must include the name of the collection and edition name separated by '+', ex: WOS+SCI. Multiple editions are separated by ','. Editions available for collection(WOS) - AHCI,CCR,IC,ISSHP,ISTP,SCI,SSCI,BHCI,BSCI and ESCI. (optional)
            # publish_time_span = 'publish_time_span_example' # str | This element specifies a range of publication dates. If publishTimeSpan is used, the loadTimeSpan parameter must be omitted. If publishTimeSpan and loadTimeSpan are both omitted, then the maximum time span will be inferred from the editions data. Beginning and end dates should be specified in the yyyy-mm-dd format separated by +, ex: 1993-01-01+2009-12-31. (optional)
            # load_time_span = 'load_time_span_example' # str | Load time span (otherwise described as symbolic time span) defines a range of load dates. The load date is the date a record was added to the database. If load date is specified, the publishTimeSpan parameter must be omitted. If both publishTimeSpan and loadTimeSpan are omitted, the maximum publication date will be inferred from the editions data. Any of D/W/M/Y prefixed with a number where D-Day, M-Month, W-Week, Y-Year allowed. Acceptable value range for Day(0-6), Week(1-52), Month(1-12) and Year(0-10), ex: 5D,30W,10M,8Y. (optional)
            # sort_field = 'sort_field_example' # str | Order by field(s). Field name and order by clause separated by '+', use A for ASC and D for DESC, ex: PY+D. Multiple values are separated by comma. (optional)

            try:
                
                # Submits a user query and returns results
                api_response = api_instance.root_get(database_id, usr_query, count, first_record)
                                                    #  , lang=lang, edition=edition, publish_time_span=publish_time_span, load_time_span=load_time_span, sort_field=sort_field)

                response.append(api_response.data)
                ids = []
                all_data = []
                for data in api_response.data:
                    id = data.ut
                    ids.append(id)
                    final = {'id': "",
                            'author': "",
                            'doctype': "",
                            'doi': "",
                            'source': "",
                            'title': "",
                            'abstract': ""
                            }
                    final['id'] =  data.ut
                    final['author'] =  data.author.authors
                    final['doctype'] = data.doctype
                    final['doi'] =  data.other.identifier_doi[0] if data.other.identifier_doi else ""
                    final['source'] = data.source
                    final['title'] = data.title.title[0]
                    

                    # browser = webdriver.Chrome()
                    # browser.get(url+id)
                    # element = WebDriverWait(browser, 10).until(lambda x: x.find_element(By.CLASS_NAME, "abstract--instance"))
                    # soup = BeautifulSoup(browser.page_source, features="html.parser")
    
                    # all_abstract = soup.find("div", class_="abstract--instance")
                    
                    # if all_abstract is not None:
                    #     paragraph = all_abstract.find("p").get_text()
                    #     final['abstract'] = paragraph
                        
                    all_data.append(final)
                    
                    import pandas as pd
                    new_df = pd.DataFrame([final.values()])
                    new_df.to_csv("test.csv", sep='\t', header=None, index=None, mode="a")
                
                        
                    # api_response = integration_api_instance.id_unique_id_get(database_id, id, 1, 1,)
            except ApiException as e:
                print('Exception when calling SearchApi->root_get: %s\n' % e)
            
            i += 100
            
            
s = GetWOS().start_execution()


#WOS Expanded API d28e4ca3894532817bc122fac68cab3a57dfdea7