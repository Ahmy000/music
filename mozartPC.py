#!/usr/bin/python

from lxml import etree

url = "https://www.allmusic.com/album/mozart-complete-piano-concertos-250th-anniversary-edition-mw0001865765"

#
def parseTrack(track):
  trackNum = track.xpath("td[@class='tracknum']")[0].text.strip()
  trackTitle = track.xpath("td[@class='title-composer']/div[@class='title']/a")[0].text.strip()
  trackTime = track.xpath("td[@class='time']")[0].text.strip()
  print(trackNum, trackTime, trackTitle)
#end

#
def parsePerformance(performance):
  performanceTitle = performance.xpath("tr[@class='performance-title']/td[2]/a")[0].text.strip()
  print(performanceTitle)

  tracks = performance.xpath("tr[@class='track']")
  for track in tracks:
    parseTrack(track)
#end

def pareseCD(cd):
  cdTitle = cd.xpath("div/h3")[0].text.strip(" \t\n\r")
  cdTitle = " ".join(cdTitle.split())
  print(cdTitle)

  performances = cd.xpath("table/tbody")
  for performance in performances:
    parsePerformance(performance)
#end

def parseAll(docs):
  listing = docs.xpath("//section[@class='track-listing']")[0]
  cds = listing.xpath("div[@class='disc']")
  for cd in cds:
    pareseCD(cd)
#end


if __name__ == "__main__":
  '''
  '''
  parser = etree.HTMLParser()
  tree = etree.parse("mozartPC.data", parser) 
  parseAll(tree)
