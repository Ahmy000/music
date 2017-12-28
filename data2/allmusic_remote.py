#!/usr/bin/python

import re, sys, json, requests
from lxml import etree
from collections import OrderedDict


base_url = "https://www.allmusic.com/album"
tail_url = "ajax_tracks"

def getDuration(str):
  ''' Get time from mm:ss '''
  times = re.split(":", str)
  time = 0
  for index, t in enumerate(reversed(times)):
    if index == 0:
      time = time + int(t)
    elif index == 1:
      time = time + int(t)*60
    elif index == 2:
      time = time + int(t)*3600
  return time
#end

def parseTrack(track):
  num = track.xpath("td[@class='tracknum']")[0].text.strip()
  title = track.xpath("td[@class='title-performer']/div[@class='title']/a")[0].text.strip(); #print(title)
  duration = track.xpath("td[@class='time']")[0].text.strip()
  return OrderedDict([("track", num),("title", title), ("durationR", duration), ("duration", getDuration(duration))])
#end


def parseCD(cd):
  title = cd.xpath("div/h3")[0].text.strip(" \t\n\r")
  title = " ".join(title.split()) ; #print(title) # spaces inside phase
  pInfos = []
  start = 0
  pTitle = ''
  trs = cd.xpath("table/tbody/tr")
  for tr in trs: # performance & movement are in the same level
    if tr.attrib["class"] == 'perfomance-title':
      if 'pInfo' in locals():
        #pInfo["movements"] = mInfos
        pInfo = OrderedDict([('title', pTitle), ('movements', mInfos)])
        pInfos.append(pInfo)
      pInfo = {}
      mInfos = []
      pInfo["title"] = tr.xpath("td/a")[0].text.strip(); #print(pInfo['title'])
      pTitle = tr.xpath("td/a")[0].text.strip(); print(pInfo['title'])
    elif tr.attrib["class"] == "track":
      trackInfo = parseTrack(tr)
      trackInfo["start"] = start
      start = start + trackInfo["duration"]
      if 'mInfos' in locals():
        mInfos.append(trackInfo)
  #end for
  #pInfo["movements"] = mInfos
  pInfo = OrderedDict([('title', pTitle), ('movements', mInfos)])
  pInfos.append(pInfo)
  return OrderedDict([("title", title), ("performances", pInfos)])
#end

def parseAll(docs):
  listing = docs.xpath("//section[@class='track-listing']")[0]
  album = {}
  cdsInfo = []
  cds = listing.xpath("div[@class='disc']")
  for cd in cds:
    cdInfo = parseCD(cd)
    cdsInfo.append(cdInfo)
  return OrderedDict([("title", "--"), ('composer','--'), ("label", "--"), ("performer", "--"), ("release", "--"), ("discs", cdsInfo)])
#end


def fetchDoc(uri):
  url = '/'.join([base_url, uri, tail_url])
  headers = {}
  headers['Accept-Language'] = 	'en-us'
  headers['Accept-Encoding'] = 'gzip, deflate' 
  headers['User-Agent'] = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8' # this is the key
  res = requests.get(url, headers=headers)
  #print(res.status_code)
  return res.text

def fetchAlbumInfo(album):
  doc = fetchDoc(album['uri'])
  doc = doc.replace("&amp;", "&")
  doc = doc.replace("&", "&amp;")
  tree = etree.fromstring(doc) 
  data = parseAll(tree)
  for index, disc in enumerate(data['discs']):
      disc["catalogue"] = album["catalogue"]
      match = re.search("([0-9]+)", disc["title"])
      if match is None:  outputJson = album['catalogue'] + ".json"
      else:  outputJson = album['catalogue'] + "-" + match.group(1) +  ".json"; disc['cd'] = match.group(1)
      with open(outputJson, 'w') as outfile:
          json.dump(disc, outfile, indent=4, sort_keys=False)
#end


if __name__ == "__main__":
  '''
  '''
  with open(sys.argv[1]) as data_file:    
    albums = json.load(data_file)
    for meta in albums['albums']:
      #print(meta)
      fetchAlbumInfo(meta)


