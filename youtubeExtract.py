# -*- coding: utf-8 -*-
import cv2
import os
import urllib
import argparse
import requests
from bs4 import BeautifulSoup
import youtube_dl
requests.packages.urllib3.disable_warnings()

def getYoutubeURL(keyword, number):

    # target search query page
    page = 1

    search_url = 'https://www.youtube.com/results?sp=EgIQAQ%253D%253D&search_query={}&page={}'
    search_soup = BeautifulSoup(requests.get(search_url.format(keyword, page), verify = False).text, 'html.parser')
    search_results = search_soup.find_all('div', {'class' : 'yt-lockup-content'})
    video_url_list = []
    for search_result in search_results[:number]:
        video_url = 'https://www.youtube.com' + search_result.h3.a['href']
        print(video_url + ' - '+ search_result.h3.a.text)
        video_url_list.append(video_url)

    return video_url_list

def youtubeDownload(urlList, vid_dir):
    try:
        os.stat(vid_dir)
    except:
        os.mkdir(vid_dir)

    os.chdir(vid_dir)

    '''
    # <urlList> example
    urlList = ['https://www.youtube.com/watch?v=no1YHRhFr5A','https://www.youtube.com/watch?v=pUjE9H8QlA4']
    '''

    # modify opts to customize output format
    opts = {
        # "http://www.youtube.com/watch?v=%(id)s.%(ext)s" but / not allowed in filename
        'outtmpl': '%(id)s.%(ext)s'
        }
    youtube_dl.YoutubeDL(opts).download(urlList)

    os.chdir("..")
    return 0

# extract frame from video
def FrameCapture(videoPath):
    

    # generate directory
    # pwd = os.getcwd()
    saveDir = videoPath.split('.mp4')[0]+"_frame"

    try:
        if not os.path.exists(saveDir):
            os.makedirs(saveDir)
    except OSError:
        print ('Error: Creating directory of '+saveDir)

    vid = cv2.VideoCapture(videoPath)
    #get frame of video
    fps = vid.get(cv2.CAP_PROP_FPS)
    count = 0
    next = True
    # capture frame until frame end
    while(next):
        next, image = vid.read()
        #  trim rate varies by fps of video
        if(int(vid.get(1)%int(fps)!=0)):
            continue
        print('Processing frame number : ' + str(int(vid.get(1))))
        # save current frame in jpg format
        cv2.imwrite("%s/%d.jpg" %(saveDir, count), image)
        count += 1
    
    # free resource
    vid.release()
    # cv2.destroyAllWindows()
    

## main
parser = argparse.ArgumentParser(description = 'Youtube Frame Extractor by Keyword')
parser.add_argument('keyword', nargs = '+')
parser.add_argument('-n', type = int, default = 10, help = 'number of search result. default: 10', metavar = 'number')
args = parser.parse_args()

'''
# args.keyword, args.n, args.p
keyword = 'test'
number = 10 # youtube shows 20 results per page
page = 1
'''
keyword, number = '+'.join(urllib.parse.quote_plus(str) for str in args.keyword), args.n

urlList = getYoutubeURL(keyword, number)
# os.mkdir("%(keyword)s_%(number)d") # attempt to vary output Dir on each query -> working...

# specify video save Dir
vid_dir = "videoDirectory"
# should be modified to download certain video quality -> working...
youtubeDownload(urlList, vid_dir)

# print(os.getcwd())

videoID_list = os.listdir(vid_dir)
print(videoID_list)
# FrameCapture("SampleVideo_720x480_2mb.mp4")
os.chdir(vid_dir)
for videoID in videoID_list:
    FrameCapture(videoID)