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
   this = True
   while this == True:
      what = raw_input()
      print what
      if what == "Stop":
          this = False
          exit
   exit
BackOffice()
