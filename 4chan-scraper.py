import requests
import json
import sys
from bs4 import BeautifulSoup
from re import sub, finditer
import re
from urllib.parse import urlparse
import argparse
 

def get_board_threads(boards):

    for board in boards:
        try: 
            url = "http://4chan.org/" + board + "/catalog"
            html = requests.get(url).text 
            data = {}
            data['threads'] = []

            thread_start = [x.start() for x in finditer('":{"date"', html)]

            for indice in thread_start:
                thread_id = ""
                counter = 1
                while html[indice-counter] != '"':
                    thread_id = html[indice-counter] + thread_id
                    counter += 1
                data['threads'].append({'thread_board': board , 'thread_id': thread_id,  'thread_url': 'https://boards.4chan.org/' + board + '/thread/' + thread_id})

            for item in data['threads']:
                indicies = [x.start() for x in finditer(item['thread_id'], html)]
                # print(indicies)
                for indice in indicies:
                    thread_crawler = ""
                    counter = 1
                    while False != True:
                        # 
                        # 
                        thread_crawler = thread_crawler + html[(indice-2)+counter] 
                                    
                        counter += 1
                        # print(thread_crawler)
                        subject_start = thread_crawler.find(',"sub":"')
                        if subject_start != -1: 
                            # add index where sub html attribute starts to index where specific thread id starts
                            subject_start = subject_start + indice
                            break
                    # print("subject start index: " + str(subject_start) + " subject content index: " +  str(html[subject_start]) )
                    
                    thread_crawler = ""
                    counter = 1
                    while False != True:
                        # 
                        # 
                        thread_crawler = thread_crawler + html[(subject_start-2)+counter] 
                        # print(html[indice+counter])
                        counter += 1
                        # print(thread_crawler)
                        teaser_start = thread_crawler.find(',"teaser":"')
                        if teaser_start != -1: 
                            # add index where teaser html attribute starts to index where specific thread id starts
                            teaser_start = teaser_start + subject_start
                            break
                    subject_end = teaser_start-1        
                    # print("subject content: " + str(html[subject_start+6:subject_end]) )
                    # print("teaser start index: " + str(teaser_start) + " teaser content index: " +  str(html[teaser_start+9]) )
                    item.update({'thread_subject': html[subject_start+7:subject_end-1]})
                    thread_crawler = ""
                    counter = 1
                    while False != True:
                        
                        thread_crawler = thread_crawler + html[(subject_end-2)+counter] 
                        # print(html[indice+counter])
                        counter += 1
                        # print(thread_crawler)

                        # end of threads is noted by end of html thread array which looks like this in the html "}},
                        teaser_end = thread_crawler.find('"},') + thread_crawler.find('"}},')
                        if teaser_end != -2: 
                            # add index where teaser html attribute starts to index where specific thread id starts
                            teaser_end = teaser_end + subject_end
                            break
                    # print("teaser content: " + str(html[teaser_start+9:teaser_end]) )
                    item.update({'thread_teaser': html[teaser_start+10:teaser_end]})

                # print(item)
        except:
            print("An exception occurred with: " + str(boards))
            
    # Omit the first post, because it's always a
    # mod's sticky for the board
    return data['threads'][1:] 

def get_thread_posts(thread_html):
   
    posts = {}
    posts['reply'] = []
    op_post_parsed = False
    
    for post in thread_html:
        try:
            # # fileText html parsing 
            file_html =  post.find(attrs={'class': 'fileText'})
            file_url = ""
            file_name = ""

            if file_html != None:
                file_url = sub("//", "https://", file_html.find("a").get('href'))
                file_name = file_html.find("a").contents[0]
            
            
            # # postInfo html parsing
            if not op_post_parsed or post.find(attrs={'class': 'post op'}) != None:
                # # op html parsing
                post_html = post.find(attrs={'class': 'post op'})
                op_post_parsed = True
                post_type = "op"

            else: 
                # # reply html parsing
                post_html = post.find(attrs={'class': 'post reply'})
                post_type = "reply"

            post_user = " "
            post_user_id = " "
            post_date = " "
            post_number = " "
            post_message = " "
        
            # # get postinfo
            if post_html != None:


                # Extract Post Info
                post_info =  post_html.find(attrs={'class': 'postInfo desktop'})
                # print(post_info.find(attrs={'class': 'name'}))
                post_number =  post_info.find('input').get('name') or "none"
                post_date =  post_info.find(attrs={'class': 'dateTime'}).contents[0] or "none"
                
                # this handles users with trips
                temp_post_info = post_info.find(attrs={'class': 'name'}).contents
                if len(temp_post_info) != 0:
                    post_user = post_info.find(attrs={'class': 'name'}).contents[0]
                else:
                    post_user = post_info.find(attrs={'class': 'postertrip'}).contents[0]
                
                # some boards dont have user ids, this handles em
                temp_post_user_id = post_info.find(attrs={'class': 'hand'})
                if temp_post_user_id == None:
                    post_user_id =  "none"
                else:
                    post_user_id =  post_info.find(attrs={'class': 'hand'}).contents[0]
                
                # Extract Post Message
                temp_post_message = post_html.find(attrs={'class': 'postMessage'}) or "none"
                len_post_message = len(temp_post_message)
                # if len_post_message == 0:
                #     # no message
                #     post_message = " "
                # else:
                    # message
                for line in temp_post_message.contents:
                    # print(line)
                    quotelink = re.search('">(.*)</a>', str(line))
                    # print(quotelink)

                    if quotelink != None:
                        line = quotelink.group(1).replace("&gt;&gt;", ">>") + "\n"
                    
                    post_message = post_message + ''.join(str(line)).replace("\u2019", "'").replace('<span class="quote">&gt;', ">").replace('<br/>', "\n").replace('</span>', "")

            posts['reply'].append({ "post_type" : post_type,
                                    "post_user": post_user,
                                    "post_user_id": post_user_id,
                                    "post_date": post_date,
                                    "post_number": post_number,
                                    "post_message": post_message,
                                    "file_url" : file_url,
                                    "file_name": file_name,})
        except:
            print("An exception occurred with: " + str(post))

    return posts['reply']

def get_thread(threads_urls):
    threads = {}
    threads['threads'] = []
    for thread in threads_urls:
        try:
            # parse url 
            parsed_url = urlparse(thread['url'])
            #local function variables
            thread_id = parsed_url.path.split('/')[-1]
            thread_board = parsed_url.path.split('/')[1]
            # web request
            html = requests.get(thread['url']).text
            soup = BeautifulSoup(html, 'html.parser') 
            thread_html = soup.find_all(attrs={'class': 'thread'})[0] 
            threads['threads'].append({"thread_id" : thread_id, "thread_board" : thread_board, "thread_posts" : get_thread_posts(thread_html)})
        except:
            print('{"Exception" : "An exception occurred with: ' + str(thread['url']) + '"}' )
    return threads

def main():

    parser = argparse.ArgumentParser()

    subparsers = parser.add_subparsers(dest='command')

    board = subparsers.add_parser('board', help='the board[s] you want to get info about')
    board.add_argument('--name', '-n', help='name the boards you want to get info about', action='extend', nargs='*')

    thread = subparsers.add_parser('thread', help='the thread[s] you want to get files/replies from')
    thread.add_argument('--url','-u', help='thread urls you want to get data from', action='extend',  nargs='*')
    thread.add_argument('--file', '-f', help='use this if you if you have threads stored in a json file like so: {"threads" : [{"url": <thread_url>}]}', action='extend',  nargs='*')

    args = parser.parse_args()
    
    if args.command == 'board':
        if args.name:
            print(json.dumps(get_board_threads(args.name), indent=1))
    
    
    elif args.command == 'thread':
        # json list represantion of urls
        json_urls = []
        
        if args.url:
            for url in args.url:
                json_urls.append({'url': url})  
        # adding urls from file to json file
        if args.file:
            count = 0
            # if count > 0 merge multiple files together, else get values from sole file
            for file in args.file:
                

                with open(file) as f:
                    temp_json = json.load(f)
                for url in temp_json['threads']:
                    json_urls.append(url)

            # print(json_urls)

        print(json.dumps(get_thread(json_urls), indent=1))

main()
