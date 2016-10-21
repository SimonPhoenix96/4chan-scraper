# 4chan Image Scraper
An image scraper written in Python.

### Usage (Linux, OSX):

- Use python3
- Make sure to install dependencies (BeautifulSoup4):
  - `sudo pip3 install -r requirements.txt`
- For entire boards: `python3 scraper.py board <board letter> <output directory>`
  - eg. `python3 scraper.py board g output`
- For single threads: `python3 scraper.py thread <thread url> <output directory>`
  - eg. `python3 scraper.py thread http://boards.4chan.org/g/thread/49098915 output`
- Remember, the directory must exist to put files in it!

NOTE: If you experience an error installing Pillow with pip3, try installing the `libjpeg8-dev` package.

### Output Directory Formatting Examples:

- Relative Paths:
  - `output`
  - `output/`
- Absolute Paths:
  - `/Users/grayson/Pictures/4chan`
