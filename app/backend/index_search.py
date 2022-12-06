from whoosh import index, qparser
from whoosh.qparser import QueryParser
from whoosh.sorting import FieldFacet

dirname = "index_dir"

def index_search(search_query):
    print('we\'re in')
    ix = index.open_dir(dirname)
    schema = ix.schema
    
    og = qparser.OrGroup.factory(0.9)
    mp = qparser.MultifieldParser(['title','content'], schema, group = og)
    
    q = mp.parse(search_query)

    facet = FieldFacet("date", reverse=True)

    with ix.searcher() as s:
        results = s.search(q, terms=True, limit = 20)
        print("Search Results: ")

        messages = []
        
        for i in range(min(len(results), 20)):
            # print(results[i]['title'], results[i]['date'])
            messages.append({
                'title': results[i]['title'],
                'date': str(results[i]['date']),
                'body': results[i]['body']
            })
        
        return messages

    
# results_dict = index_search("")