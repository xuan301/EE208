#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import jieba
import re
import sys, os, lucene, threading, time
from datetime import datetime
from my_load import load
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
#from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)
count=0
class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
        analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print 'commit index',
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print 'done'

    def indexDocs(self, root, writer):
        global count

        t1 = FieldType()
        t1.setIndexed(False)
        t1.setStored(True)
        t1.setTokenized(False)
        
        t2 = FieldType()
        t2.setIndexed(True)
        t2.setStored(True)
        t2.setTokenized(True)
        t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        
        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                try:
                    data=load(filename)
                    raw_title = data['title']
                    title = ' '.join(jieba.cut_for_search(raw_title))
                    print title
                    print "adding", filename
                    doc = Document()
                    doc.add(Field("raw_title", raw_title, t1))
                    doc.add(Field("filename", filename, t1))
                    doc.add(Field("url", data['url'], t1))
                    doc.add(Field("title", title, t2))
                    doc.add(Field("ctime",str(data['ctime']),t1))
                    doc.add(Field("content", data['content'], t1))
                    for img in data['realimgs']:
                        doc.add(Field("imgs",img[1],t1))
                        doc.add(Field("imgurls",img[0],t1))
                    writer.addDocument(doc)
                    count+=1
                except Exception, e:
                    print "Failed in indexDocs:", e

if __name__ == '__main__':
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    try:
        IndexFiles('data', "index")
        print count
        end = datetime.now()
        print end - start
    except Exception, e:
        print "Failed: ", e
        raise e
