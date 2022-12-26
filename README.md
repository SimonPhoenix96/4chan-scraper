# General (need python 3.8+ for argparse's extend action)

i use this to routinely (cronjob) collect the latest /wsg/ (https://boards.4channel.org/wsg/thread/4331591) bump file urls, which i then save in a git managed file that gets pushed to my github on file change (logic for that is handled in my cron file) using a personal access token so i dont need to manually push changes to the [bump links](https://github.com/SimonPhoenix96/random/tree/main/bump-links) database, users of my [bump-loader](https://github.com/SimonPhoenix96/mpv-userscripts/tree/master/bump-loader) can then use these urls to automatically get the latest /wsg/ and bumpworthy.com bumps for streaming instead of downloading these bumps locally which would take way too much space in the long run.

# 4chan-scraper
modifications made to graysonpikes to code:

- removed pillow (image processing lib) requirement and other image processing functions as i like to use curl/wget for that 
 
+ added python 3.8+ (argparse's extend action) do *python3 4chan-scraper.py -h || python3 4chan-scraper.py thread -h* for more info 
+ output scraped data as JSON
+ scrape Original Post contents incl. names, date, image file url etc. by passing a list of boards
+ scrape thread contents incl. replys, names, date, image file url etc. by passing thread urls





# Examples using JQ (https://stedolan.github.io/jq/) for parsing JSON output
    // only thread_subject, thread_url
    python3 4chan-scraper.py board --name wsg | jq '.[] | {thread_subject: .thread_subject, thread_url: .thread_url}'
    
    // get posts from thread
    /usr/bin/python3 4chan-scraper.py thread --url "https://boards.4chan.org/g/thread/85729998" | jq '.threads[0].thread_posts[]'
    
    // get post_message, file_name, file_url
    /usr/bin/python3 4chan-scraper.py thread --url "https://boards.4chan.org/g/thread/85729998" | jq '.threads[0].thread_posts[] | {post_message: .post_message , file_name : .file_name , file_url : .file_url }'

    // download all images of a thread using curl
    /usr/bin/python3 4chan-scraper.py thread --url "https://boards.4chan.org/g/thread/85729998" | jq '.threads[0].thread_posts[] | {file_url: .file_url} | join(",")'  | sed 's/\*\*/ -P /g' | xargs -n 3 -P 8 wget -P <output dir>
    
    // write to bash variable and then parse this bash variable later with jq  
    JSON_STRING=$(/usr/bin/python3 4chan-scraper.py thread --url "https://boards.4chan.org/g/thread/85729998" | jq -r '.[]') && jq -r '.' <<< "$JSON_STRING"


    
# Basic Usage
    
    pip3 install -r requirements.txt
    python3 4chan-scraper.py [-h] {board,thread} ...

POSITIONAL ARGUMENTS {board,thread}:

    board         the board[s] you want to get info about
    thread        the thread[s] you want to get files/replies from

SUBARGUMENTS board:
  
    --name [NAME ...], -n [NAME ...]
                        name the boards you want to get info about

e.g.

    python3 4chan-scraper.py board --name wsg tv v







SUBARGUMENTS thread:
  
    --url [URL ...], -u [URL ...]
                        thread urls you want to get data from
    --file [FILE ...], -f [FILE ...]
                        use this if you if you have threads stored in a json file like so: {"threads" : [{"url": <thread_url>}]}
                        
e.g.

    python3 4chan-scraper.py thread --file .\recent-bump-threads.json .\recent-bump-threads2.json --url https://yuki.la/wsg/2147319#p2169090 https://boards.4channel.org/wsg/thread/3768662
    
    
```json
{"threads": 
[
  {
   "thread_id": "2047443",
   "thread_board": "wsg",
   "thread_posts": 
   [
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
```



# 4chan-thread-collector
monitors and logs url status of threads, if dead it'll replace the url with a yuki.la archive one

# Usage 

    python3 4chan-thread-collector.py [thread_url]  [logged_threads_path json.file]

e.g.

    python3 4chan-thread-collector.py https://boards.4chan.org/wsg/thread/2358343  D:\4chan-thread-collector\bump-threads.json
