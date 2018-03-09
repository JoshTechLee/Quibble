Please do not move any of the files around, as this is all set to make evaluation easy.

1. run the "reset" bash script to make every file empty
2. Run the OneDayRun on bash for the daily script
       - check in the "transactions" file to see all the changes made
3. Run the OneWeekRun on bash for the weekly script
       - again check in the "transactions" file to see all the changes
4. run the "reset" bash script again
5. Do whatever other tests to check the authenticity of the code on "Quibble"

NOTE:
In the "transactions" file there will be a set of weeks named "weekly01" to "weekly99" 
depending on how many weeks have been run.  Within one of the weekly files, there are 
"daily1" to "daily5" files depending on how many sessions have been run that week.  
Finally, inside each daily file, there are several text files holding the following information:
   "currentEvents.txt" holds the current events prior to run
   "newCE.txt" holds the current events after running
   "masterEvents.txt" holds the old master events
   "newME.txt" is the new produced master events file
   "dailyTransactions##.txt" holds the transactions for one session
   "mergedTransactions.txt" holds the summary of all daily transactions

"Quibble" holds the bash script to run the program
"QuibbleFE.py" is the Python script for the front end
"QuibbleBO.py" is the Python script for the back end
"DailyScripts" is the file containing the set of scripts to run one day
"WeeklyDayScripts" is the file that holds the set of scripts to run one week
"OneDayRun" is a bash script that runs a modified version of "Quibble" with the files in DailyScripts (modification reasoning mentioned later)
"OneWeekRun" is a bash script that runs Quibble for a one week duration
"WeeklySummary.txt" holds the summary of the set of scripts for one week
"DailySummary.txt" holds the summary of the set of scripts for one day
"ErrorFile" holds a significant error that prevented me from making scripts

There is one significant error that does not allow me to create automated scripts 
as I wanted to.  This was the biggest reason why I received a zero on my assignment 3 
(sorry for the late response on this one).  After looking into the "ErrorFile" and running 
"RunThis" once, you can see my "OneDayRun" and "OneWeekRun" scripts to see how I worked 
around the error.  If you run "Quibble" on its own, there is no problem.
