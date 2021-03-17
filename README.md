# General

i use this to routinely (cronjob) collect the latest bump thread, which i then collect in a file and upload to my github, so that users of my webm-bump-loader can automatically get the latest bump thread url 

# 4chan-scraper
basically changed graysonpikes code to scrape only original post data in a board and return this as json

# Usage
4chan-scraper.py [boardA,boardB...] 

# 4chan-thread-collector
monitors and logs url status of threads, if dead it'll replace the url with a yuki.la archive one

# Usage 

4chan-thread-collector.py [thread_url]  [logged_threads_path json.file]
