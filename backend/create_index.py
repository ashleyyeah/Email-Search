import json
import os, os.path
from whoosh.fields import Schema, TEXT, ID, DATETIME
from whoosh import index
from datetime import datetime

f = open('emails.json')
data = json.load(f)

schema = Schema(title=TEXT(stored=True), 
                date=DATETIME(stored=True, sortable=True), 
                path=ID(stored=True),
                body=TEXT(stored=True), 
                content=TEXT(stored = True))

if not os.path.exists("index_dir"):
    os.mkdir("index_dir")

ix = index.create_in("index_dir", schema)
writer = ix.writer()

for i, msg in enumerate(data['messages']):
    msg_date = datetime.now()
    try:
        msg_date = datetime.strptime(msg['date'], "%Y-%m-%d %H:%M:%S%z")
    except Exception:
        msg_date = datetime.strptime(msg['date'], "%Y-%m-%d %H:%M:%S")
    writer.add_document(title=msg['subject'], content=msg['body'], body=msg['raw_body'], path=str(i), date=msg_date)
writer.commit()

f.close()