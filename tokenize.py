import os
import re
import mailbox
from email.header import decode_header, make_header
import json
from bs4 import BeautifulSoup
import spacy

nlp = spacy.load('en_core_web_sm')

# https://stackoverflow.com/questions/7166922/extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard
def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    return charsets

def getBody(msg):
    while msg.is_multipart():
        msg=msg.get_payload()[0]
    t=msg.get_payload(decode=True)
    for charset in getcharsets(msg):
        t=t.decode(charset)
    return t

def clean(msg):
    # remove html formatting
    soup = BeautifulSoup(msg, "html.parser")  # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.extract()
    
    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    # remove url links and unreadable characters + normalize text to lowercase
    text = re.sub(r'http\S+', ' ', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.lower()

    doc = nlp(text)
    
    # Tokenization and lemmatization
    lemma_list = []
    for token in doc:
        lemma_list.append(token.lemma_)
    
    # Filter the stopwords
    filtered_sentence =[] 
    for word in lemma_list:
        lexeme = nlp.vocab[word]
        if lexeme.is_stop == False:
            filtered_sentence.append(word) 

    return filtered_sentence

def clean_subject(subject):
    text = str(make_header(decode_header(subject)))
    text = re.sub(r'[^!-~]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

mbox = mailbox.mbox('mail/emails.mbox')
msgs = {
    "messages": []
}

if (os.path.exists("emails.json")):
    os.remove("emails.json")
f = open("emails.json", "a")
f.seek(0)

for i, message in enumerate(mbox):
    try:
        msgs["messages"].append({ 
            "date": message['date'],
            "from": message['from'],
            "subject": clean_subject(message['subject']),
            "body": clean(getBody(message)) 
        })
    except Exception as e: 
        print(i)
        print(e)

    # if i == 1000:
    #     break

f.write(json.dumps(msgs, indent=4))
f.close()