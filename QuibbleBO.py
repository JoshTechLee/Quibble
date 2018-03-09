#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      family
#
# Created:     23-11-2015
# Copyright:   (c) family 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from sys import stdin
import sys
import time
import os.path

# This is the BackOffice which runs at the end of the day, not the end of a
# session.  This BackOffice runs void of any dependency from the session
# activities.  The function creates a mergedTransactions.txt file which combines
# all the dailytransactions##.txt files into one.  A new master events file is
# created by utilizing the previous master events file and the merged
# transaction file.  From the master events file, a new current events file is
# created.
def BackOffice():
    #print 'Arguments:', str(sys.argv)
    # Arguments: oldmasterEvents, mergedtransaction, newMasterEvents, newCE

    mergedList = CreateMergedList(str(sys.argv[2]))
    masterList = UpdateMasterEvents(str(sys.argv[1]), mergedList)
    WriteMasterEventsFile(str(sys.argv[3]), masterList)
    WriteCurrentEventsFile(str(sys.argv[4]), masterList)


# Creates a merged transaction file from all the daily transaction files of
# ended sessions.
def CreateMergedList(fileName):
    mergedList = []
    with open(fileName) as mergedFile:
        for transaction in mergedFile:
            transaction = transaction.split()
            if transaction[0] == "00":
                break
            mergedList.append(transaction)
    return mergedList

# Update the master events file and stores it into an array using the merged
# events file (currently stored in an array called "mergedList")
def UpdateMasterEvents(fileName, mergedList):
    masterList = []
    with open(fileName) as masterFile:
        for event in masterFile:
            event = event.split()
            masterList.append(event)
    for event in mergedList:
        if event[0] == "03":
            for masterEvent in masterList:
                if masterEvent[2] == event[1]:
                    print "Error: Event \""+ event[1] + "\" already exists"
                    exit
            masterEvent = [event[2], event[3], event[1]]
            masterList.append(masterEvent)
        else:
            exists = False
            # search for the event for the index
            for index in range(len(masterList)):
                if masterList[index][2] == event[1]:
                    exists = True
                    break
            if exists == False:
                print "ERROR: Event \""+ event[0] + "\" doesn't exist"
                exit
            if event[0] == "01":
                if (int(masterList[index][1]) - int(event[3])) < 0:
                    print "ERROR: Number of tickets out of range:", masterList[index][1], "remaining"
                    print "Tickets Reset to 0"
                    masterList[index][1] = 0
                    continue
                masterList[index][1] = int(masterList[index][1]) - int(event[3])
            elif event[0] == "02":
                if (int(masterList[index][1]) + int(event[3])) > 99999:
                    print "ERROR: Number of tickets out of range:", masterList[index][1], "remaining"
                    print "Tickets Reset to 99999"
                    masterList[index][1] = 99999
                    continue
                masterList[index][1] = int(masterList[index][1]) + int(event[3])
            elif event[0] == "04":
                if (int(masterList[index][1]) + int(event[3])) > 99999:
                    print "ERROR: Number of tickets out of range:", masterList[index][1], "remaining"
                    print "Tickets Reset to 99999"
                    masterList[index][1] = 99999
                    continue
                masterList[index][1] = int(masterList[index][1]) + int(event[3])
            elif event[0] == "05":
                for masterEvent in masterList:
                    if masterEvent[2] == event[1]:
                        exists = True
                        masterList.remove(masterList[index])
                if exists == False:
                    print "Error: Event \""+ event[1] + "\" doesn't exist"
                    exit
    InsertionSort(masterList, 0)
    masterCopy = list(masterList)
    for event in masterCopy:
        if int(event[0]) < int(time.strftime("%y%m%d")):
            masterList.remove(event)
            print "Event:", event[2], "Removed"
    return masterList

# Write out master events file using the masterList, which contains the updated
# master events file
def WriteMasterEventsFile(fileName, masterList):
    masterFile = open(fileName, 'a')
    masterFile.truncate()
    for event in masterList:
        masterEvent = ("{0:0>6}".format(event[0]) + " " + "{0:0>5}".format(event[1]) + " " + event[2].ljust(20) + "\n")
        masterFile.write(masterEvent)
    masterFile.close()

# Write current events file from the updated master events file
def WriteCurrentEventsFile(fileName, masterList):
    currentFile = open(fileName, 'a')
    currentFile.truncate()
    for event in masterList:
        currentEvent = (event[2].ljust(20) + " " + "{0:0>5}".format(event[1]) + "\n")
        currentFile.write(currentEvent)
    currentFile.write("END".ljust(20) + " " + "00000")
    currentFile.close()

# This new modified insertion sort is used to sort an array based on an element
# of an array of arrays.
def InsertionSort(aList, part):
    for i in range(1, len(aList)):
        j = i
        while (j > 0) and (aList[j-1][part] > aList[j][part]):
            aList[j-1], aList[j] = aList[j], aList[j-1]
            j = j - 1

BackOffice()
