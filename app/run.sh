#!/bin/bash

# git config --global --add safe.directory /app/volume/git_repo/.git
git clone -b $GIT_BRANCH --depth 1 $GIT_REPO git_repo
cd git_repo
pip install -r requirements.txt
cd ..

flask run --host=0.0.0.0 --port=5000 &
FLASK_PID=$!

streamlit run git_repo/app.py --server.port 8501 --server.headless true &
STREAMLIT_PID=$!

sleep 5
service nginx start

wait $FLASK_PID $STREAMLIT_PID