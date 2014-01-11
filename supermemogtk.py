# Implement gui of supermemo using pygtk

import pygtk
pygtk.require('2.0')
import gtk
import pdb
from datetime import date, timedelta
import superfunc 


class Mainboard:
    def destroy(self, widget, data=None):
        gtk.main_quit()

    def show_committed_card(self, widget, command):
        len_card_list = len(self.committed_list)
        if command == 'prev':
            self.index -= 1
            self.index %= len_card_list
            card = self.committed_list[self.index]
            card_string = 'Question:\n' + card.question + '\n====\n' + 'Answer:\n' + card.answer
        elif command == 'next':
            self.index += 1
            self.index %= len_card_list
            card = self.committed_list[self.index]
            card_string = 'Question:\n' + card.question + '\n====\n' + 'Answer:\n' + card.answer
        else:
            print 'show_committed_card argument error'
            
        self.textbuffer.set_text(card_string)
        
        self.textview.show()
        
        self.scrolled_window.show()


    def quit_test(self, widget, data=None):
        self.window.remove(self.test_box)
        self.window.add(self.mainbox)

    def quit_study(self, widget, data=None):
        self.window.remove(self.study_box)
        self.window.add(self.mainbox)


    def test(self, widget, data=None):
        self.test_box = gtk.VBox(False, 0)
        
        label = gtk.Label('card')
        label.set_alignment(0, 0)
        label.show()
        self.test_box.pack_start(label, False, False, 0)


        self.textview = gtk.TextView(buffer=None)
        self.textbuffer = self.textview.get_buffer()

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add(self.textview) # add textview into a scrolled window
        self.test_box.pack_start(self.scrolled_window)


        separator = gtk.HSeparator()
        # The last 3 arguments to pack_start are:
        # expand, fill, padding.
        separator.show()

        button_show_answer = gtk.Button("Show Answer/Question")
        button_show_answer.show()
        
        box_evaluate = gtk.HBox(False, 0)
        score_button_1 = gtk.Button("0")
        score_button_2 = gtk.Button("1")
        score_button_3 = gtk.Button("2")
        score_button_4 = gtk.Button("3")
        score_button_5 = gtk.Button("4")
        score_button_6 = gtk.Button("5")
        
        score_button_1.show()
        score_button_2.show()
        score_button_3.show()
        score_button_4.show()
        score_button_5.show()
        score_button_6.show()
        
        box_evaluate.pack_start(score_button_1, False, True, 1)
        box_evaluate.pack_start(score_button_2, False, True, 1)
        box_evaluate.pack_start(score_button_3, False, True, 1)
        box_evaluate.pack_start(score_button_4, False, True, 1)
        box_evaluate.pack_start(score_button_5, False, True, 1)
        box_evaluate.pack_start(score_button_6, False, True, 1)

        box_evaluate.show()


        previous_card_button = gtk.Button("Previous")
        previous_card_button.connect("clicked", self.show_committed_card, 'prev')
        previous_card_button.show()

        next_card_button = gtk.Button("Next")
        next_card_button.connect("clicked", self.show_committed_card, 'next')
        next_card_button.show()

        quit_test_button = gtk.Button("Quit Test")
        quit_test_button.connect("clicked", self.quit_test)
        quit_test_button.show()

        box_navigate = gtk.HBox(False, 0)

        box_navigate.pack_start(previous_card_button, False, True, 1)
        box_navigate.pack_start(next_card_button, False, True, 1)
        box_navigate.pack_end(quit_test_button, False, True, 1)

        box_navigate.show()
        
        self.test_box.pack_end(box_navigate, False, True, 5)
        self.test_box.pack_end(box_evaluate, False, True, 5)
        self.test_box.pack_end(button_show_answer, False, True, 3)
        self.test_box.pack_end(separator, False, True, 5)


        self.test_box.show()
        self.window.remove(self.mainbox)
        self.window.add(self.test_box)
        #self.window.show()


    def study(self, widget, data=None):
        self.study_box = gtk.VBox(False, 0)
        
        label = gtk.Label('card')
        label.set_alignment(0, 0)
        label.show()
        self.study_box.pack_start(label, False, False, 0)


        self.textview = gtk.TextView(buffer=None)
        self.textbuffer = self.textview.get_buffer()

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add(self.textview) # add textview into a scrolled window
        self.study_box.pack_start(self.scrolled_window)


        separator = gtk.HSeparator()
        # The last 3 arguments to pack_start are:
        # expand, fill, padding.
        separator.show()

        button_show_answer = gtk.Button("Show Answer/Question")
        button_show_answer.show()
        
        box_evaluate = gtk.HBox(False, 0)
        right_button = gtk.Button("Right")
        wrong_button = gtk.Button("Wrong")
        
        right_button.show()
        wrong_button.show()

        box_evaluate.pack_start(right_button, False, True, 1)
        box_evaluate.pack_start(wrong_button, False, True, 1)

        box_evaluate.show()


        previous_card_button = gtk.Button("Previous")
        previous_card_button.connect("clicked", self.show_committed_card, 'prev')
        previous_card_button.show()

        next_card_button = gtk.Button("Next")
        next_card_button.connect("clicked", self.show_committed_card, 'next')
        next_card_button.show()

        quit_test_button = gtk.Button("Quit Test")
        quit_test_button.connect("clicked", self.quit_study)
        quit_test_button.show()

        box_navigate = gtk.HBox(False, 0)

        box_navigate.pack_start(previous_card_button, False, True, 1)
        box_navigate.pack_start(next_card_button, False, True, 1)
        box_navigate.pack_end(quit_test_button, False, True, 1)

        box_navigate.show()
        
        self.study_box.pack_end(box_navigate, False, True, 5)
        self.study_box.pack_end(box_evaluate, False, True, 5)
        self.study_box.pack_end(button_show_answer, False, True, 3)
        self.study_box.pack_end(separator, False, True, 5)


        self.study_box.show()
        self.window.remove(self.mainbox)
        self.window.add(self.study_box)
        

    def __init__(self, all_card_list):
        self.index = 0 # used for indicate the element in card_list
        self.all_card_list = all_card_list
        [self.committed_list, self.uncommitted_list] = superfunc.seperate_committed_uncommitted(all_card_list)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.connect("destroy", lambda w: gtk.main_quit())
        self.window.set_title("SuperMemo")
        self.window.set_border_width(5)
                
        self.mainbox = gtk.HBox(False, 0)
        
        self.button_test = gtk.Button("Test")
        self.button_test.show()
        self.mainbox.pack_start(self.button_test)
        self.button_test.connect("clicked", self.test)
        
        self.button_study = gtk.Button("Study")
        self.button_study.show()
        self.mainbox.pack_start(self.button_study)
        self.button_study.connect("clicked", self.study)

        
        self.mainbox.show()
        self.window.add(self.mainbox)
        self.window.show()

        
def main():
    gtk.main()


#if __name__ == "__main__":
datafile = 'words.txt'
card_list = superfunc.get_all_cards_from_file(datafile)


board = Mainboard(card_list)
main()

