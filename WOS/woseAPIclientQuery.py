"""
Script to produce CSV from WoS Expanded API
Example usage: python3 woseAPIclientQuery.py -q TS="antarctica microorganisms"
"""
import csv
import sys
import argparse
import json
import requests
from WOS import woseclient

# DEFAULT VALUES
#Hardcode API key here:
apikey = 'WOS_EXPANDED_API_KEY'

params = {'databaseId': 'WOS',
          'usrQuery': 'TS=antartica microorganisms',
          'firstRecord': 1,
          'count': 50,
          'sortField': 'TC+D'#,
          #'tcModifiedTimeSpan': '2023-09-01+2023-11-14'
          }


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--query', help="Query to send to WoS API. "
                        "e.g. TS=CRISPR")
    parser.add_argument('-k', '--key', help="WoS Starter API token.")

    return parser.parse_args(args)


def safeget(dct, *keys):
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
        except TypeError:
            pass
    if dct:
        try:
            if isinstance(dct, list):
                if isinstance(dct[0], dict):
                    try:
                        return dct[0][key]
                    except:
                        return dct[0]
                return dct[0]
            else:
                return dct
        except:
            return None
            
def parse_woscitations(rec):
    woscites = {}
    try:
        x = rec['dynamic_data']['citation_related']['tc_list']['silo_tc']
        for i in x:
            if isinstance(x, list):
                if i['coll_id'] == 'WOS':
                    woscites = i['local_count']
            else:
                if x['coll_id'] == 'WOS':
                    woscites = x['local_count']
    except Exception as ex:
        return woscites
    return woscites
    
def parse_dois(rec):
    dois = {}
    try:
        x = rec['dynamic_data']['cluster_related']['identifiers']['identifier']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'doi':
                    dois = i['value']
            else:
                if x['type'] == 'doi':
                    dois = x['value']
    except Exception as ex:
        return dois
            
    return dois
    
def parse_issns(rec):
    issns = {}
    try:
        x = rec['dynamic_data']['cluster_related']['identifiers']['identifier']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'issn':
                    issns = i['value']
            else:
                if x['type'] == 'issn':
                    issns = x['value']
    except Exception as ex:
        return issns       
    return issns
    
def parse_eissns(rec):
    eissns = {}
    try:
        x = rec['dynamic_data']['cluster_related']['identifiers']['identifier']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'eissn':
                    eissns = i['value']
            else:
                if x['type'] == 'eissn':
                    eissns = x['value']
    except Exception as ex:
        return eissns        
    return eissns
    
def parse_pmids(rec):
    pmids = {}
    try:
        x = rec['dynamic_data']['cluster_related']['identifiers']['identifier']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'pmid':
                    pmids = i['value']
            else:
                if x['type'] == 'pmid':
                    pmids = x['value']
    except Exception as ex:
        return pmids          
    return pmids

def parse_tmac(rec):
    tmac = {}
    try:
        if 'citation_topics' in rec['dynamic_data']['citation_related']:
            for i in rec['dynamic_data']['citation_related']['citation_topics']['subj-group']['subject']:
                if i['content-type'] == 'macro':
                    tmac = i['content']
        else:
            tmac = 'NULL'
    except Exception as ex:
        return 'NULL'      
    return tmac
    
def parse_tmes(rec):
    tmes = {}
    try:
        if 'citation_topics' in rec['dynamic_data']['citation_related']:
            for i in rec['dynamic_data']['citation_related']['citation_topics']['subj-group']['subject']:
                if i['content-type'] == 'meso':
                    tmes = i['content']
        else:
            tmes = 'NULL'
    except Exception as ex:  
        return 'NULL'

    return tmes
    
def parse_tmic(rec):
    tmic = {}
    try:
        if 'citation_topics' in rec['dynamic_data']['citation_related']:
            for i in rec['dynamic_data']['citation_related']['citation_topics']['subj-group']['subject']:
                if i['content-type'] == 'micro':
                    tmic = i['content']
        else:
            tmic = 'NULL'
    except Exception as ex:
        return 'NULL' 
    return tmic
    
def parse_sdgs(rec):
    sdg = {}
    try:
        if 'SDG' in rec['dynamic_data']['citation_related']:
            sdg_list = rec['dynamic_data']['citation_related']['SDG']['sdg_category']
            for i in sdg_list:
                if isinstance(sdg_list, list):
                    sdg = ';'.join(i.get('content') for i in sdg_list)
                else:
                    sdg = sdg_list['content']
        else:
            sdg = 'NULL'
    except Exception as ex:
        return 'NULL'

    return sdg

def parse_sourcetitle(rec):
    stitle = {}
    try:
        x = rec['static_data']['summary']['titles']['title']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'source':
                    stitle = i['content']
            else:
                if x['type'] == 'source':
                    stitle = x['content']
    except Exception as ex:
        return stitle

    return stitle
    
def parse_sotitleabbrev(rec):
    stitleabbrev = {}
    try:
        x = rec['static_data']['summary']['titles']['title']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'source_abbrev':
                    stitleabbrev = i['content']
            else:
                if x['type'] == 'source_abbrev':
                    stitleabbrev = x['content']

    except Exception as ex:
        return stitleabbrev

    return stitleabbrev
    
def parse_itemtitle(rec):
    itemtitle = {}
    try:
        x = rec['static_data']['summary']['titles']['title']
        for i in x:
            if isinstance(x, list):
                if i['type'] == 'item':
                    itemtitle = i['content']
            else:
                if x['type'] == 'item':
                    itemtitle = x['content']
    except Exception as ex:
        return itemtitle

    return itemtitle
    
def parse_editions(rec):
    wosed = {}
    try:
        if 'EWUID' in rec['static_data']['summary']:
            wosed_list = rec['static_data']['summary']['EWUID']['edition']
            for i in wosed_list:
                if isinstance(wosed_list, list):
                    wosed = ';'.join(i.get('value') for i in wosed_list)
                else:
                    wosed = wosed_list['value']
        else:
            wosed = 'NULL'
    except Exception as ex:
        return 'NULL'    
    return wosed

def parse_woshead(rec):
    
    woshead = {}
    try:
        if 'headings' in rec['static_data']['fullrecord_metadata']['category_info']:
            woshead_list = rec['static_data']['fullrecord_metadata']['category_info']['headings']['heading']
            if isinstance(woshead_list, list):
                woshead = ';'.join(woshead_list)
            else:
                woshead = woshead_list
        else:
            woshead = 'NULL'

    except Exception as ex:
        return 'NULL'

    return woshead

def parse_wossubhead(rec):
    wossubhead = {}
    try:
        if 'subheadings' in rec['static_data']['fullrecord_metadata']['category_info']:
            wossubhead_list = rec['static_data']['fullrecord_metadata']['category_info']['subheadings']['subheading']
            if isinstance(wossubhead_list, list):
                wossubhead = ';'.join(wossubhead_list)
            else:
                wossubhead = wossubhead_list
        else:
            wossubhead = 'NULL'
    except Exception as ex:
        return 'NULL'    
    return wossubhead
    
def parse_ascatrad(rec):
    ascatrad_out = []
    try:
        if 'subjects' in rec['static_data']['fullrecord_metadata']['category_info']:
            ascatrad_list = rec['static_data']['fullrecord_metadata']['category_info']['subjects']['subject']
            if isinstance(ascatrad_list, list):
                for i in ascatrad_list:
                    if i['ascatype'] == 'traditional':
                        ascatrad_out.append(i['content'])
                ascatrad = ';'.join(ascatrad_out)
            else:
                if ascatrad_list['ascatype'] == 'traditional':
                        ascatrad = ascatrad_list['conent']
        else:
            ascatrad = 'NULL'
    except Exception as ex:
        return 'NULL'   
    return ascatrad
    
def parse_ascaext(rec):
    ascaext_out = []
    try:
        if 'subjects' in rec['static_data']['fullrecord_metadata']['category_info']:
            ascaext_list = rec['static_data']['fullrecord_metadata']['category_info']['subjects']['subject']
            if isinstance(ascaext_list, list):
                for i in ascaext_list:
                    if i['ascatype'] == 'extended':
                        ascaext_out.append(i['content'])
                ascaext = ';'.join(ascaext_out)
            else:
                if ascaext_list['ascatype'] == 'extended':
                    ascaext = ascaext_list['content']
        else:
            ascaext = 'NULL'
    except Exception as ex:
        return 'NULL'

    return ascaext
    
def parse_abstract(rec):
    abstract = {}
    try:
        if 'abstracts' in rec['static_data']['fullrecord_metadata']:
            abstract_list = rec['static_data']['fullrecord_metadata']['abstracts']['abstract']['abstract_text']['p']
            if isinstance(abstract_list, list):
                abstract = ';'.join(abstract_list)
            else:
                abstract = abstract_list
        else:
            abstract = 'NULL'
    except Exception as ex:
        return 'NULL'
    return abstract
    
def parse_acknowledgements(rec):
    ack = {}
    try:
        if 'fund_ack' in rec['static_data']['fullrecord_metadata']:
            if 'fund_text' in rec['static_data']['fullrecord_metadata']['fund_ack']:
                ack_list = rec['static_data']['fullrecord_metadata']['fund_ack']['fund_text']['p']
                if isinstance(ack_list, list):
                    ack = ';'.join(ack_list)
                else:
                    ack = ack_list
            else:
                ack = 'NULL'
        else:
            ack = 'NULL'
    except Exception as ex:
        return 'NULL'
        
    return ack

# if __name__ == "__main__":
#     args = parse_args(sys.argv[1:])
#     if args.key:
#         apikey = args.key
#     else:
#         print("Using hardcoded API key")
#     if args.query:
#         q = args.query
#         params['usrQuery'] = q
#     else:
#         print("Using default query set in wosStarterTest.py")
#     print('Using query: {}'.format(params['usrQuery']))

#     if apikey and apikey != '':
#         data = woseclient.get_all_records(apikey, params, params['firstRecord'], params['count'])
#     else:
#         raise ValueError('No API key was supplied')

#     if len(data) > 0:
#         with open('woseResults.csv', 'w', newline = '') as f:
#             print("Mapping {} records to CSV.".format(len(data)))
#             csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#             header = ['WoS UT', 'Pub Year', 'Early Access Year', 'Sort Date', 'Cover Date', 'DOAJ OA', 'Has Abstract', 'Abstract', 'Pub Type', 'Doc Type', 'Collection Edition', 'DOI', 'PMID', 'ISSN', 'eISSN', 'Source Title', 'Source Title Abbreviation', 'Item Title', 'Macro Citation Topic', 'Meso Citation Topic', 'Micro Citation topic', 'SDGs', 'WoS Subject Headings', 'WoS Subject Subheadings', 'WoS Subject Categories', 'WoS Research Areas', 'Acknowledgements', 'WOS Times Cited']
#             csv_writer.writerow(header)

#             for rec in data:
#                 row = []
#                 row.append(safeget(rec, 'UID'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'pubyear'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'early_access_year'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'sortdate'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'coverdate'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'journal_oas_gold'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'has_abstract'))
#                 row.append(parse_abstract(rec))
#                 row.append(safeget(rec, 'static_data', 'summary', 'pub_info', 'pubtype'))
#                 row.append(safeget(rec, 'static_data', 'summary', 'doctypes', 'doctype'))
#                 row.append(parse_editions(rec))
#                 row.append(parse_dois(rec))
#                 row.append(parse_pmids(rec))
#                 row.append(parse_issns(rec))
#                 row.append(parse_eissns(rec))
#                 row.append(parse_sourcetitle(rec))
#                 row.append(parse_sotitleabbrev(rec))
#                 row.append(parse_itemtitle(rec))
#                 row.append(parse_tmac(rec))
#                 row.append(parse_tmes(rec))
#                 row.append(parse_tmic(rec))
#                 row.append(parse_sdgs(rec))
#                 row.append(parse_woshead(rec))
#                 row.append(parse_wossubhead(rec))
#                 row.append(parse_ascatrad(rec))
#                 row.append(parse_ascaext(rec))
#                 row.append(parse_acknowledgements(rec))
#                 row.append(parse_woscitations(rec))
                    
#                 csv_writer.writerow(row)

#         print("CSV written to woseResults.csv")
#     else:
#         print("*** No data to write :( ***".format(args.query))
