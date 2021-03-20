# General

i use this to routinely (cronjob) collect the latest bump thread, which i then collect in a file and upload to my github, so that users of my webm-bump-loader can automatically get the latest bump thread url 

# 4chan-scraper
basically changed graysonpikes code to scrape only original post data in a board and return this as json
or scrape a thread and return all its info as json



# Usage

4chan-scraper.py [-h] {board,thread} ...

positional arguments:
  {board,thread}
    board         the board[s] you want to get info about
    thread        the thread[s] you want to get files/replies from

subarguments board:
  
  --name [NAME ...], -n [NAME ...]
                        name the boards you want to get info about

e.g.

4chan-scraper.py board --name wsg tv v

subarguments thread:
  
  --url [URL ...], -u [URL ...]
                        thread urls you want to get data from
  --file [FILE ...], -f [FILE ...]
                        use this if you if you have threads stored in a json file like so: {"threads" : [{"url": <thread_url>}]}
                        
e.g.

4chan-scraper.py thread --file .\recent-bump-threads.json .\recent-bump-threads2.json --url https://yuki.la/wsg/2147319#p2169090 https://boards.4channel.org/wsg/thread/3768662



# 4chan-thread-collector
monitors and logs url status of threads, if dead it'll replace the url with a yuki.la archive one

# Usage 

4chan-thread-collector.py [thread_url]  [logged_threads_path json.file]

e.g.

4chan-thread-collector.py https://boards.4chan.org/wsg/thread/2358343  D:\4chan-thread-collector\bump-threads.json
