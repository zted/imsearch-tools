"""
Downloads search engine query results into html files.
"""
import os
import sys
import time
import warnings

import imsearchtools as ist
from imsearchtools.utils import result_page_gen

warnings.filterwarnings("ignore")


def download_htmls(wordlist, dir_root, numresults):
    """
    given a text file with a list of words, download them into a directory
    a folder with the name of the query word is created for each query word,
    in the folder contains the file 'wordname.html', containing all the results
    Args:
        wordlist: list of words we want to query for
        dir_root: folder that you want to save all the queries to
        numresults: number of results you want to return per query

    Returns: Nothing
    """

    from imsearchtools.engines.search_client import QueryException

    searcher = ist.query.BingAPISearch()
    # or google or flickr
    for n, query_string in enumerate(wordlist):
        t = time.time()
        # TODO: exception handler for queries not found, implement handler,
        # perhaps because internet disconnected that results cannot be retrieved.
        # put a counter here or something
        print 'Querying for string "{}"'.format(query_string)
        try:
            results = searcher.query(query_string, num_results=numresults)
        except QueryException:
            print('Could not find word, moving on to next')
            continue
        results_copy = results[:]

        print 'Retrieved %d result URLs in %f seconds' % (len(results), (time.time() - t))
        outdir = dir_root + '/' + query_string
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        html_fn = '{0}/{1}.html'.format(outdir, query_string)
        result_page_gen.gen_results_page(results_copy, 'BingAPISearch()',
                                         html_fn, show_in_browser=False)
        time.sleep(1.0)
        # allow the search engine some time before performing another query
    return


if __name__ == "__main__":

    working_directory = sys.argv[1]
    if not(os.path.isdir(working_directory)):
        raise EnvironmentError("Directory entered is not a valid path")
    t = time.time()
    words_file = sys.argv[2]
    num_results = 700
    word_list = []
    with open(words_file, 'r') as f:
        for line in f:
            word = line.rstrip('\n')
            word_list.append(word)
    print('Total number of words processed: {}'.format(len(word_list)))
    print('Last word processed: {}'.format(word))
    download_htmls(word_list, working_directory, num_results)
    print('Total number of words processed: {}'.format(len(word_list)))
    print('Last word processed: {}'.format(word))
    print('Whole operation took {} seconds'.format(time.time() - t))
