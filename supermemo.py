#!/usr/bin/python

# Functions for supermemo 

import sys
sys.path.append('.')

from datetime import date, timedelta
import pdb
import sqlite3


class Card:
    """Card(repeat, interval, start)"""
    # question = ''
    # answer = ''
    # EF = 2.5 # 1.3 - 2.5
    # repeat = 0
    # interval = 0
    # commit = date.fromordinal(1)
    # start = date.fromordinal(1)
    # next = date.fromordinal(1)

    def __init__(self, *cardTuple):
        # print(cardTuple)
        initDate = date.fromordinal(1)

        self.question = cardTuple[0]
        self.answer = cardTuple[1]
        self.EF = 2.5 if cardTuple[2] == None else cardTuple[2]
        self.repeat = 0 if cardTuple[3] == None else cardTuple[3]
        self.interval = 0 if cardTuple[4] == None else cardTuple[4]
        self.initDate = initDate if cardTuple[5] == None \
            else date.fromordinal(cardTuple[5])
        self.startDate = initDate if cardTuple[6] == None \
            else date.fromordinal(cardTuple[6])
        self.nextDate = initDate if cardTuple[7] == None \
            else date.fromordinal(cardTuple[7])


    def get_interval(self, repeat, last_interval, EF):
        """calculate the interval days from start with respect to repeat, last_interval and EF"""
        if repeat == 1:
            interval = 1
        elif repeat == 2:
            interval = 6
        else:
            interval = last_interval * EF
            interval = int(round(interval))
        return interval
        

    def update(self, q):
        """update the date on which this card would appear"""
        self.repeat += 1

        newEF = self.EF+(0.1-(5-q)*(0.08+(5-q)*0.02))
        if newEF < 1.3:
            self.EF = 1.3
        elif newEF > 2.5:
            self.EF = 2.5
        else:
            self.EF = newEF

        self.interval = self.get_interval(self.repeat, self.interval, self.EF)
        self.nextDate = self.startDate + timedelta(days=self.interval)

    def add(self, today):
        self.initDate = today
        self.startDate= today
        self.nextDate = today + timedelta(1)

    def reset(self):
        self.EF = 2.5
        self.repeat = 0
        self.interval = 0
        self.initDate = date.fromordinal(1)
        self.startDate = date.fromordinal(1)
        self.nextDate = date.fromordinal(1)

    def restart(self, today):
        """reset the date of the card if q < 3"""
        self.startDate= today
        self.repeat = 0
        self.interval = 0

    def getcard(self):
        print 'question  ', self.question
        print 'answer    ', self.answer

        # if date.fromordinal(1) < self.init:
        #     print '[Initted]'
        # else:
        #     print '[Not Initted]'

        if self.initDate == date.fromordinal(1):
            print '[Not Initted]'
        else:
            print '[Initted]'
            
    def getcard_info(self):
        print 'question  ', self.question
        print 'answer    ', self.answer
        print 'EF        ', self.EF
        print 'repeat    ', self.repeat
        print 'interval  ', self.interval
        print 'init      ', self.initDate
        print 'start     ', self.startDate
        print 'next      ', self.nextDate


def importcards(csvfilename):
    '''import csv or txt file into sqlite db
    '''

    conn = sqlite3.connect('sm.db')
    c = conn.cursor()
    table = csvfilename[:-4]
    # create table named 'csvfilename'
   
    try:
        sqlcmd = ('CREATE TABLE {}('
                  'question TEXT, '
                  'answer TEXT, '
                  'ef REAL, '
                  'repeat INTEGER, '
                  'interval INTEGER, '
                  'init INTEGER, '
                  'start INTEGER, '
                  'next INTEGER)'.format(table))

        c.execute(sqlcmd)
    except sqlite3.OperationalError:
        # return "Table '{}' has existed already.".format(table)
        print(sys.exc_info()[0])
        return False

    # insert each line into table 'csvfilename'
    sqlcmd = 'INSERT INTO {}(question, answer) values (?,?)'.format(table)
    
    # read content of csvfilename into a list of tuple
    import csv
    with open(csvfilename, 'r') as csvfile:
        spamreader = csv.reader(csvfile)
        for card in spamreader:
            # print tuple(card)
            c.execute(sqlcmd, tuple(card))
    
    conn.commit()
    conn.close()

    return True

def readcards(table):
    '''read cards from table in sm.db
    '''

    conn = sqlite3.connect('sm.db')
    c = conn.cursor()
    # read db
    sqlcmd = 'SELECT * FROM {}'.format(table)
    c.execute(sqlcmd)
    cardsList = c.fetchall()

    conn.close()

    return cardsList

def removetable(table):
    '''remove table from sm.db

    return False if no such table, 
           Ture if the table is deleted
    '''

    conn = sqlite3.connect('sm.db')
    c = conn.cursor()
    sqlcmd = 'DROP TABLE {}'.format(table)

    try:
        c.execute(sqlcmd)
    except:
        return False

    conn.commit()
    conn.close()

    return True

def listables():
    '''list all tables in sm.db

    return a list of name of tables
    '''

    conn = sqlite3.connect('sm.db')
    c = conn.cursor()
    c.execute('SELECT name FROM sqlite_master')
    tables = c.fetchall()
    conn.close()

    return tables

def TupleList_to_CardList(TupleList):
    CardList = []
    for cardtuple in TupleList:
        CardList.append(Card(*cardtuple))
    
    return CardList

def CardList_to_TupleList(CardList):
    TupleList = []
    for Cardobj in CardList:
        TupleList.append((Cardobj.question,
                          Cardobj.answer,
                          Cardobj.EF,
                          Cardobj.repeat,
                          Cardobj.interval,
                          Cardobj.initDate.toordinal(),
                          Cardobj.startDate.toordinal(),
                          Cardobj.nextDate.toordinal()))

    return TupleList

def update_table(table, TupleList):
    '''update all card record in sm.db

    return True if no error, else False
    '''

    conn = sqlite3.connect('sm.db')
    c = conn.cursor()
    sqlcmd = ('UPDATE {} SET '
              'ef=?, '
              'repeat=?, '
              'interval=?, '
              'init=?, '
              'start=?, '
              'next=? '
              'WHERE question=?'.format(table))

    for card in TupleList:
        c.execute(sqlcmd, (card[2], 
                           card[3], 
                           card[4], 
                           card[5], 
                           card[6], 
                           card[7], 
                           card[0]))

    conn.commit()
    conn.close()

    return True
