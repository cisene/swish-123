#!/usr/bin/env bash


# Sort entries
python3 ./entries-sort.py

# Uppdate gåvomottagare from Masterdata
python3 ./entries-update-gåvomottagare.py

# Render JSON
python3 ./entries-to-json.py

# Render CSV
python3 ./entries-to-csv.py

# Render TSV
python3 ./entries-to-tsv.py

# Render XML
python3 ./entries-to-xml.py


# Add to git
git add ../yaml/entries.yaml
git add ../json/swish-123-datasource.json
git add ../text/swish-123-datasource.csv
git add ../text/swish-123-datasource.tsv
git add ../xml/swish-123-datasource.xml

git commit -m "Automated commit"

git push

python3 yaml-knockout-tests.py
