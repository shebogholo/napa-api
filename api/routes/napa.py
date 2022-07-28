import re
from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel
from fastapi import APIRouter, Response
from elasticsearch import Elasticsearch
from core.db import create_query, get_all_queries

router = APIRouter()


es = Elasticsearch("http://172.17.0.1:9200")


class SearchQuery(BaseModel):
    query: str


@router.get(
    "/index",
)
async def index():
    return {'message': 'NaPA API'}

def get_number(query: str):
    p = re.compile(r'^\d{1,4}')
    number = re.findall(r'^\d{1,4}', query)
    search = query.split(' ')
    index = ''
    if len(number) >  0:
        if number[0] in search:
            index = search.index(number[0])
        return index, int(number[0])
    else:
        return None, None


def get_postcode(query: str):
    p = re.compile(r'\d{5}')
    postcode = re.findall(r'\d{5}', query) 
    search = query.split(' ')
    index = ''
    if len(postcode) >  0:
        if postcode[0] in search:
            index = search.index(postcode[0])
        return index, int(postcode[0])
    else:
        return None, None

# 41220
# 14126
@router.post('/search')
async def search(query: SearchQuery):
    try:
        await create_query({'query': query.query, 'timestamp': datetime.now().replace(microsecond=0)})
    except:
        pass
    userQuery = query.query.split(' ')
    
    search = query.query.split(' ')

    index, number = get_number(query.query)
    if index != None:
        del search[index]

    index, postcode = get_postcode(query.query)
    if index != None:
        del search[index-1]

    searchQuery = ' '.join(search)

    # user provided number and postcode
    if number != None and postcode != None:
        number_postcode_search_query = {
            "bool": {
            "must": [
                {
                "query_string": {
                    "fields": ['road^10', 'ward^5'],
                    "query": searchQuery
                }
                },
                {
                "terms": { 
                    "number": [number]
                }
                },
                {
                "terms": { 
                    "postcode": [postcode]
                }
                }
            ]
            }
        }
        response = es.search(index='addresses', size=5,
                             min_score=14, query=number_postcode_search_query)
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        return {'data': results}

    if number != None:
        number_search_query = {
            "bool": {
            "must": [
                {
                "multi_match": {
                    "fields": ['road^10', 'ward^5'],
                    "query": searchQuery
                }
                },
                {
                "terms": { 
                    "number": [number]
                }
                }
            ]
            }
        }
        response = es.search(index='addresses', size=50,
                             min_score=10, query=number_search_query)
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        return {'data': results}


    if postcode != None:
        postcode_search_query = {
            "bool": {
            "must": [
                {
                "multi_match": {
                    "fields": ['road^10', 'ward^5'],
                    "query": searchQuery
                }
                },
                {
                "terms": { 
                    "postcode": [postcode]
                }
                }
            ]
            }
        }
        response = es.search(index='addresses', size=50,
                             min_score=10, query=postcode_search_query)
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        return {'data': results}

    query = ' '.join(userQuery)
    response = es.search(index=['services', 'addresses'], size=70,
                            min_score=30, query={
                                'query_string': {
                                    #"fields": ['name^8', 'road^3'],
                                    'query': query
                                    }
                                }
                            )
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])
    return {'data': results}


    # if userQuery[0].isdigit():
    #     term = userQuery[0]
    #     del userQuery[0]
    #     query = ' '.join(userQuery)

    #     if len(term) == 5:
    #         search_query = {
    #             "bool": {
    #                 "must": [
    #                     {
    #                         "query_string": {"query": query}
    #                     },
    #                     {
    #                         "terms": {
    #                             "postcode": [term]
    #                         }
    #                     }
    #                 ]
    #             }
    #         }
    #     else:
    #         search_query = {
    #             "bool": {
    #                 "must": [
    #                     { "query_string": {"query": query}},
    #                     {"terms": {"number": [term]}}
    #                 ]
    #             }
    #         }

    #     response = es.search(index='addresses', size=20,
    #                          min_score=8, query=search_query)
    #     results = []
    #     for hit in response['hits']['hits']:
    #         results.append(hit['_source'])
    #     return {'data': results}

    # else:
    #     query = ' '.join(userQuery)
    #     response = es.search(index='addresses', size=20,
    #                          min_score=8, query={'query_string': {'query': query}})
    #     results = []
    #     for hit in response['hits']['hits']:
    #         results.append(hit['_source'])
    #     return {'data': results}


class GuidedQuery(BaseModel):
    road: str
    number: str
    postcode: str

# search by guide
@router.post('/search_guide')
async def search_guide(request: GuidedQuery):
    number = request.number
    postcode = request.postcode
    search_query = {
        "bool": {
            "must": [
                {
                "query_string": {
                    "fields": ['road'],
                    "query": request.road
                }
                },
                {
                "terms": { "number": [number]}
                },
                {
                "terms": { "postcode": [postcode]}
                }
            ]
        }
    }
    response = es.search(index='addresses', size=20,
                             min_score=4, query=search_query)
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])
    return {'data': results}

@router.get('/queries')
async def get_list_of_queries():
    return get_all_queries()