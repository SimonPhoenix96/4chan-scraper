import sys
from bs4 import BeautifulSoup
from urllib.request import urlretrieve, urlopen
from urllib.parse import urlsplit
from re import sub, finditer


def get_board_threads(url):

    thread_ids = []

    # Get URLs of all active threads of a board
    html = urlopen(url).read().decode('utf-8')
    indicies = [x.start() for x in finditer('":{"date"', html)]
    for indice in indicies:
        thread_id = ""
        counter = 1
        while html[indice-counter] != '"':
            thread_id = html[indice-counter] + thread_id
            counter += 1
        thread_ids.append(thread_id)
    print(thread_ids)
    return thread_ids[1:]


def download_file(url, dest_dir, filename=None):
    # If no specific filename is provided, use the filename as
    # exists on the URL path
    if(filename is None):
        filename = urlsplit(url).path.split("/")[-1]
    urlretrieve(url, dest_dir + "/" + filename)


def get_file_urls(soup):
    file_urls = []

    for anchor in soup.find_all(attrs={'class': 'fileThumb'}):
        # Fix 4chan's href, which excludes the 'https://' protocol
        file_urls.append(sub("//", "http://", anchor.get('href')))

    return file_urls


def get_filenames(soup):
    filenames = []

    for anchor in soup.find_all(attrs={'class': 'fileText'}):
        filenames.append(anchor.get_text().split(" ")[1])

    return filenames


def main():

    print("4chan Image Scraper by Grayson Pike")

    if(sys.argv[1] == "thread"):
        # First argument is the thread URL
        url = sys.argv[2]
        # Second is the output directory
        # Output directory is via local (relative) path
        # ex. output
        # ex. output/
        # You can also do absolute paths (only tested with linux & mac)
        # ex. /Users/graysonpike/Desktop/4chan
        dest_dir = sys.argv[3]

        html = urlopen(url).read().decode('utf-8')
        # Beautiful soup allows for easy document navigation
        soup = BeautifulSoup(html, "html.parser")

        file_urls = get_file_urls(soup)
        filenames = get_filenames(soup)

        for i in range(len(file_urls)):
            download_file(file_urls[i], dest_dir, filenames[i])

    elif(sys.argv[1] == "board"):
        board = sys.argv[2]
        print("Checking board catalog @: " + "http://boards.4chan.org/" + board + "/catalog")
        board_url = "http://boards.4chan.org/" + board + "/catalog"
        thread_ids = get_board_threads(board_url)
        dest_dir = sys.argv[3]

        for thread in thread_ids:
            print("Downloading thread (id: " + thread + ") @: http://boards.4chan.org/" + board + "/thread/" + thread)
            url = "http://boards.4chan.org/" + board + "/thread/" + thread
            html = urlopen(url).read().decode('utf-8')
            # Beautiful soup allows for easy document navigation
            soup = BeautifulSoup(html, "html.parser")
            file_urls = get_file_urls(soup)
            filenames = get_filenames(soup)
            for i in range(len(file_urls)):
                download_file(file_urls[i], dest_dir, filenames[i])

    else:
        print("Usage: python3 scraper.py <'thread' or 'board'> <thread url> <dest directory>")
        print("See: https://github.com/Grayson112233/python-4chan-scraper")


main()
