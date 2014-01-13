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

    def quit_test(self, widget, data=None):
        self.window.remove(self.test_box)
        self.window.add(self.mainbox)

    def quit_study(self, widget, data=None):
        self.window.remove(self.study_box)
        self.window.add(self.mainbox)

    def filp(self, widget, card):
        #pdb.set_trace()
        if self.current_card_side == 'front':
            self.textbuffer.set_text('Answer:\n' + card.answer)
            self.current_card_side = 'back'
        elif self.current_card_side == 'back':
            self.textbuffer.set_text('Question:\n' + card.question)
            self.current_card_side = 'front'
        else:
            print 'argument of card_side has error'
        
        self.textview.show()
        #self.scrolled_window.show()


    def set_card_index(self, widget, command):
        if len(self.test_list) == 0:
            self.textbuffer.set_text("no card")
        else:
            if command == 'prev':
                self.current_card_index -= 1
                #if len(self.test_list) > 0:
                self.current_card_index %= len(self.test_list)
            elif command == 'next':
                self.current_card_index += 1
                self.current_card_index %= len(self.test_list)
            else:
                print 'navigate argument error'

            self.textbuffer.set_text('Question:\n' + self.test_list[self.current_card_index].question)
            self.current_card_side = 'front'
        ## the following code may be used in browse mode
        # if self.current_card_side == 'front':
        #     self.textbuffer.set_text('Question:\n' + self.test_list[self.current_card_index].question)
        # elif self.current_card_side == 'back':
        #     self.textbuffer.set_text('Answer:\n' + self.test_list[self.current_card_index].answer)
        # else:
        #     print 'current_card_side error'


    def evalute_card(self, widget, score):
        if len(self.test_list) > 0:
            card = self.test_list[self.current_card_index]
            card.update(score)
            self.test_list.remove(card)
            if score < 3:
                self.study_list.append(card)
            self.current_card_index += 1
            #pdb.set_trace()
            if len(self.test_list) == 0:
                self.textbuffer.set_text('No card, today')
            else:
                self.current_card_index %= len(self.test_list)
                self.textbuffer.set_text('Question:\n' + self.test_list[self.current_card_index].question)


    def test(self, widget, data=None):
        for card in self.committed_list:
            if date.fromordinal(1) < card.next_date <= self.today:
                self.test_list.append(card)

        self.test_box = gtk.VBox(False, 0)
        
        label = gtk.Label('Test')
        label.set_alignment(0, 0)
        label.show()
        self.test_box.pack_start(label, False, False, 0)

        
        self.textview = gtk.TextView(buffer=None)
        self.textview.set_justification(gtk.JUSTIFY_CENTER)
        self.textbuffer = self.textview.get_buffer()

        if len(self.test_list) == 0:
            self.textbuffer.set_text('No card to be tested today')
        else:
            self.textbuffer.set_text('Question:\n' + self.test_list[self.current_card_index].question)

        self.textview.show()

        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add(self.textview) # add textview into a scrolled window
        self.test_box.pack_start(self.scrolled_window)


        self.scrolled_window.show()

        separator = gtk.HSeparator()
        # The last 3 arguments to pack_start are:
        # expand, fill, padding.
        separator.show()
        
        button_show_answer = gtk.Button("Show Answer/Question")
        button_show_answer.connect("clicked", self.filp, self.test_list[self.current_card_index])
        button_show_answer.show()

        
        box_evaluate = gtk.HBox(False, 0)
        score_button_0 = gtk.Button("0")
        score_button_1 = gtk.Button("1")
        score_button_2 = gtk.Button("2")
        score_button_3 = gtk.Button("3")
        score_button_4 = gtk.Button("4")
        score_button_5 = gtk.Button("5")
        
        score_button_0.connect("clicked", self.evalute_card, 0)
        score_button_1.connect("clicked", self.evalute_card, 1)
        score_button_2.connect("clicked", self.evalute_card, 2)
        score_button_3.connect("clicked", self.evalute_card, 3)
        score_button_4.connect("clicked", self.evalute_card, 4)
        score_button_5.connect("clicked", self.evalute_card, 5)


        score_button_0.show()
        score_button_1.show()
        score_button_2.show()
        score_button_3.show()
        score_button_4.show()
        score_button_5.show()
        
        box_evaluate.pack_start(score_button_0, False, True, 1)
        box_evaluate.pack_start(score_button_1, False, True, 1)
        box_evaluate.pack_start(score_button_2, False, True, 1)
        box_evaluate.pack_start(score_button_3, False, True, 1)
        box_evaluate.pack_start(score_button_4, False, True, 1)
        box_evaluate.pack_start(score_button_5, False, True, 1)

        box_evaluate.show()

        previous_card_button = gtk.Button("Previous")
        previous_card_button.connect("clicked", self.set_card_index, 'prev')
        previous_card_button.show()

        next_card_button = gtk.Button("Next")
        next_card_button.connect("clicked", self.set_card_index, 'next')
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
        
        self.textview.show()


        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.scrolled_window.add(self.textview) # add textview into a scrolled window
        self.study_box.pack_start(self.scrolled_window)

        self.scrolled_window.show()

        separator = gtk.HSeparator()
        # The last 3 arguments to pack_start are:
        # expand, fill, padding.
        separator.show()

        button_show_answer = gtk.Button("Show Answer/Question")
        button_show_answer.connect("clicked", self.filp, self.study_list) #change to 'self.study_list' later
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
        previous_card_button.connect("clicked", self.set_card_index, 'prev', self.len_committed_list)
        previous_card_button.show()

        next_card_button = gtk.Button("Next")
        next_card_button.connect("clicked", self.set_card_index, 'next', self.len_committed_list)
        next_card_button.show()

        quit_test_button = gtk.Button("Quit Study")
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
        self.today = date.today()

        self.current_card_index = 0 # used for indicate the element in card_list
        self.current_card_side = 'front' # 'front'(question) or 'back'(answer)

        self.all_card_list = all_card_list
        [self.committed_list, self.uncommitted_list] = superfunc.seperate_committed_uncommitted(all_card_list)
        self.test_list = []
        self.study_list = []

        self.len_committed_list = len(self.committed_list)
        self.len_uncommitted_list = len(self.uncommitted_list)
        self.len_all_card_list = len(self.all_card_list)
        self.len_study_list = len(self.study_list)

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_default_size(320, 320)
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

