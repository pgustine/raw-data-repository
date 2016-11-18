from google.cloud import datastore
import datetime
import sys

"""Biobank report generator
Runs locally, after "gcloud beta auth application-default login"
with an account that has access to the staging environment"""

PROJECT = 'all-of-us-rdr-staging'
DRY_RUN_START = datetime.datetime(2016, 11, 1)
BIOBANK_ID_SYSTEM = 'https://orders.mayomedicallaboratories.com'

c = datastore.Client(project=PROJECT, namespace='')
cache = {}
def get_participant(pid):
  if pid not in cache:
    cache[pid] = c.get(pid)
  return cache[pid]

def printrow(row):
  print '\t'.join(row)

def generate_report():
  q = c.query(kind='BiobankOrder', order=['created'], filters=[['created', '>=', DRY_RUN_START]])
  printrow(['biobank_id', 'biobank_order_id', 'test_label', 'finalized_time'])
  for r in q.fetch():
    if 'samples' not in r: continue
    biobank_order_id = r['identifier.value'][r['identifier.system'].index(BIOBANK_ID_SYSTEM)]
    for s in r['samples']:
      if s['finalized']:
        parent = get_participant(r.key.parent)
        if parent['biobank_id']:
          row = (parent['biobank_id'], biobank_order_id, s['test'], s['finalized'].isoformat())
          printrow(row)

if __name__ == '__main__':
  generate_report()
