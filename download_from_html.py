from bs4 import BeautifulSoup
import urllib
import time
import sys
import os


def download_images(top_directory):
    all_words = os.listdir(top_directory)
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
            except IOError:
                continue
            time.sleep(0.2)
        print('Time taken to download all images in this folder: {}'.format(time.time() - t))


if __name__ == "__main__":

    PROCESSING_DIRECTORY = sys.argv[1]
    if not(os.path.isdir(PROCESSING_DIRECTORY)):
        raise EnvironmentError("Directory entered is not a valid path")
    download_images(PROCESSING_DIRECTORY)
