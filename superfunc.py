#!/usr/bin/python

# Functions for supermemo 

from datetime import date, timedelta
import pdb

class Card:
    """Card(repeat, interval, start_date)"""
    question = ''
    answer = ''
    EF = 2.5 # 1.3 - 2.5
    repeat = 0
    interval = 0
    committed_date = date.fromordinal(1)
    start_date = date.fromordinal(1)
    next_date = date.fromordinal(1)

    #def __init__(self, question, answer, EF, repeat, interval, committed_date, start_date, next_date):
        # self.repeat = repeat
        # self.interval = interval
        # self.start_date = start_date
    def __init__(self):
        pass

    def get_interval(self, repeat, last_interval, EF):
        """calculate the interval days from start_date with repect to repeat, last_interval and EF"""
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
        self.next_date = self.start_date + timedelta(days=self.interval)

    def restart(self, today):
        """reset the date of the card if q < 3"""
        self.start_date = today
        self.repeat = 0
        self.interval = 0

    def getcard(self):
        print 'question  ', self.question
        print 'answer    ', self.answer

        # if date.fromordinal(1) < self.committed_date:
        #     print '[Committed]'
        # else:
        #     print '[Not Committed]'

        if self.committed_date == date.fromordinal(1):
            print '[Not Committed]'
        else:
            print '[Committed]'
            

    def getcard_info(self):
        print 'question  ', self.question
        print 'answer    ', self.answer
        print 'EF        ', self.EF
        print 'repeat    ', self.repeat
        print 'interval  ', self.interval
        print 'committed ', self.committed_date
        print 'start_date', self.start_date
        print 'next_date ', self.next_date


def card_string_to_formated_card(card_string):
    #pdb.set_trace()
    card_elements = card_string.split('\t')
    card = Card() # Instance a Card object card
    card.question = card_elements[0].strip()
    card.answer = card_elements[1].strip()


    if len(card_elements) == 9:
        card.EF = float(card_elements[2])
        card.repeat = int(card_elements[3])
        card.interval = int(card_elements[4])
        card.committed_date = date.fromordinal(int(card_elements[5]))
        card.start_date = date.fromordinal(int(card_elements[6]))
        card.next_date = date.fromordinal(int(card_elements[7]))
    elif len(card_elements) == 2:
        pass
    else:
        print 'There are format errors in datafile!'

    return card

def formated_card_to_card_string(card):
    card_element_string = [card.question, card.answer, repr(card.EF), repr(card.repeat), repr(card.interval), repr(card.committed_date.toordinal()), repr(card.start_date.toordinal()), repr(card.next_date.toordinal())]
    card_element_string.append('\n')
    card_string = '\t'.join(card_element_string)
    return card_string


def get_all_cards_from_file(filename):
    print 'Read cards ...',

    f = open(filename, 'r')
    f.seek(0)

    allcards = [] # store all cards readed from data file into 'allcards' list
    while True:
        newcard = f.readline()
        if newcard == '':
            break
        else:
            allcards.append(newcard)
            
    f.close()
    
    allcards.sort()

    formated_card_list = [] # store all Card objects into a list
    for card_string in allcards:
        formated_card_list.append(card_string_to_formated_card(card_string))

    print 'Done.'

    return formated_card_list

def save_card_list_to_file(filename, card_list):
    print 'Save cards data ...',

    card_string_list = []
    for card in card_list:
        card_string_list.append(formated_card_to_card_string(card))
    
    f = open(filename, 'w')
    f.seek(0, 0)
    for card_string in card_string_list:
        f.write(card_string)

    f.close()
    print 'Done.'

def show_help():
    print """h  print command help
q  exit program
n  go to the next day
s  show all cards
t  test today's cards
d  show today's date
r  reset all cards
i  show info of study status"""


artifical_interval = 0
def goto_next_day():
    global artifical_interval
    artifical_interval = artifical_interval + 1
    today = date.today() + timedelta(days=artifical_interval)
    return today

def test_card(card_list, today):
    study_list = []
    for card in card_list:
        if date.fromordinal(1) < card.next_date <= today:
            card.getcard()
            quality = raw_input('choose a number 0-5 according to your performance: ')
            if quality.isdigit():
                quality = int(quality)
                if quality >= 3:
                    card.update(quality)
                elif quality < 3:
                    study_list.append(card)
                    card.restart(today)
                    card.update(quality)
            else:
                print 'exit ...'
                break
    else:
        print 'No cards to be tested, today'
    
    return study_list

def study_card(study_list):
    list_len = len(study_list)
    if list_len > 0:
        print '\nStudy the following cards!!'
    while list_len > 0:
        for card in study_list:
            print '(', list_len, 'cards left )'
            card.getcard()
            while True:

                result = raw_input('Right or Wrong? [r/w]: ')
                if result == 'r':
                    study_list.remove(card)
                    list_len -= 1
                    break
                elif result == 'w':
                    break
                else:
                    print "Please answer 'r' or 'w'"
    else:
        print 'No cards to be studied, today'

def commit_card(card, today):
    card.committed_date = today
    card.start_date = today
    card.next_date = today

def reset_card(card):
    card.EF = 2.5
    card.repeat = 0
    card.interval = 0
    card.committed_date = date.fromordinal(1)
    card.start_date = date.fromordinal(1)
    card.next_date = date.fromordinal(1)

def get_study_status(card_list):
    count_committed = 0
    for card in card_list:
        if card.committed_date != date.fromordinal(1):
            count_committed += 1
    
    print 'Committed', count_committed, ', Total', len(card_list)

def show_cards(card_list, today):
    index = 0
    len_list = len(card_list)
    while len_list > 0:
        #pdb.set_trace()
        index %= len_list
                
        card = card_list[index]
        print '------(', index + 1, ')-------'
        card.getcard()
        print '-----------------'

        # may be useless
        if repr(type(card.committed_date)) != "<type 'datetime.date'>":
            print 'committed date of this card may have error'

        # Input command for each card to commit or reset it.
        while True:
            subcommand = raw_input('use command:\ncommit|reset|exit|info|prev|next, press enter key to go to next card: ')

            if subcommand == 'commit':
                if card.committed_date == date.fromordinal(1):
                    commit_card(card, today)
                    print '[the card is committed]'
                else:
                    print 'This card has already been committed'

            elif subcommand == 'reset':
                if card.committed_date == date.fromordinal(1):
                    print 'This card has already been reset'
                else:
                    reset_card(card)

            elif subcommand == 'info':
                card.getcard_info()

            elif subcommand == 'prev':
                index -= 1
                break

            elif subcommand == 'next':
                index += 1
                break

            elif subcommand == 'exit':
                break

            elif subcommand == '':
                break

            else:
                print "Please enter 'commit' or 'reset' or 'exit' or 'info' or 'prev' or 'next'"

        if subcommand == 'exit':
            break

        # if subcommand == 'exit':
        #     break
    
    else:
        print 'No card'


def show_card_number(card_list):
    number = len(card_list)
    if number in [0, 1]:
        print number, 'card'
    else:
        print number, 'cards'
