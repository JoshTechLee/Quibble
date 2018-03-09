#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      family
#
# Created:     25-11-2015
# Copyright:   (c) family 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stdin
import sys
import time
import os.path

def CreateMergedFile():
    exists = True
    fileNumber = 0
    mergedList = []
    mergedFile = open('mergedTransactions.txt', 'a')
    mergedFile.truncate()

    while (exists == True):
        fileName = 'dailyTransactions' + "{0:0>2}".format(fileNumber) + '.txt'
        exists = os.path.isfile(fileName)
        fileNumber = fileNumber + 1
        if exists == True:
            with open(fileName) as f:
                for event in f:
                    if event == "00":
                        break
                    mergedFile.write(event)
                    mergedEvent = event.split()
                    mergedList.append(mergedEvent)
    mergedFile.write("00")
    mergedFile.close
    return mergedList

CreateMergedFile()