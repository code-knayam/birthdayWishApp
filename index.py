import sys
from urllib import urlencode
import calendar
from urlparse import urlparse, parse_qs
from random import choice
from datetime import datetime, date
import facebook
import requests

print("\n")
access_token = raw_input("Enter secret access token.\nDont have?  Get from https://developers.facebook.com/tools/explorer/ \n")
print("\n")

message_list = ["Thanks alot!!! :)", "Thank you :)", "Thanks :)" ]

print("Mention the date from which you want to reply to posts")
year = int(raw_input("Enter  year\n"))
month = int(raw_input("Enter Month\n"))
day = int(raw_input("Enter Day\n"))

bday = datetime(year, month, day, 0, 0, 0)

epoch=datetime(1970,1,1)
td = bday - epoch
utc_bday = int((td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 1e6)

#proxy settings
http_proxy = ""
http_proxy = ""
ftp_proxy = ""

proxy_dict = {
    "http" : http_proxy,
    "https" : http_proxy,
    "ftp" : ftp_proxy
}

def getData(post_id, field) :
    # creating and sending request to get the from and message field for individual post
    base_url = 'https://graph.facebook.com/v2.10/%s' % (post_id)
    

    params = {'access_token': access_token, 'fields': field }
    url = '%s?%s' % (base_url, urlencode(params))
    req = requests.get(url, proxies=proxy_dict)

    if req.status_code == 200:
        content = req.json()              
        if field in content:
            return content[field]
        else :
            return ''
    else :
        print("Couldnt get info.")
        return ""

def getChoice():
    while True:
        userInput = raw_input("Reply to it ? Y or N \n") 
        if userInput not in [ 'y', 'Y', 'n', 'N' ] :
            print("Enter a valid choice")
            continue
        elif userInput in [ 'y', 'Y'] :
            return True
        else:
            return False

def sendReply(post_id, reply) :
    url = 'https://graph.facebook.com/%s/likes/total_count?access_token=%s' % (post_id, access_token)
    requests.post(url, data={}, proxies=proxy_dict)    
    
    url = 'https://graph.facebook.com/%s/comments?access_token=%s' % (post_id, access_token)
    requests.post(url, data={'message': reply}, proxies=proxy_dict)    



# creating and sending request to get all posts
base_url = 'https://graph.facebook.com/v2.10/me/feed'
params = {'since': utc_bday, 'access_token': access_token}
url = '%s?%s' % (base_url, urlencode(params))

req = requests.get(url, proxies=proxy_dict)



if req.status_code == 200 :

    content = req.json()
    posts = content['data']

    print("\n\n")
    print("number of posts found %s" % ( len(posts) ))
    print("Get ready to thank them")
    print("\n\n")
    
    userInput = raw_input("Enter 1 - to thank all at once. 2 - Thank one by one\n")

    if userInput == '1' :
        # thank all at once
        for post in posts :
            post_id = post['id']
            reply = choice(message_list)
            sendReply(post_id,reply)

        print("Replied to all the posts !")
    else :
        # thank one by one
        # main loop going through all the posts
        for post in posts:  
            
            print("\n\n")
            print("_________________________")        
            print("\n\n")

            post_id = post['id']
            if 'message' not in post:
                post["message"] = getData(post_id, 'message')
            if 'story' not in post:
                post["story"] = getData(post_id, 'story')    
            post["from"] = getData(post_id, 'from')
            post["type"] = getData(post_id, 'type')            
            
            message =  "Message from %s \nStory : %s \nSays : %s\nType : %s" % (post["from"]["name"] ,post["story"], post["message"], post["type"] )
            print(message)

            user_choice = getChoice()        

            if user_choice :
                print("Replying\n")
                reply = choice(message_list)
                sendReply(post_id, reply)
                print("Commented : %s \n" % (reply) )
            else :
                print("Ignoring this one.")
                        
else :
    print("Some error occured")


