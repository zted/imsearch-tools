"""
Downloads images from html files, use after download_htmls.py
Usage: python download_from_htmls.py directory/containing/query/results
"""

import os
import socket
import sys
import time
import urllib
from bs4 import BeautifulSoup


def download_images(top_directory):
    """
        Goes into every folder, looks for the .html file, and downloads images from each of the link in the file
        into the same folder.
        WARNING!!! Does not take into account robots.txt file, best if you check it with the site manually.
        Args:
            top_directory: directory that contains folders which contains htmls, generated
            from download_from_html
        Returns: None
        """
    all_words = os.listdir(top_directory)
    all_words.sort()
    for word in all_words:
        print('Downloading images for "{}"'.format(word))
        t = time.time()
        download_folder = '{}/{}'.format(top_directory, word)
        htmlfile = '{}/{}.html'.format(download_folder, word)
        f = open(htmlfile, 'r')
        data = f.read()
        f.close()
        soup = BeautifulSoup(data)
        img_links = soup.findAll(attrs={"class":"result"})
        for n, img_link in enumerate(img_links):
            address = img_link.img['src']
            filepath = '{}/{}.jpg'.format(download_folder, n)
            try:
                urllib.urlretrieve(address, filepath)
            except (IOError, UnicodeError):
                # Websites sometimes download slow, get stuck, just continue on.
                continue
            time.sleep(0.5)
        print('Time taken to download all images in this folder: {}'.format(time.time() - t))
    return


if __name__ == "__main__":
    socket.setdefaulttimeout(5)
    PROCESSING_DIRECTORY = sys.argv[1]
    if not(os.path.isdir(PROCESSING_DIRECTORY)):
        raise EnvironmentError("Directory entered is not a valid path")
    download_images(PROCESSING_DIRECTORY)
