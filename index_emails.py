import os
import re
import mailbox
import json
from bs4 import BeautifulSoup

# https://stackoverflow.com/questions/7166922/extracting-the-body-of-an-email-from-mbox-file-decoding-it-to-plain-text-regard
def getcharsets(msg):
    charsets = set({})
    for c in msg.get_charsets():
        if c is not None:
            charsets.update([c])
    # print("charsets: " + charsets)
    return charsets

def getBody(msg):
    while msg.is_multipart():
        msg=msg.get_payload()[0]
    t=msg.get_payload(decode=True)
    for charset in getcharsets(msg):
        t=t.decode(charset)
    return t

def strip_html_css_js(msg):
    soup = BeautifulSoup(msg, "html.parser")  # create a new bs4 object from the html data loaded
    for script in soup(["script", "style"]):  # remove all javascript and stylesheet code
        script.extract()
    # get text
    text = soup.get_text()
    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'[^a-zA-Z0-9 ]', ' ', text)
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
    msgs["messages"].append({ 
        "date": message['date'],
        "from": message['from'],
        "subject": strip_html_css_js(message['subject']),
        "body": strip_html_css_js(getBody(message)) 
    })
    if i == 20:
        break

f.write(json.dumps(msgs, indent=4))
f.close()