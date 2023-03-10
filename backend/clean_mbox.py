import os
import re
import mailbox
from email.header import decode_header, make_header
from email.utils import parsedate_to_datetime
import json
from bs4 import BeautifulSoup
import string
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

def clean(msg, raw=False):
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

    if raw:
        printable = set(string.printable)
        text = ''.join(filter(lambda x: x in printable, text))
        return text

    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    text = text.lower()

    doc = nlp(text)
    
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

    text = ' '.join(filtered_sentence)

    return text

def clean_subject(subject):
    text = str(make_header(decode_header(subject)))
    text = re.sub(r'[^!-~]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text

mbox = mailbox.mbox('emails.mbox')
msgs = {
    "messages": []
}

if (os.path.exists("emails.json")):
    os.remove("emails.json")
f = open("emails.json", "a")
f.seek(0)

print("--------------Start email cleaning--------------")

for i, message in enumerate(mbox):
    if (message['x-gmail-labels'] == 'Chat'):
        continue
    try:
        msgs["messages"].append({ 
            "date": str(parsedate_to_datetime(message['date'])),
            "from": message['from'],
            "subject": clean_subject(message['subject']),
            "body": clean(getBody(message)),
            "raw_body": clean(getBody(message), True)
        })
    except Exception as e: 
        print(i)
        print(e)

    # if i == 1000:
    #     break

f.write(json.dumps(msgs, indent=4))
f.close()