from __future__ import print_function
import csv
import json
import sys
import datetime
import os
from collections import defaultdict

START_DATE = os.environ['DRY_RUN_START']
DRY_RUN_START = datetime.datetime.strptime(START_DATE, "%Y-%m-%d" )
print("START", DRY_RUN_START)


samples = open(sys.argv[1])
orders = open(sys.argv[2])
report = open(sys.argv[3], "w")

orders_reader = csv.DictReader(orders, delimiter='\t')
samples_reader = csv.DictReader(samples, delimiter='\t')

received_samples = {}
# only want root-level samples, not aliquots
for r in filter(lambda s: 'Parent Sample Id' not in s or (not s['Parent Sample Id']), samples_reader):
  key = (r['External Participant Id'], r['Test Code'])
  if key not in received_samples:
    received_samples[key] = []
  received_samples[key].append(r)

sent_samples = {}
for r in orders_reader:
  key = (r['biobank_id'], r['test_label'])
  if key not in sent_samples:
    sent_samples[key] = []
  sent_samples[key].append(r)

sent_only = set(sent_samples.keys()) - set(received_samples.keys())
received_only = set(received_samples.keys()) - set(sent_samples.keys())
sent_and_received = set(received_samples.keys()) & set(sent_samples.keys())

print("sent but not received", len(sent_only))
print("received but not sent", len(received_only))
print("sent and received", len(sent_and_received))

def print_row(r, file=None):
  print("\t".join([str(e) for e in r]), file=file)

print_row(["biobank_id", "sent_order_id", "site_id", "sent_test", "sent_time", "received_test", "received_time", "test_match", "date_match"], report)
for k in sorted(set(sent_samples.keys() + received_samples.keys())):
  biobank_id = k[0]
  test_label = k[1]
  sent_order_id = ""
  sent_test = ""
  sent_time = ""
  received_test = ""
  received_time = ""
  site_id = ""

  sent_json = ""
  received_json = ""

  if k in sent_samples:
    # just look for the most recent shipment of this testCode
    sent_samples[k] = sorted(sent_samples[k], key=lambda v: v['collected_time'], reverse=True)
    sample = sent_samples[k][0]
    sent_test = test_label
    sent_time = sample['collected_time'][:10]
    sent_json = json.dumps(sample)
    sent_order_id = sample['biobank_order_id']
    site_id = sample['site_id']

  if k in received_samples:
    # just look for the most recent receipt of this testCode
    received_samples[k] = sorted(received_samples[k], key=lambda v: v['Sample Confirmed Date'], reverse=True)
    sample = received_samples[k][0]
    received_test = test_label
    received_json = json.dumps(sample)
    received_time = sample['Sample Confirmed Date'][:10].replace('/','-')

  if k not in sent_samples and received_time:
    if datetime.datetime.strptime(received_time, "%Y-%m-%d") < DRY_RUN_START:
      print("skipped because it's too early: ", received_time)
      continue

  test_match = sent_test and (sent_test == received_test)

  # TODO: allow these to be 1 day apart and still count as a "match"
  date_match = sent_time and (sent_time == received_time)
  #row = [biobank_id, sent_order_id, sent_test, sent_time, received_test, received_time, test_match, date_match, sent_json, received_json]
  row = [biobank_id, sent_order_id, site_id, sent_test, sent_time, received_test, received_time, test_match, date_match]
  print_row(row, report)
