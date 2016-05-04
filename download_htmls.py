import os
import sys
import time
import warnings

import imsearchtools as ist
from imsearchtools.utils import result_page_gen

warnings.filterwarnings("ignore")


def download_images(wordlist, dir_root, numresults):
    searcher = ist.query.BingAPISearch()
    for n, query_string in enumerate(wordlist):
        t = time.time()
        # example of querying for image URLs using Google Web engine
        # TODO: exception handler for queries not found, implement handler,
        # perhaps because internet disconnected that results cannot be retrieved.
        # put a counter here or something
        results = searcher.query(query_string, num_results=numresults)
        results_copy = results[:]

        print 'Retrieved %d result URLs in %f seconds' % (len(results), (time.time() - t))
        outdir = dir_root + '/' + query_string
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        html_fn = '{0}/{1}.html'.format(outdir, query_string)
        result_page_gen.gen_results_page(results_copy, 'BingAPISearch()',
                                         html_fn, show_in_browser=False)
        print 'Finished retrieving for query "{}"'.format(query_string)
        time.sleep(5.0)


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
    download_images(word_list, working_directory, num_results)
    print('Total number of words processed: {}'.format(len(word_list)))
    print('Last word processed: {}'.format(word))
    print('Whole operation took {} seconds'.format(time.time() - t))
