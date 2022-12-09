# Personalized Email Search Extension for Your Browser

### A local chrome extension that can be used to search your emails using Gmail's mbox dumps.  

<br>

### Tutorial Video Link: https://drive.google.com/file/d/1qh5PhN8BvJC0O1fBLAIAEE6hthWDPVrX/view?usp=sharing

<br>

# Table of Contents

- [Project Stack](#stack)
- [Technical Details](#technical)
- [Project Setup Tutorial](#tutorial)
    - [Machine Requirements](#requirements)
    - [Downloading Your Gmail Takeout](#gmail)
    - [Running the Search Backend](#search)
    - [Adding the Chrome Extension](#chrome_extension)

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

# Project Setup Tutorial <a name = "tutorial"></a>

*Note: The project is desiged to run on Mac/Linus so if you'reon a windows machine, it's best to use a Linux VM or [WSL](https://learn.microsoft.com/en-us/windows/wsl/install).  

## Requirements <a name = "requirements"></a>

You will need the following before beginning the setup process:

- Your Gmail Account
- Google Chrome Browser
- [Python 3.7+](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/getting-started/) 
- git clone https://github.com/ashleyyeah/Email-Finder-Extension.git into a folder of your choice

## 1) Downloading you Gmail Takeout <a name = "technical"></a>

Because of the sensitivity of personal emails, I didn't think it would be suitable to upload my email mbox, so you will have to use your own email mbox to search for your emails. To do so first visit: https://takeout.google.com/settings/takeout

From there you will be met with this screen:

<img src="./screenshots/Screenshot%202022-12-06%20at%202.30.11%20PM.jpg" alt="drawing" width="600"/>

Go ahead and choose to `Deselect all` and then scroll down to the mail section:

<img src="./screenshots/Screenshot%202022-12-06%20at%202.30.39%20PM.jpg" alt="drawing" width="600"/>  

From here you can choose to either download all of your mail data or choose some specific labels:

<img src="./screenshots/Screenshot%202022-12-06%20at%202.30.59%20PM.jpg" alt="drawing" width="600"/> 

You can then continue to the next step, where you will choose to have the download link emailed to you once:

<img src="./screenshots/Screenshot%202022-12-06%20at%202.31.43%20PM.jpg" alt="drawing" width="600"/> 
<img src="./screenshots/Screenshot%202022-12-06%20at%202.32.41%20PM.jpg" alt="drawing" width="600"/> 

Once you hit create export, you'll be prompted that this download could take hours to days. Since you're only downloading your email and not all of your Google data, it should only take a few hours. From personal experience, my download link was ready in about 2 hours.

When the link is ready, you'll receive an email that looks like this:

<img src="./screenshots/Screenshot%202022-12-08%20at%204.24.40%20PM.jpg" alt="drawing" width="600"/> 

You can go ahead and download your files, which will download as a zip file. When you unzip the file, you will get a `Takeout` folder, with a `Mail` subfolder. Here, you can find the `All mail including Spam and Trash.mbox` file.

<img src="./screenshots/Screenshot%202022-12-08%20at%204.27.27%20PM.jpg" alt="drawing" width="700"/> 

Please rename the file to `emails.mbox` and copy and paste this file into the backend folder of your local version of this project.

Your local project directory should now look like this:

    .
    ├── backend
    │   ├── app.py          
    │   ├── clean_mbox.py    
    │   ├── create_index.py      
    │   ├── emails.mbox          
    │   ├── index_search.py       
    │   └── requirements.txt       
    ├── chrome-extension
    ├── screenshots
    └── ...

## 2) Running the Search Backend <a name = "search"></a>

Open up a terminal and navigate the your local project folder. From there you can run the executable bash script `search_api.sh`.  You may need to give the file executable permission like so:

```
chmod +x search_api.sh
```
Then, you can go ahead and execute the script like so:

```
./search_api.sh
```

This will clean your Gmail mbox file and create an index for all of your emails. This whole process may take a few minutes, so don't be concerned if nothing happens for awhile. Once done, the script will open the search engine server on your `localhost:5000`. Please leave the flask server running as it is required for the extension to work.

## 3) Adding the Chrome Extension <a name = "chrome_extension"></a>

Go to your Google Chrome browser and visit: [chrome://extensions/](chrome://extensions/)

From here, turn on `Developer mode` and click on `Load unpacked`:

<img src="./screenshots/Screenshot%202022-12-08%20at%204.53.06%20PM.jpg" alt="drawing" width="600"/> 

Navigate to the folder of the project and then under the `chrome-extension` folder, select the `build` folder

<img src="./screenshots/Screenshot%202022-12-08%20at%205.00.34%20PM.jpg" alt="drawing" width="500"/>

Now that you have loaded the extension, you can go ahead and visit the Gmail site and use it to find some long lost emails in your inbox!

<img src="./screenshots/Screenshot%202022-12-08%20at%205.34.03%20PM.jpg" alt="drawing" width="500"/>