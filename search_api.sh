#!/bin/bash

cd backend
pip install -r requirements.txt
python clean_mbox.py
python create_index.py
flask run