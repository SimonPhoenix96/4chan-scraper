import subprocess
import os
import json
import sys
import requests
from urllib.parse import urlparse

# process cmd line arguments containing thread url
thread_url = sys.argv[1]
threads_save_path = sys.argv[2]

def log_thread(urls, threads_save_path)-> dict():
    
    # read already logged threads from local json file 
    with open(threads_save_path) as f:
        data = json.load(f)
    
    for url in urls:
        # parse url 
        parsed_url = urlparse(url)
        # local function variables
        thread_exists_locally = False
        thread_id = parsed_url.path.split('/')[-1]
        thread_board = parsed_url.path.split('/')[1]
        thread_replaced = False



        # check if thread still up 
        html = requests.get(url).text 
        if (html.find("4chan - 404 Not Found") != -1 ):
            print("thread dead!")
            for thread in data['threads']:
                # compare url with logged ones, if dead replace link with yuki_archive_url
                if thread['url'] == url:
                    print("found thread in local threads.json, replace with yuki archive link")
                    yuki_archive_url = 'https://yuki.la/' + thread_board + '/' +  thread_id + '#' + thread_id    
                    thread['url'] = yuki_archive_url
                    thread_replaced = True
            if not thread_replaced:
                print("did not found thread in local threads.json, add to local threads.json")
                data['threads'].append({'url': url})

        else:
            print("thread alive!")
            for thread in data['threads']:
                if thread['url'] == url:
                    print("thread found in local threads.json, dont add to local thread.json")
                    thread_exists_locally = True
            if thread_exists_locally == False:
                print("thread not found in local threads.json, add to local thread.json")
                data['threads'].append({'url': url})

    return data


def main():

    # check if log file exists
    if not os.path.exists(threads_save_path):
        empty_data = {"threads": []}
        with open(threads_save_path, 'w') as json_file:
            json.dump(empty_data, json_file)

    # collect already logged alive threads 
    with open(threads_save_path) as f:
        data = json.load(f)
    collected_threads = []
    for thread in data['threads']:
        if thread['url'].find("yuki") == -1:
            collected_threads.append(thread['url'])

    # check if thread_url passed from terminal exists in collected_threads
    if not (thread_url in collected_threads):
        print("thread_url passed from terminal not in collected_threads, append to collected_threads")
        collected_threads.append(thread_url)
    else:
        print("thread_url passed from terminal already in collected_threads")

    # get changed log data 
    changed_data = dict()
    changed_data = log_thread(collected_threads, threads_save_path)
    print(json.dumps(changed_data, indent=1))
    # write changes to local file
    if data != changed_data:
        print("writing changes to local file")
        with open(threads_save_path, 'w') as json_file:
            json.dump(changed_data, json_file)
    else:
        print("no change!")
    
    # check for thread passed through command line
    # log_thread(scraped_thread_url, threads_save_path, thread_id, thread_board)


main()