#!/bin/bash

set -e

echo "getting CSV"
CSVFILE=$(gsutil ls  gs://dryrun_biobank_samples_upload_bucket/*.CSV | tail -n 1)
gsutil cat "$CSVFILE" > biobank_sample.csv
echo "Got $CSVFILE"

python biobank_report.py > biobank_orders.csv
python reconcile.py biobank_sample.csv biobank_orders.csv reconciliation_report.csv

echo "Wrote report, uploading"
gsutil cp reconciliation_report.csv gs://dryrun_biobank_samples_upload_bucket/reconciliation/report_$(date -u +"%Y-%m-%d").csv
echo "uploaded"
date -u +"%Y-%m-%d"
