import sys
from bs4 import BeautifulSoup
from urllib.request import urlretrieve, urlopen
from urllib.parse import urlsplit
from re import sub


def download_file(url, dest_dir, filename=None):
    if(filename == None):
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

    if(len(sys.argv) != 3):
        print("Usage: python3 scraper.py <url> <dest directory>")

    else:
        # First argument is the thread URL
        url = sys.argv[1]
        # Second is the output directory
        # Output directory is via local (relative) path
        # ex. output
        # ex. output/
        # You can also do absolute paths (only tested with linux & mac)
        # ex. /Users/graysonpike/Desktop/4chan
        dest_dir = sys.argv[2]

        html = urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        file_urls = get_file_urls(soup)
        filenames = get_filenames(soup)

        for i in range(len(file_urls)):
            download_file(file_urls[i], dest_dir, filenames[i])

main()
