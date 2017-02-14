from google.cloud import datastore
import datetime
import sys
import os

"""Biobank report generator
Runs locally, after "gcloud beta auth application-default login"
with an account that has access to the dryrun environment"""

PROJECT = 'all-of-us-rdr-dryrun'
START_DATE = os.environ['DRY_RUN_START']
DRY_RUN_START = datetime.datetime.strptime(START_DATE, "%Y-%m-%d" )
BIOBANK_ID_SYSTEM = 'https://orders.mayomedicallaboratories.com'
SITE_ID_SYSTEM = 'https://www.pmi-ops.org/mayolink-site-id'

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
  printrow(['biobank_id', 'biobank_order_id', 'site_id', 'test_label', 'collected_time'])
  for r in q.fetch():
    if 'samples' not in r: continue
    if BIOBANK_ID_SYSTEM not in r['identifier.system']:
        continue
    biobank_order_id = r['identifier.value'][r['identifier.system'].index(BIOBANK_ID_SYSTEM)]

    site_id = "0"
    if SITE_ID_SYSTEM in r['identifier.system']:
        site_id= r['identifier.value'][r['identifier.system'].index(SITE_ID_SYSTEM)]
        if '.' in site_id:
            site_id = site_id.split('.')[0]

    for s in r['samples']:
      if s['finalized']:
        parent = get_participant(r.key.parent)
        if parent['biobank_id']:
          row = (parent['biobank_id'], biobank_order_id, site_id,  s['test'], s['collected'].isoformat())
          printrow(row)

if __name__ == '__main__':
  generate_report()
