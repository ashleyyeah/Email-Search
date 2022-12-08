# Personalized Email Search Extension for Your Browser

### A local chrome extension that can be used to search your emails using Gmail's mbox dumps.

<br>

# Table of Contents

- [Project Stack](#stack)
- [Technical Details](#technical)
- [How to Run the Project On Your Local Machine](#templates)
    - [Requirements](#requirements)
    - [Downloading Your Gmail Takeout](#gmail)
    - [Creating the Search Index](#search_index)
    - [Running the Search API](#search_api)
    - [Adding the Chrome Extension](#chrome_extension)
- [Get Feedback](#feedback)
- [Acknowledgements](#acknowledgements)

<br>

# Project Stack <a name = "stack"></a>

### Python 3.7+

### Mbox and Text Processing
- [mailbox](https://docs.python.org/3/library/mailbox.html)
- [email](https://docs.python.org/3/library/email.html#module-email)  
- [Beautiful Soup 4 (4.11.1)](https://beautiful-soup-4.readthedocs.io/en/latest/#)
- [re](https://docs.python.org/3/library/re.html)
- [spacy (3.4.3)](https://spacy.io/usage/v3-4)

### Email Indexing, Tokenizing, and Searching
- [Whoosh (2.7.4)](https://whoosh.readthedocs.io/en/latest/intro.html)

### Search Engine Exposure
- [Flask (2.2.2)](https://flask.palletsprojects.com/en/2.2.x/)

### Chrome Extension
- [ReactTS](https://create-react-app.dev/)

# Technical Details <a name = "technical"></a>

This project is a full-stack implementation of an email search engine. For the search engine backend, I have used python and it's many available packages for text parsing, language processing and search engine implementation. Specifically, for .mbox format parsing, I used `Beautiful Soup`, for text cleaning and formatting, I used a combination of python's regex library and the `spacy` library's NLP model for lemmatizing the email texts'. For the search engine library, I utilized `Whoosh`, which is a pure python search engine library that tokenizes the text to your specifications, indexes all of the emails, and allows for searching by scoring query matches with the **BM25** function.

With the search engine setup with the given Gmail mbox, to expose the search engine, I have created a minimal python `flask` API that allows queries to be made to a localhost port. 

Lastly, the chrome extension interface was implemented using ReactTS and gives the user a search interface to search and preview their emails, as well as redirect them to their actual email in Gmail.

