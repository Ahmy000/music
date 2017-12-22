#! /usr/bin/python
import fnmatch
import os, re
from subprocess import call
import glob, os
from os import listdir
from os.path import isfile, isdir, join
import eyed3

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

            alac = "\'{}_{}.m4a\'".format(album, cd)
            alac = '_'.join(re.split("[ ,:]", alac))
            if len(alac) == 0 or len(source) == 0:  continue
            cmd = "ffmpeg -i \'{}\' -c:a alac {}".format(source, alac)
            #print(os.getcwd());
            print(cmd)
            os.system(cmd)
            #tag = eyed3.load(alac).tag
            #tag.album(album)
            #tag.save()

if __name__ == '__main__' :
  '''
  '''
  searchDir()
  
