"""
Web of Science Expanded API client
Note: WoS Expanded API plans are based on the number of records downloaded per year.  For "free" downloads, please use the Short Record option (optionView=SR)
"""

import requests
import json
from time import sleep

base_url = 'https://wos-api.clarivate.com/api/wos'

def get_response(apikey, params, firstRecord=1, count=50):
    """
    Send the request to the WOS API
    """

    headers = {"Accept":"application/json", "X-ApiKey": apikey}
    #print('Retrieving records {}'.format(firstRecord))
    #print(params)
    print(base_url, params)
    r = requests.get(base_url, headers=headers, params=params)
    if r.status_code == 200:
            return r.json()
    elif r.status_code == 429:
        sleep(1)
        r = requests.get(base_url, headers=headers, params=params)
        return r.json()
    else:
        print('There was an ERROR')
        print(r.status_code)
        print(r.text)

def get_addl_results(apikey, params, RecordsFound, firstRecord=1, count=50,
                     data=[]):
    headers = {"Accept":"application/json", "X-ApiKey": apikey}

    while firstRecord <= RecordsFound:
        firstRecord += count
        params['firstRecord'] = firstRecord
        print(base_url, params)
        r = requests.get(base_url, headers=headers, params=params)
        if 'REC' in r.json()["Data"]["Records"]["records"]:
            if r.status_code == 200:
                data += r.json()["Data"]["Records"]["records"]["REC"]
                print('Retrieving {} of {}'.format(len(data), RecordsFound))
                #firstRecord += count
            else:
                print('Error! attempting to continue...')
                print(r.text)
                #firstRecord += count

    return data


def get_all_records(apikey, params, firstRecord=1, count=50):
    """
    Retrieve all results for a query
    """
    r = get_response(apikey, params, firstRecord, count)
    qr = r['QueryResult']
    data = r['Data']['Records']['records']['REC']
    # return data
    try:
        if qr['RecordsFound'] > count:
            data = get_addl_results(apikey, params, qr['RecordsFound'],
                                firstRecord, count, data)
    except Exception as ex:
        print(ex)

    return data
