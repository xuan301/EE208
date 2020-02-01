#!/usr/bin/env python

INDEX_DIR = "IndexFiles.index"

import sys, os, lucene, threading, time, re
import jieba
from datetime import datetime
from bs4 import BeautifulSoup

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer
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


class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)

        store = SimpleFSDirectory(File(storeDir))
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

        # t1 = FieldType()
        # t1.setIndexed(True)
        # t1.setStored(True)
        # t1.setTokenized(False)
        # t1.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS)

        # t2 = FieldType()
        # t2.setIndexed(True)
        # t2.setStored(False)
        # t2.setTokenized(True)
        # t2.setIndexOptions(FieldInfo.IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

        if not root.endswith('.txt'):
            print "Please give the index file end with .txt !"
            return

        index_file = open(root)
        for line in index_file.readlines():
            url_and_name = line.split()
            url = url_and_name[0]
            filename = url_and_name[1]
            print "adding", filename
            try:
                path = os.path.join("html", filename)
                file = open(path)
                contents = file.read()
                soup = BeautifulSoup(contents, features="html.parser")
                if soup.head.title:
                    title = soup.head.title.string
                    title = jieba.cut(title)
                    if title:
                        title = ' '.join(title)
                    else:
                        title = ' '
                else:
                    title = ' '
                contents = ''.join(soup.findAll(text=True))
                file.close()
                doc = Document()
                doc.add(Field("title", title,
                              Field.Store.YES,
                              Field.Index.ANALYZED))
                doc.add(Field("name", filename,
                              Field.Store.YES,
                              Field.Index.NOT_ANALYZED))
                doc.add(Field("path", path,
                              Field.Store.YES,
                              Field.Index.NOT_ANALYZED))
                doc.add(Field("url", url,
                              Field.Store.YES,
                              Field.Index.NOT_ANALYZED))
                if len(contents) > 0:
                    doc.add(Field("contents", contents,
                                  Field.Store.NO,
                                  Field.Index.NOT_ANALYZED))
                else:
                    print "warning: no content in %s" % filename
                writer.addDocument(doc)
            except Exception, e:
                print "Failed in indexDocs:", e
        index_file.close()


if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf8')
    """
    if len(sys.argv) < 2:
        print IndexFiles.__doc__
        sys.exit(1)
    """
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', lucene.VERSION
    start = datetime.now()
    # try:
    """
            base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
            IndexFiles(sys.argv[1], os.path.join(base_dir, INDEX_DIR),
                       StandardAnalyzer(Version.LUCENE_CURRENT))
                       """
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    IndexFiles('index.txt', "index", analyzer)
    end = datetime.now()
    print end - start
    # except Exception, e:
        # print "Failed: ", e
        # raise e
