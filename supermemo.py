# Implementation of Supermemo 
# Algorithm SM-2
# Reference:
# http://www.supermemo.com/english/ol/sm2.htm
# 
# Cao Jin <xlscaoj@gmail.com>
# Thu Dec 26 21:53:52 CST 2013

from datetime import date, timedelta
import superfunc 
import pdb

# q should be 0-5:
# 5 - perfect response
# 4 - correct response after a hesitation
# 3 - correct response recalled with serious difficulty
# 2 - incorrect response; where the correct one seemed easy to recall
# 1 - incorrect response; the correct one remembered
# 0 - complete blackout.



today = date.today()

print "Supermemo!\nThis program is designed to help you to memeorize whatever you want to learn.\nPress 'h' for command help."

#datafile = raw_input('Please enter the filename of data: ')
datafile = 'words.txt'
card_list = superfunc.get_all_cards_from_file(datafile)

while True:

    command = raw_input('supermemo > ')

    if command == 'h':
        superfunc.show_help()

    elif command == 'n':
        # this operation should be placed before the program exit
        superfunc.save_card_list_to_file(datafile, card_list) 

        today = superfunc.goto_next_day()
        print 'Today is', today

        # this operation shoud be placed after program start
        card_list = superfunc.get_all_cards_from_file(datafile)

    elif command == 's':
        # show each card
        committed_list = []
        uncommitted_list = []
        for card in card_list:
            if card.committed_date == date.fromordinal(1):
                uncommitted_list.append(card)
            else:
                committed_list.append(card)
                
        while True:
            select_mode = raw_input('committed? uncommitted? all? [c/u/a] ')
            if select_mode == 'c':
                # print the number of committed cards
                superfunc.show_card_number(committed_list)
                
                # call show_cards() function to show each card one by one
                superfunc.show_cards(committed_list, today)
                break

            elif select_mode == 'u':
                superfunc.show_card_number(uncommitted_list)
                superfunc.show_cards(uncommitted_list, today)
                break

            elif select_mode == 'a':
                superfunc.show_card_number(card_list)
                superfunc.show_cards(card_list, today)
                break
            
            else:
                print "Please enter: 'c', 'u' or 'a'"
        

    elif command == 'd':
        print today

    elif command == 't':
        study_list = superfunc.test_card(card_list, today)
        superfunc.study_card(study_list)

    elif command == 'r':
        while True:
            confirm = raw_input('Do you want to reset all cards? [yes/no] ')
            if confirm in ('yes', 'ye', 'y'):
                for card in card_list:
                    superfunc.reset_card(card)
                else:
                    print "all cards have been reset!"
                break
            elif confirm in ('no', 'n', 'nop', 'nope'):
                break
            else:
                print "Please answer 'yes' or 'no'."
        
    elif command == 'i':
        superfunc.get_study_status(card_list)

    elif command == 'save':
        superfunc.save_card_list_to_file(datafile, card_list)
        

    elif command == '':
        pass

    elif command == 'q':
        
        print 'exiting program...'
        break    

    else:
        print "Ooops! A valid command, Please!. \n Press 'h' for help."

