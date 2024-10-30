#!/bin/bash

pip install --upgrade pip
pip install -r requirements.txt

streamlit run streamlit_present.py --server.port 8080