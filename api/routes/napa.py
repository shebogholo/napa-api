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
    response = es.search(index='napa-roads', size=8, min_score=8, query={'query_string': {'query': query.query}})
    results = []
    for hit in response['hits']['hits']:
        results.append(hit['_source'])
    return {'data': results}
