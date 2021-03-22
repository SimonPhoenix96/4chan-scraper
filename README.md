# General (need python 3.8+ for argparse's extend action, if you want to use an older python version change this yourself)

i use this to routinely (cronjob) collect the latest bump thread, which i then collect in a file and upload to my github, so that users of my [webm-bump-loader](https://github.com/SimonPhoenix96/mpv-userscripts/tree/master/webm-bump-loader) can automatically get the latest bump thread url 

# 4chan-scraper
basically changed graysonpikes code to scrape only original post data in a board and return this as json
or scrape a thread and return all its info as json

# Usage

4chan-scraper.py [-h] {board,thread} ...

positional arguments {board,thread}:

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

{"threads": [
  {
   "thread_id": "2047443",
   "thread_board": "wsg",
   "thread_posts": [
    {
     "post_type": "op",
     "post_user": "Anonymous",
     "post_user_id": "none",
     "post_date": "01/04/18(Thu)19:21:12",
     "post_number": "2047443",
     "post_message": " Come share an [experience] with us",
     "file_url": "https://ii.yuki.la/d/65/8cd320aaab678b70f9d8dbf1c239af2784d192846797f2da3cb54fd5710b665d.webm",
     "file_name": "[space makes me feel lone(...).webm"
    },
    {
     "post_type": "reply",
     "post_user": "Anonymous",
     "post_user_id": "none",
     "post_date": "01/04/18(Thu)19:21:49",
     "post_number": "2047446",
     "post_message": " >>2047443\n",
     "file_url": "https://ii.yuki.la/0/49/b3c8b854226d0edd288ef752e84e93fc85c7632a0f8473b2b9bb2bb30057f490.webm",
     "file_name": "[sweater weather by no se(...).webm"
    }]}


# 4chan-thread-collector
monitors and logs url status of threads, if dead it'll replace the url with a yuki.la archive one

# Usage 

4chan-thread-collector.py [thread_url]  [logged_threads_path json.file]

e.g.

4chan-thread-collector.py https://boards.4chan.org/wsg/thread/2358343  D:\4chan-thread-collector\bump-threads.json
