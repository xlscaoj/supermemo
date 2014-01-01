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
        card_list_backup = card_list[:]
        while len(card_list_backup) > 0:
            for card in card_list_backup:
                print '-----------------'
                card.getcard()
                print '-----------------'

                # may be useless
                if repr(type(card.committed_date)) != "<type 'datetime.date'>":
                    print 'committed date of this card may have error'
                
                # Input command for each card to commit or reset it.
                while True:
                    subcommand = raw_input('use command:\ncommit|reset|exit|info, press enter key to go to next card: ')

                    if subcommand == 'commit':
                        if card.committed_date == date.fromordinal(1):
                            superfunc.commit_card(card, today)
                        else:
                            print 'This card has already been committed'

                    elif subcommand == 'reset':
                        if card.committed_date == date.fromordinal(1):
                            print 'This card has already been reset'
                        else:
                            superfunc.reset_card(card)

                    elif subcommand == 'info':
                        card.getcard_info()

                    elif subcommand == 'exit':
                        break

                    elif subcommand == '':
                        break

                    else:
                        print "Please enter 'next' or 'info' or 'commit'"

                if subcommand == 'exit':
                    break

            if subcommand == 'exit':
                break

    elif command == 'd':
        print today

    elif command == 't':
        study_list = superfunc.test_card(card_list, today)
        superfunc.study_card(study_list)

    elif command == 'r':
        while True:
            confirm = raw_input('Do you want to reset all cards? [yes/no] ')
            if confirm == 'yes' or confirm == 'y':
                for card in card_list:
                    superfunc.reset_card(card)
                break
            elif confirm == 'no' or confirm == 'n':
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

