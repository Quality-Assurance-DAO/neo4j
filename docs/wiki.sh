#!/bin/bash
WIKI_REPO="https://github.com/Quality-Assurance-DAO/neo4j.wiki.git"
LOCAL_WIKI_DIR="wiki"

# Clone the Wiki repo
git clone $WIKI_REPO $LOCAL_WIKI_DIR

# Copy docs to wiki
cp -r docs/* $LOCAL_WIKI_DIR/

# Commit and push
cd $LOCAL_WIKI_DIR
git add .
git commit -m "Update Wiki from docs"
git push origin master
cd ..
rm -rf $LOCAL_WIKI_DIR
