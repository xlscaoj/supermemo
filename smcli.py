# Implementation of Supermemo 
# Algorithm SM-2
# Reference:
# http://www.supermemo.com/english/ol/sm2.htm
# 
# Cao Jin <xlscaoj@gmail.com>
# Thu Dec 26 21:53:52 CST 2013

import sys
sys.path.append('.')

from datetime import date, timedelta
import supermemo 
import pdb
import sqlite3

# q should be 0-5:
# 5 - perfect response
# 4 - correct response after a hesitation
# 3 - correct response recalled with serious difficulty
# 2 - incorrect response; where the correct one seemed easy to recall
# 1 - incorrect response; the correct one remembered
# 0 - complete blackout.

days = 0 # set number of days after today()
today = date.today() + timedelta(days)

print '''Supermemo!
This program is designed to help you to memeorize whatever you want to learn.
Press 'h' for command help.'''


# command line interface. Database Mode
def database_mode():
    while True:

        command = raw_input('supermemo > ')

        if command == 'h':
            database_mode_help()

        elif command == 's':
            while True:
                try:
                    table = raw_input('name of the table? ')
                    if table != '':
                        table_mode(table)
                    break
                except sqlite3.OperationalError:
                    print(sys.exc_info()[1])

        elif command == 'l':
            tables = supermemo.listables()
            print("===== card table =====")
            for name in tables:
                print(name[0])

            print('======================')

        elif command == 'd':
            tablename = raw_input('name of the table? ')
            if tablename != '':
                if supermemo.removetable(tablename):
                    print('card table {} is deleted'.format(tablename))
                else:
                    print('card table {} can not be deleted'.format(tablename))

        elif command == 'i':
            csvname = raw_input('csv file? ')
            if csvname != '':
                if supermemo.importcards(csvname):
                    print('import cards, Done')
                else:
                    print('Ooops... can not import {}'.format(csvname))

        elif command == '':
            pass

        elif command == 'q':

            print 'exiting program...'
            break    

        else:
            print "Ooops! A valid command, Please!. \n Press 'h' for help."

def database_mode_help():
    print """
    h  print command help
    s  select a card table
    l  list all tables
    q  exit program
    d  delete card table
    i  import csv file into SQLite3 database
    """

def table_mode(table):    
    # change cardTupleList to CardList of Card Objects
    cardTupleList = supermemo.readcards(table) 
    CardList = supermemo.TupleList_to_CardList(cardTupleList)
    studyListindex = []
    studiedListindex = []
    testListindex = []
    testedListindex = []

    refresh_studyList(CardList, studyListindex, studiedListindex, \
                          testListindex, testedListindex, today)
    # command line interface, table mode 
    while True:

        #display study info
        print('Today is {}\n'
              'study {}\n'
              'test  {}\n'.format(today, len(studyListindex), len(testListindex)))

        command = raw_input('sm(table) > ')

        if command == 'h':
            table_mode_help()

        # show all card
        elif command == 'b':
            browse_mode(CardList, today)
            refresh_studyList(CardList, studyListindex, studiedListindex, \
                                  testListindex, testedListindex, today)

        # test mode
        elif command == 't':
            test_mode(CardList, testListindex, testedListindex)
            refresh_studyList(CardList, studyListindex, studiedListindex, \
                                  testListindex, testedListindex, today)

        # study mode
        elif command == 's':
            study_mode(CardList, studyListindex, studiedListindex)

        elif command == 'l':
            print 'studyListindex', studyListindex

        elif command == 'q':
            print 'exiting table mode...'
            newcardTupleList = supermemo.CardList_to_TupleList(CardList)
            supermemo.update_table(table, newcardTupleList)
            break

        elif command == '':
            pass

        else:
            print "Ooops! A valid command, Please!. \n Press 'h' for help."

 
def table_mode_help():
    print("""
    h  print command help
    q  exit program
    t  test mode
    s  study mode
    b  browse all cards in this table
    """)

def browse_mode(CardList, today):
    index = 0
    len_list = len(CardList)
    while len_list > 0:
        #pdb.set_trace()
        index %= len_list
                
        card = CardList[index]
        print '------(', index + 1, ')-------'
        card.getcard()
        print '-----------------'

        # Input command for each card to init or reset it.
        while True:
            subcommand = raw_input(\
                '(a)dd|(r)eset|(e)xit|(i)nfo, "enter key" to go next: ')

            if subcommand == 'a':
                if card.initDate == date.fromordinal(1):
                    card.add(today)
                    print 'This card is added'
                else:
                    print 'This card has already been added'

            elif subcommand == 'r':
                if card.initDate == date.fromordinal(1):
                    print 'This card has already been reset'
                else:
                    card.reset()
                    print 'This card is reseted'

            elif subcommand == 'i':
                card.getcard_info()

            elif subcommand == 'p':
                index -= 1
                break

            elif subcommand == 'e':
                break

            elif subcommand == '':
                index += 1
                break

            else:
                print("Oops... ")

        if subcommand == 'e':
            break

    # else:
    #     print 'No card'


def refresh_studyList(CardList, studyListindex, studiedListindex, \
                          testListindex, testedListindex, today):
    newstudyListindex = []
    newtestListindex = []

    for index, cardobj in enumerate(CardList):
        # if date.fromordinal(1) < cardobj.nextDate <= today:
        if cardobj.startDate == today or cardobj.EF < 2.5:
            newstudyListindex.append(index)

        if cardobj.startDate < cardobj.nextDate <= today:
            newtestListindex.append(index)

    for index in newstudyListindex:
        if index not in studiedListindex and index not in studyListindex:
            studyListindex.append(index)

    for index in newtestListindex:
        if index not in testedListindex:
            testListindex.append(index)


def study_mode(CardList, studyListindex, studiedListindex):
    length_index = len(studyListindex)
    while length_index > 0:
        for index in studyListindex:
            print '(', length_index, 'cards left )'
            CardList[index].getcard()

            while True:
                command = raw_input('Right or Wrong? [r/w]: ')
                if command == 'r':
                    length_index -= 1
                    studyListindex.remove(index)
                    studiedListindex.append(index)
                    #CardList[index].nextDate += timedelta(1)
                    break
                elif command == 'w':
                    break
                elif command == 'q':
                    return
                else:
                    print "Please answer 'r' or 'w'; 'q' for quit"
    else:
        print 'No card'

def test_mode(CardList, testListindex, testedListindex):
    
    # for index, card in enumerate(CardList):
    for index in testListindex[:]:
        # key part, deciding which card should be tested 
        #if date.fromordinal(1) < card.nextDate <= today:
        # if card.startDate < card.nextDate <= today:
        #     card.getcard()
        CardList[index].getcard()
        while True:
            try:
                quality = int(raw_input(
                        'score your memory, 0(worst)-5(best): '))
                CardList[index].update(quality)

                # if quality >= 3:
                #     # card.update(quality)
                #     CardList[index].update(quality)
                # elif quality < 3:
                #     # studyListindex.append(index)
                #     # card.restart(today)
                #     # card.update(quality)
                #     CardList[index].restart(today)
                #     # CardList[index].update(quality)
                break

            except ValueError:
                print "Oops! That was no valid number. Try again..."
        testListindex.remove(index)
        testedListindex.append(index)
        #pdb.set_trace()
    else:
        print 'No cards to be tested, today'

    # return studyListindex


if __name__ == "__main__" : 
    database_mode() 

