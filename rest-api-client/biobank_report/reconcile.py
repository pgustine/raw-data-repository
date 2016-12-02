from __future__ import print_function
import csv
import json
import sys
from collections import defaultdict


samples = open(sys.argv[1])
orders = open(sys.argv[2])
report = open(sys.argv[3], "w")

orders_reader = csv.DictReader(orders, delimiter='\t')
samples_reader = csv.DictReader(samples, delimiter='\t')

received_samples = {}
# only want root-level samples, not aliquots
#for r in filter(lambda s: 'Parent Sample Id' not in s or s['Parent Sample Id'] == '', samples_reader):
for r in samples_reader:
  key = (r['External Participant Id'], r['Test Code'])
  received_samples[key] = r

sent_samples = {}
for r in orders_reader:
  key = (r['biobank_id'], r['test_label'])
  sent_samples[key] = r

sent_only = set(sent_samples.keys()) - set(received_samples.keys())
received_only = set(received_samples.keys()) - set(sent_samples.keys())
sent_and_received = set(received_samples.keys()) & set(sent_samples.keys())

print("sent but not received", len(sent_only))
print("received but not sent", len(received_only))
print("sent and received", len(sent_and_received))

def print_row(r, file=None):
  print("\t".join([str(e) for e in r]), file=file)

#print_row(["biobank_id", "sent_order_id", "sent_test", "sent_time", "received_test", "received_time", "test_match", "date_match", "sent_json", "received_json"], report)
print_row(["biobank_id", "sent_order_id", "sent_test", "sent_time", "received_test", "received_time", "test_match", "date_match"], report)
for k in sorted(set(sent_samples.keys() + received_samples.keys())):
  biobank_id = k[0]
  test_label = k[1]
  sent_order_id = ""
  sent_test = ""
  sent_time = ""
  received_test = ""
  received_time = ""

  if k in sent_samples:
    sample = sent_samples[k]
    sent_test = test_label
    sent_time = sample['finalized_time'][:10]
    sent_json = json.dumps(sample)
    sent_order_id = sample['biobank_order_id']

  if k in received_samples:
    sample = received_samples[k]
    received_test = test_label
    received_json = json.dumps(sample)
    received_time = sample['Sample Family Collection Date'][:10].replace('/','-')

  test_match = sent_test and (sent_test == received_test)
  date_match = sent_time and (sent_time == received_time)
  #row = [biobank_id, sent_order_id, sent_test, sent_time, received_test, received_time, test_match, date_match, sent_json, received_json]
  row = [biobank_id, sent_order_id, sent_test, sent_time, received_test, received_time, test_match, date_match]
  print_row(row, report)
