#!/usr/bin/python3.6
from dateutil import parser as dateutilparser
from datetime import datetime

import os

import argparse

from collections import namedtuple

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

from dialog import Dialog


argparser = argparse.ArgumentParser(
    description="List tlog sessions that can be played back")
argparser.add_argument("--es-host", required=True,
                       help="Elasticsearch server hostname[:port]")
argparser.add_argument("--es-index", required=True,
                       help="Index tlog stores recordings in")
argparser.add_argument("--query", required=False, default="*",
                       help="Elasticsearch query string, see https://github.com/Scribery/tlog#playing-back-from-elasticsearch for example query string")
args = vars(argparser.parse_args())

#Add ES port
if ":" not in args['es_host']:
    args['es_host'] = args['es_host'] + ":9200"

ESClient = Elasticsearch(hosts=[args['es_host']])

Recording = namedtuple(
    'Recording', ['rec', 'host', 'session', 'user', 'timestamp'])

s = Search(using=ESClient, index=args['es_index']).query(
    'query_string', query=args['query']).query("match", id=1)

esresults = [y['_source'] for y in s.execute().to_dict()['hits']['hits']]

recordinglist = [Recording(x['rec'], x['host'], x['session'], x['user'],
                           dateutilparser.parse(x['timestamp'])) for x in esresults]

# Sort recordings by time
recordinglist.sort(key=lambda r: r.timestamp, reverse=True)

dialoglist = []
for i in range(len(recordinglist)):
    r = recordinglist[i]
    timestamp = datetime.fromtimestamp(r.timestamp.timestamp()).strftime("%F %T") #local timezone
    dialoglist.append((str(i), f"user: {r.user}, host: {r.host}, time: {timestamp}"))

d = Dialog(autowidgetsize=True)

code, tag = d.menu("Choose recording", choices=dialoglist)

tlog_rec = recordinglist[int(tag)].rec
os.system("reset")
os.system(f"tlog-play -r es --es-baseurl=http://{args['es_host']}/{args['es_index']}/tlog/_search --es-query=rec:{tlog_rec}")
