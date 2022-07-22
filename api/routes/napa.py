from pydantic import BaseModel
from fastapi import APIRouter, Response
from elasticsearch import Elasticsearch

router = APIRouter()


es = Elasticsearch("http://172.17.0.1:9200")


class SearchQuery(BaseModel):
    query: str


@router.get(
    "/index",
)
async def index():
    return {'message': 'NaPA API'}


@router.post('/search')
async def search(query: SearchQuery):
    response = es.search(index='napa-roads', size=8, min_score=8,
                         query={'query_string': {'query': query.query}})
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])
    return {'data': results}


@router.post('/search_services')
async def search(query: SearchQuery):
    response = es.search(index='napa-services', size=20, min_score=8,
                         query={'query_string': {'query': query.query}})
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])
    return {'data': results}


@router.post('/search_address')
async def search(query: SearchQuery):
    query = query.query.split(' ')
    if query[0].isdigit():
        term = query[0]
        del query[0]
        query = ' '.join(query)
        response = es.search(index='napa-addresses', size=20,
                             min_score=8, query={
                                 "bool": {
                                     "must": [
                                         {
                                             "query_string": {"query": query}
                                         },
                                         {
                                             "terms": {
                                                 "number": [term]
                                             }
                                         }
                                     ]
                                 }
                             })
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        return {'data': results}

    else:
        query = ' '.join(query)
        response = es.search(index='napa-addresses', size=20,
                            min_score=8, query={'query_string': {'query': query}})
        results = []
        for hit in response['hits']['hits']:
            results.append(hit['_source'])
        return {'data': results}
