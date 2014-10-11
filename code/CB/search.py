#!/usr/bin/env python
#coding=utf8

import json
import logging
import sys
import xapian

from util import log_matches


### Start of example code.
def search(index_file_path, querystring, offset=0, ret_num=10):
    # offset - defines starting point within result set
    # ret_num- defines number of records to retrieve

    # Open the database we're going to search.
    db = xapian.Database(index_file_path)

    # Set up a QueryParser with a stemmer and suitable prefixes
    queryparser = xapian.QueryParser()
    #queryparser.set_stemmer(xapian.Stem("en"))
    #queryparser.set_stemming_strategy(queryparser.STEM_SOME)
    queryparser.add_prefix("title", "tt")
    queryparser.add_prefix("content", "cn")

    # And parse the query
    query = queryparser.parse_query(querystring)

    #print 'query in xapian is : ', query

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches, ret_res = [], []
    for match in enquire.get_mset(offset, ret_num):
        fields = json.loads(match.document.get_data())
        #print u"%(rank)i: #%(docid)3.3i, %(newsid)s %(title)s--%(content)s" % {
        #    'rank': match.rank + 1,
        #    'docid': match.docid,
        #    'newsid': fields.get('newsid', u''),
        #    'title': fields.get('title', u''),
        #    'content': fields.get('content', u'')[:50],
        #    }
        #matches.append(match.docid)
        ret_res.append(fields.get('newsid', '-1'))

    # Finally, make sure we log the query and displayed results
    log_matches(querystring, offset, ret_num, matches)
    return ret_res

def main():
    logging.basicConfig(level=logging.INFO)
    querystr = 'title:马航'
    search(index_file_path, querystr)

if __name__ == '__main__':
    main()
