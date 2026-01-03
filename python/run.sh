#!/usr/bin/env bash


# Sort entries
python3 ./entries-sort.py

# Update gåvomottagare from Masterdata
python3 ./entries-update-gåvomottagare.py

# Update varningslistan from Masterdata
python3 ./entries-update-varningslistan.py
python3 ./entries-masterdata-lookup.py

# Filter YAML
python3 ./entries-filter.py

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
git add ../yaml/swish-123-datasource.yaml
git add ../json/swish-123-datasource.json
git add ../text/swish-123-datasource.csv
git add ../text/swish-123-datasource.tsv
git add ../xml/swish-123-datasource.xml
git add ../yaml/masterdata-organisations.yaml

#git add ../swish-123.md
#git add ../swish-123.pdf

git commit -m "Automated commit"

git push

python3 yaml-knockout-tests.py
