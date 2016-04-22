import imsearchtools as ist
import time
import os
from imsearchtools.utils import result_page_gen
import sys

def test_callback(out_dict):
    import json
    # print json.dumps(out_dict)
    time.sleep(0.2)


def download_images(wordsfile, dir_root):
    opts = ist.process.ImageProcessorSettings()
    opts.conversion['max_height'] = 256
    opts.conversion['max_width'] = 256
    opts.conversion['format'] = 'jpg'
    imgetter = ist.process.ImageGetter(opts=opts)
    searcher = ist.query.BingAPISearch()
    for query_string in wordsfile:
        print 'Executing Bing Image Search...'
        t = time.time()
        # example of querying for image URLs using Google Web engine
        # TODO: exception handler for queries not found, implement handler,
        # perhaps because internet disconnected that results cannot be retrieved.
        # put a counter here or something
        results = searcher.query(query_string, num_results=10)
        results_copy = results[:]

        print 'Retrieved %d result URLs in %f seconds' % (len(results), (time.time() - t))
        outdir = dir_root + '/' + query_string
        if not os.path.isdir(outdir):
            os.makedirs(outdir)
        html_fn = '{0}/{1}.html'.format(outdir, query_string)
        result_page_gen.gen_results_page(results_copy, 'BingAPISearch()',
                                         html_fn, show_in_browser=False)
        print 'Downloading images...'
        t = time.time()
        # example of downloading images from a query engine
        # a demo callback is also provided -
        #    if it is not required, the parameter can simply be removed
        output_fns = imgetter.process_urls(results, outdir, test_callback)
        print 'Downloaded %d results in %f seconds' % (len(output_fns), (time.time() - t))


if __name__ == "__main__":
    working_directory = sys.argv[1]
    if not(os.path.isdir(working_directory)):
        raise EnvironmentError("Directory entered is not a valid path")
    words_file = sys.argv[2]
    uniqueWords = set([])
    with open(words_file, 'r') as f:
        for line in f:
            word = line.rstrip('\n')
            print(word)
            uniqueWords.add(word)
    print(len(uniqueWords))
    # download_images(words_file, working_directory)
