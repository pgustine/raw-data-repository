CSVFILE=$(gsutil ls  gs://staging_biobank_samples_upload_bucket/*.CSV | tail -n 1)
gsutil cat "$CSVFILE" > biobank_sample.csv
python biobank_report.py > biobank_orders.csv
python reconcile.py biobank_sample.csv biobank_orders.csv reconciliation_report.csv
