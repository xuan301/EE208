#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene
import jieba

from java.io import File
#from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.util import Version
try:
    vm_env=lucene.initVM(vmargs=['-Djava.awt.headless=true'])
except:
    vm_env = lucene.getVMEnv()
"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""
def run(searcher, analyzer,command):
    vm_env.attachCurrentThread()
    while True:
        if command == '':
            return []
        command = ' '.join(jieba.cut_for_search(command))
        query = QueryParser(Version.LUCENE_CURRENT, "title",
                            analyzer).parse(command)
        scoreDocs = searcher.search(query, 50).scoreDocs
        result=[]
        for i, scoreDoc in enumerate(scoreDocs):
            doc = searcher.doc(scoreDoc.doc)
            result.append(doc.get("filename"))
            #print 'explain:', searcher.explain(query, scoreDoc.doc)
        return result

def Search_text(command):
    STORE_DIR = "index"
    # lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    vm_env.attachCurrentThread()
    print 'lucene', lucene.VERSION
    #base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    res=run(searcher, analyzer,command)
    del searcher
    return res
