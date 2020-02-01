#!/usr/bin/env python
# encoding=utf-8
INDEX_DIR = "IndexFiles.index"

import sys, os, lucene

from java.io import File
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import BooleanClause
import jieba
import re

def parseCommand(command):
    allowed_opt = ['site']
    command_dict = {}
    opt = 'contents'
    for i in command.split(' '):
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command = " ".join(jieba.cut(i))
            command_dict[opt] = command_dict.get(opt, '') + ' ' + i
    return command_dict

def run_pic(valueFromOut, searcher, analyzer):
    command = valueFromOut

    seg_list = jieba.cut(command)
    command = " ".join(seg_list)
    if command == '':
        return

    result = []
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 10).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        partResult = {}

        partResult['title'] = doc.get('title')
        partResult['url'] = doc.get('url')
        partResult['imgurl'] = doc.get('imgurl')

        result.append(partResult)

    return result


def run_txt(valueFromOut, searcher, analyzer):
    command = valueFromOut

    seg_list = jieba.cut(command)
    command = " ".join(seg_list)
    if command == '':
        return
    result = []
    command_dict = parseCommand(command)
    querys = BooleanQuery()
    for k, v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)
        querys.add(query, BooleanClause.Occur.MUST)
    scoreDocs = searcher.search(querys, 10).scoreDocs
    print "%s total matching documents." % len(scoreDocs)

    for scoreDoc in scoreDocs:
        doc = searcher.doc(scoreDoc.doc)
        partResult = {}

        partResult['title'] = doc.get('title')
        partResult['url'] = doc.get('url')
        contents_raw = doc.get('contents_raw')
        keywords = list()
        if 'contents' in command_dict:
            keywords += list(jieba.cut(command_dict['contents']))
        beginning = min(map(contents_raw.find, keywords))
        if beginning < 0:
            continue
        para = contents_raw[max(0, beginning - 10): beginning + 50]
        for keyword in keywords:
            para = para.replace(keyword.strip(), '<span style="color:blue;font-weight:bold">'+keyword+'</span>')
        partResult['keyword'] = para
        result.append(partResult)

    return result


STORE_DIR = "index_6"
vm_env = lucene.initVM(vmargs=['-Djava.awt.headless=true'])


def lab7txtSearch(valueFromOut):
    vm_env.attachCurrentThread()
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    result = run_txt(valueFromOut, searcher, analyzer)
    del searcher
    return result

STORE_DIR_pic = "indeximg"


def lab7picSearch(valueFromOut):
    vm_env.attachCurrentThread()
    print 'lucene', lucene.VERSION
    # base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR_pic))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = StandardAnalyzer(Version.LUCENE_CURRENT)
    result = run_pic(valueFromOut, searcher, analyzer)
    del searcher
    return result
