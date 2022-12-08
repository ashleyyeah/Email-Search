from whoosh import index, qparser
from whoosh.qparser import QueryParser
from whoosh.sorting import FieldFacet
import spacy

nlp = spacy.load('en_core_web_sm')

dirname = "index_dir"

def index_search(search_query):
    doc = nlp(search_query)
    
    # Tokenization and lemmatization
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)
    
    # Filter the stopwords
    filtered_sentence = [] 
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word) 

    search_query = ' '.join(filtered_sentence)

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
                'date': results[i]['date'].strftime('%Y/%m/%d'),
                'body': results[i]['body']
            })
        
        return messages

    
# results_dict = index_search("")