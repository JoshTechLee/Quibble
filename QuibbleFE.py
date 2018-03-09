#-------------------------------------------------------------------------------
# Name:        Quibble.ph
# Purpose:
#   Program to deal with transactions for, hopefully, some sort of music
#   festival.  The program has two ends: the front end and the back office.
#   When logging in the front end, the program either runs in an administrative
#   session or a sales session, which limits permissions depending on which
#   session is chosen.  Several actions can be taken after logging in and
#   all background events are covered by the back office.
#   The back office covers the records of all the events and transactions
#   that occur during all front end activities.  The back office is updated
#   every end of day (does not mean every logout).
#
#   SCROLL ALL THE WAY DOWN FOR RUNNING FRONT END OR BACK OFFICE!
#
# Author:      Joshua Lee and Nelson Yi
#
# Created:     13-11-2015
# Copyright:   (c) Joshua Lee and Nelson Yi 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# import for current date, standard input, and file checking respectively
from sys import stdin
import sys
import time
import os.path


# Deals with all the front end activities collectively.  It first asks you
# to login, the session, and options according to the session.  For every action
# within an option, if an error is reached, the function throws user back into
# "UserInterface()" for quick exit.
def FrontEnd():
    session = Login()
    if session == None:     # if session isn't chosen, exit program run
        return
    BackEndStartUp()        # prepare current events file and transaction file

    # Prompts user until available option is selected
    option = "Not Selected"
    while option != "Logout":
        # print menu for user
        print "Menu:"
        print "   Sell"
        print "   Return"
        if (session == "Admin"):
            print "   Create"
            print "   Add"
            print "   Delete"
        print "   Logout"
        # Restrict or allow options depending on session chosen.  Each option
        # chosen throws you into
        option = raw_input("Select from Menu:")
        if (session == "Sales"):
            if option == "Sell":
                Sell(session)
            elif option == "Return":
                Return(session)
            elif option == "Logout":
                Logout()
        elif (session == "Admin"):
            if option == "Sell":
                Sell(session)
            elif option == "Return":
                Return(session)
            elif option == "Create":
                Create()
            elif option == "Add":
                Add()
            elif option == "Delete":
                Delete()
            elif option == "Logout":
                Logout()
        # If input is invalid, input is thrown and error message is sent back
        elif option != "Sell" and option != "Return" and option != "Create":
            if option != "Add" and option != "Delete" and option != "Logout":
                print option
                print "ERROR: Invalid option:", option


# The Login function welcomes the user, asks for the user to 'Login' and then
# pick a session (Admin or Sales).
def Login():
    print "Welcome to Quibble!"
    status = raw_input("Please type 'Login':")
    if status != "Login":
        print "ERROR: Invalid input:", status
        return         # return to menu if not entering 'Login'
    else:
        print "-", status
        print "Sessions:"
        print "   Admin"
        print "   Sales"
        session = raw_input("Select a Session:")
        if session == "Admin" or session == "Sales":
            print "-", session
            return session      # returns session choice
        else:
            print "ERROR: Invalid input:", session
            return      # returns to menu if not entering valid choice


# The Sell function receives the session type as input and determines the
# limitations depending on the session.  The Sell function allows you to sell
# 'x' number of tickets depending on whether the event exists and the available
# tickets for the event.
def Sell(session):

    print "Event Name:"
    print "(Maximum of 20 characters)"
    eventName = raw_input("Name of event:") # Accept user input
    # if the user input is too long, the user is thrown back to main menu
    if len(eventName) > 20:
        print "ERROR: Input greater than 20 characters:", eventName
        return
    else:
        # find the event in the current events list array
        eventFound = False
        for index in range(len(eventList)):
            if eventList[index][0] == eventName:
                eventFound = True
                break
        # if not found, throw user back to menu
        if eventFound == False:
            print "ERROR: Event not found:", eventName
            return
    print "-", eventName

    # depending on session, ask user for tickets within a certain range
    if session == "Admin":
        message = "Number of Tickets:\n(Number of tickets between 0 and 99999)"
        prompt = "Number of tickets:"
        eventTickets = UserNumberInput(message, prompt)     # does exception catching for input
        if eventTickets == None:
            return
        eventTickets = int(eventTickets)
        # if the user inputs a number out of range, the user is thrown to menu
        if (eventTickets < 0) or (eventTickets > 99999):
            print "ERROR: Number of tickets out of range:", eventTickets
            return
    # same with "Admin" session, but with different restrictions
    else:
        message = "Number of Tickets:\n(Number of tickets between 0 and 8)"
        prompt = "Number of tickets:"
        eventTickets = UserNumberInput(message, prompt)
        eventTickets = int(eventTickets)
        if (eventTickets < 0) or (eventTickets > 8):
            print "ERROR: Number of tickets out of range:", eventTickets
            return
    if (eventList[index][1] - eventTickets) < 0:
        print "ERROR: Not enough tickets:", eventList[index][1], "remaining"
        return
    print "-", eventTickets

    # remove a certain number of tickets, depending on number of tickets sold
    eventList[index][1] = eventList[index][1] - eventTickets
    # change format and input into "transaction" array
    transaction.append("01 "+ eventName.ljust(20)+ " " + "{0:0>6}".format(eventList[index][2]) + " " + "{0:0>5}".format(eventTickets))
    # confirmation
    print "Tickets Sold!"


# The Return function allows the user to return 'x' amount of tickets depending
# on the session chosen.
def Return(session):

    print "Event Name:"
    print "(Maximum of 20 characters)"
    eventName = raw_input("Name of event:")
    if len(eventName) > 20:
        print "ERROR: Input greater than 20 characters:", eventName
        return
    else:
        eventFound = False
        for index in range(len(eventList)):
            if eventList[index][0] == eventName:
                eventFound = True
                break
        if eventFound == False:
            print "ERROR: Event not found:", eventName
            return
    print "-", eventName

    # depending on session, ask user for tickets within a certain range
    if session == "Admin":
        message = "Number of Tickets:\n(Number of tickets between 0 and 99999)"
        prompt = "Number of tickets:"
        eventTickets = UserNumberInput(message, prompt)     # does exception catching for input
        if eventTickets == None:
            return
        eventTickets = int(eventTickets)
        if (eventTickets < 0) or (eventTickets > 99999):
            print "ERROR: Number of tickets out of range:", eventTickets
            return
    # same with "Admin" session, but with different restrictions
    else:
        message = "Number of Tickets:\n(Number of tickets between 0 and 8)"
        prompt = "Number of tickets:"
        eventTickets = UserNumberInput(message, prompt)
        if eventTickets == None:
            return
        eventTickets = int(eventTickets)
        if (eventTickets < 0) or (eventTickets > 8):
            print "ERROR: Number of tickets out of range:", eventTickets
            return
    if (eventList[index][1] + eventTickets) > 99999:
        print "ERROR: Exceeding Ticket Limit:", eventList[index][1], "remaining"
        return
    print "-", eventTickets

    # The number of tickets is updated with the returned tickets
    eventList[index][1] = eventList[index][1] + eventTickets
    # The formatting is changed and recorded into the temporary transaction list
    transaction.append("02 "+ eventName.ljust(20)+ " " + "{0:0>6}".format(eventList[index][2]) + " " + "{0:0>5}".format(eventTickets))
    print "Tickets Returned!"


# When the admin wants to create a new event, this method is called.  Once the
# method is called, the user is prompted for an event name, a date, and the
# number of tickets available for sale for the event.
def Create():

    print "Event Name:"
    print "(Maximum of 20 characters)"
    eventName = raw_input("Name of event:")
    if len(eventName) > 20:
        print "ERROR: Input greater than 20 characters:", eventName
        return
    else:
        if eventName.strip() == "END":
            print "ERROR: Reserved code name: ", eventName
            return
        elif len(eventName.split()) == 2:
            print "ERROR: Delimiters not permitted: ", eventName
            return
        for event in eventList:
            if event[0] == eventName:
                print "Error: Event \""+ eventName + "\" already exists"
                return
    print "-", eventName

    # When asked for the date, the function receives the current date and
    # returns the date two years after the current date.  These two dates are
    # used as limits for the range of dates the user may enter.
    print "Event Date:"
    startDate = time.strftime("%y%m%d")
    endDate = str(int(startDate) + 20000)[-6:]
    message = "(Date between " + startDate + " and " + endDate + " (YYMMDD))"
    prompt = "Date of event:"
    eventDate = UserNumberInput(message, prompt)
    if eventDate == None:
        return
    elif (int(eventDate[:2]) < int(startDate[:2])) or (int(eventDate[:2]) > int(endDate[:2])):
        print "ERROR: Chosen year not in range:", eventDate
        return
    elif (int(eventDate[:2]) == int(endDate[:2])) and (int(eventDate[2:4]) > int(endDate[2:4])):
        print "ERROR: Chosen month not in range:", eventDate
        return
    if (int(eventDate[:2]) == int(endDate[:2])):
        if (int(eventDate[2:4]) >= int(endDate[2:4])) and int((eventDate[4:6]) > int(endDate[4:6])):
            print "ERROR: Chosen month not in range:", eventDate
            return
    elif (int(eventDate[2:4]) < 1) or (int(eventDate[2:4]) > 12):
        print "ERROR: Chosen month not valid:", eventDate
        return
    elif (int(eventDate[4:6]) < 1) or (int(eventDate[4:6]) > 31):
        print "ERROR: Chosen day not valid:", eventDate
        return
    print "-", eventDate

    # Asks for the number of tickets for the event to have
    message = "Number of Tickets:\n(Number of tickets between 0 and 99999)"
    prompt = "Number of tickets:"
    eventTickets = UserNumberInput(message, prompt)
    if eventTickets == None:
            return
    eventTickets = int(eventTickets)
    if (eventTickets < 0) or (eventTickets > 99999):
        print "ERROR: Number of tickets out of range:", eventTickets
        return
    print "-", eventTickets

    # The new event is saved within the current events list with the name,
    # number of tickets, and the date for the event respectively
    newEvent = [eventName, eventTickets, eventDate]
    # The formatting is changed for the transaction list
    transaction.append("03 "+ eventName.ljust(20)+ " " + "{0:0>6}".format(eventDate) + " " + "{0:0>5}".format(eventTickets))
    eventList.append(newEvent)
    print "Event Created!"


# The Add function allows the admin to increase the number of available tickets
# for an event, limited to 99999.
def Add():
    print "Event Name:"
    print "(Maximum of 20 characters)"
    eventName = raw_input("Name of event:")
    if len(eventName) > 20:
        print "ERROR: Input greater than 20 characters:", eventName
        return
    else:
        eventFound = False
        for index in range(len(eventList)):
            if eventList[index][0] == eventName:
                eventFound = True
                break
        if eventFound == False:
            print "ERROR: Event not found:", eventName
            return
    print "-", eventName

    message = "Number of Tickets:\n(Number of tickets between 0 and 99999)"
    prompt = "Number of tickets:"
    eventTickets = UserNumberInput(message, prompt)
    if eventTickets == None:
            return
    eventTickets = int(eventTickets)
    if (eventTickets < 0) or (eventTickets > 99999):
        print "ERROR: Number of tickets out of range:", eventTickets
        return
    if (eventList[index][1] + eventTickets) > 99999:
        print "ERROR: Exceeding Ticket Limit:", eventList[index][1], "remaining"
        return
    print "-", eventTickets

    eventList[index][1] = eventList[index][1] + eventTickets
    transaction.append("04 "+ eventName.ljust(20)+ " " + "{0:0>6}".format(eventList[index][2]) + " " + "{0:0>5}".format(eventTickets))
    print "Tickets Added!"


# For only the admin, the user may delete an existing event.  If the event does
# not exist, the user is thrown back into the menu
def Delete():
    print "Event Name:"
    print "(Maximum of 20 characters)"
    eventName = raw_input("Name of event:")
    if len(eventName) > 20:
        print "ERROR: Input greater than 20 characters:", eventName
        return
    else:
        eventFound = False
        print eventList[0][0]
        for index in range(len(eventList)):
            if eventList[index][0] == eventName:
                eventFound = True
                eventList.remove(eventList[index])
                break
    if eventFound == False:
        print "ERROR: Event not found:", eventName
        return

    print "-", eventName
    transaction.append("05 "+ eventName.ljust(20)+ " " + "000000" + " " + "00000")
    print "Event Deleted!"


# Once logged out, the user may not do any other action and the system is
# shutdown.  Before shutting down all the necessary back end work is done for
# that session.
def Logout():
    print "Goodbye!"
    BackEndShutdown()
    exit


# Whenever there is a number input for the user to enter, the UserNumberInput
# function checks what type of input the user put in and returns the value
# or not depending if it is valid.
def UserNumberInput(message, prompt):
    while True:
        try:
            print message
            number = raw_input(prompt)
            int(number)
            break
        except ValueError:
            print "ERROR: Not a number:", number
            return
    return number


# This is the back end work that occurs before any action is selected after
# logging in.  The BackEndStartUp function creates a global array "transaction"
# to keep a running temporary transaction file and an "eventList" array which
# deals with keeping all the current events.
def BackEndStartUp():
    global transaction
    global eventList
    transaction = []
    eventList = []
    with open('currentEvents.txt') as f:
        for line in f:
            event = line.split()
            if event[0] == "END":
                break
            event[1] = int(event[1])
            event.append("000000")
            eventList.append(event)


# Once a session ends and the user logs out, the BackEndShutDown runs.  This
# function creates a new "dailyTransactions##.txt" file.  The new transaction
# file makes sure to make a new daily transaction file and never to overwrite
# an existing file.
def BackEndShutdown():
    exists = True
    fileNumber = 0
    while (exists == True):
        fileName = 'dailyTransactions' + "{0:0>2}".format(fileNumber) + '.txt'
        exists = os.path.isfile(fileName)
        fileNumber = fileNumber + 1

    transactionFile = open(fileName, 'a')
    for line in transaction:
        transactionFile.write(line + '\n')
    transactionFile.write("00")
    transactionFile.close()

FrontEnd()
