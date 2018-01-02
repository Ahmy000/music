#! /usr/bin/python
import fnmatch
import os, sys, re, json
from subprocess import call
import glob, os
from os import listdir
from os.path import isfile, isdir, join
import taglib

albumInfos = []
def findFiles(directory, pattern):
  for root, dirs, files in os.walk(directory):
    for baseName in files:
      if fnmatch.fnmatch(baseName, pattern):
        fileName = os.path.join(root, baseName)
        yield fileName


def searchDir():
    albums = [s for s in listdir('.') if isdir(s)]
    for album in albums: 
        cds = [d for d in listdir(album) if isdir(os.path.join(album, d))]
        for cd in cds:
            pieces = [p for p in listdir(os.path.join(album, cd)) if isfile(os.path.join(album, cd, p))]
            source = ''
            for piece in pieces:
                if piece.endswith('.flac') or piece.endswith('.ape'): 
                    source = os.path.join(album, cd, piece)
                    break

            alac = "{}_{}.m4a".format(album, cd)
            alac = '_'.join(re.split("[ ,:]", alac))
            if len(alac) == 0 or len(source) == 0:  continue
            cmd = "ffmpeg -i \'{}\' -c:a alac {}".format(source, alac)
            #print(os.getcwd());
            if os.path.exists(alac) == False:
                print(cmd)
                #os.system(cmd)
            if os.path.exists(alac) == True:
                catalog = getCatalog(alac)
                if catalog == None: continue
                match = re.search("([0-9]+)", cd); #print(cd)
                if match != None: catalogCD = catalog + "-" + match.group(1); #print(match.group(1))
                else: catalogCD = catalog
                info = searchAlbumInfo(catalog)
                if info == None: continue
                audio = taglib.File(alac)
                audio.tags["ALBUM"] = info['title']
                audio.tags["TITLE"] = u'{}-{}-[{}]'.format(info['title'], cd, catalogCD)
                print(audio.tags["TITLE"])
                #audio.tags["COMPOSER"] = ''
                audio.tags["CATALOGUE"] = info['catalogue']
                audio.tags["GENRE"] = "Classical"
                audio.save()

#end
def getCatalog(audio):
    m = re.search("\[(.*?)\]", audio)
    #print(m.group(1))
    return m.group(1)
            
def searchAlbumInfo(catalog):
    for info in albumInfos:
        if info['catalogue'] == catalog:
            #print(info)
            return info
    return None
#end

def loadInfos(info):
    with open(info) as data_file:    
        global albumInfos
        albumInfos = json.load(data_file)['albums']

if __name__ == '__main__' :
  '''
  '''
  loadInfos(sys.argv[1])
  searchDir()
  
