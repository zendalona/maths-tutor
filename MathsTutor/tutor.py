###########################################################################
#    Maths-Tutor
#
#    Copyright (C) 2022-2023 Roopasree A P <roopasreeap@gmail.com>    
#    
#    This project is Supervised by Zendalona(2022-2023)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###########################################################################


import gi
import time
import speechd
gi.require_version("Gtk", "3.0")
gi.require_version('Gst', '1.0')
from gi.repository import Gtk, Gdk, GObject, GLib,Pango

from MathsTutor import global_var

# Import GST
from gi.repository import Gst
import re
import os
import threading
import math
import random
import pygame

class MathsTutorWindow(Gtk.Window):
    def __init__(self,file_name):
        Gtk.Window.__init__(self, title="Maths-Tutor")
        self.set_border_width(10)

        # initialize Gstreamer
        Gst.init(None)
        
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the background music
        pygame.mixer.music.load(global_var.data_dir+'/sounds/backgroundmusic.ogg')
        # Set the volume
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # -1 will loop the music indefinitely
        #Create a vertical box layout
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)

        vbox2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        # Add the VBox container to the main window
        self.add(vbox)
        
        self.welcome_message = "Welcome! \nPress enter to start "
        
        
        # create  a Gtk label
        self.label = Gtk.Label()
        
        # Set the text of the label to the value of welcome_message
        self.label.set_text(self.welcome_message)
        
        # Modify the font of the label
        vbox2.modify_font(Pango.FontDescription("Sans 40"))
        
        
        
        # Define the font color
        font_color = "#0603f0"
        
        # Define the background color
        background_color = "#ffffff"
        
        # Set the font color
        vbox2.modify_fg(Gtk.StateFlags.NORMAL, Gdk.color_parse(font_color))
        
        # Set the background color
        vbox2.modify_bg(Gtk.StateFlags.NORMAL, Gdk.color_parse(background_color))
        
        # Add the label to the vbox container
        vbox2.pack_start(self.label, True, True, 0)
        
        
        #Create a horizontal box layout 
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        fix1 = Gtk.Fixed()
        hbox.pack_start(fix1, True, True, 0)
        
        #Add the hbox to the vbox container
        vbox2.pack_start(hbox, False, False, 0)

       
        #Create a Gtk.Entry widget and assign it to self.entry
        self.entry = Gtk.Entry()
        
        # Connect the "activate" signal of the entry widget to the self.on_entry_activated method
        self.entry.connect("activate", self.on_entry_activated)
        
        #Add entry to horizontal box
        hbox.pack_start(self.entry, False, False, 0)

        fix2 = Gtk.Fixed()
        hbox.pack_start(fix2, True, True, 0)
        
        
        #Create multiple instances of GtkImage and add them to the vertical box
        self.image = Gtk.Image()
        self.set_image("welcome", 3)
        vbox2.pack_start(self.image, True, True, 0)

        vbox.pack_start(vbox2, True, True, 0)
        
        #Horizontal box for About and User-Guide
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)       
     
        
        # Creating quit button
        quit_button = Gtk.Button(label="Quit")
        # Connect the clicked signal to the on_quit_clicked method
        quit_button.connect("clicked", self.on_quit_clicked)
        quit_button.set_size_request(200, 30)
        hbox2.pack_end(quit_button, False, False, 0)
        
        # Add the hbox2 to the vbox container
        vbox.pack_start(hbox2, False, True, 0)

        self.current_question_index = -1
        self.wrong=False
        self.excellent=0
        self.final_score=0
        self.incorrect_answer_count=0
        
        
        # Create a playbin element with the name 'player' and assign it to self.player
        self.player = Gst.ElementFactory.make('playbin', 'player')
        
        # Playing starting sound
        self.play_file('welcome')
        
        
        # Initialize speechd client
        self.spd_cli = speechd.Client("MathTeacher")
        self.spd_cli.set_output_module("rhvoice")
        self.speak(self.welcome_message)
        
        self.connect('delete-event', self.on_destroy)
        self.connect('destroy', self.on_destroy)
        
        self.load_question_file(file_name)
        
        self.set_default_size(500,700)
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        Gtk.main()


        

    #Function to play sounds
    def play_file(self, name, rand_range=1):
        print("Playing file " + name + " rand ="+str(rand_range));
        if(rand_range == 1):
            file_path_and_name = 'file:///'+global_var.data_dir+'/sounds/'+name+".ogg";
        else:
            value = str(random.randint(1, rand_range))
            file_path_and_name = 'file:///'+global_var.data_dir+'/sounds/'+name+"-"+value+".ogg";
        self.player.set_state(Gst.State.READY)
        self.player.set_property('uri',file_path_and_name)
        self.player.set_state(Gst.State.PLAYING)
    
    
    #Function to set image from file 
    def set_image(self, name, rand_range):
	    value = str(random.randint(1, rand_range))
	    self.image.set_from_file(global_var.data_dir+"/images/"+name+"-"+value+".gif");

    def speak(self, text, enqueue=False):
        if(enqueue == False):
            self.spd_cli.cancel();
        self.spd_cli.speak(text)
   
    #Function to read the questions from the file
    def load_question_file(self, file_path):
        self.list = []
        self.current_question_index = -1
        self.wrong=False
        with open(file_path, "r") as file:
            for line in file:
                stripped_line = line.strip()
                self.list.append(stripped_line)
    
    
    # Function to covert the signs to text
    def convert_signs(self, text):
        return text.replace("+"," plus ").replace("-"," minus ").replace("*"," multiply ").replace("/"," devided by ")

    

    # Function to display the question and corresponding images and sounds
    def on_entry_activated(self,entry):
        if self.current_question_index == -1:
            self.starting_time = time.time();
            self.wrong=False
            self.excellent=0
            self.final_score=0
            self.incorrect_answer_count=0
            self.next_question()
            
        else:
            answer = self.entry.get_text()
            correct_answer = self.answer
            
            if answer == correct_answer:                
                time_end = time.time()
                
                time_taken = time_end - self.time_start
                
                time_alotted = int(self.list[self.current_question_index].split("===")[2])
                
                self.incorrect_answer_count=0
                
                print(time_taken)
                if  time_taken < time_alotted:
                    self.excellent=self.excellent+3
                    self.final_score=self.final_score+5
                    self.speak("Excellent!")
                    self.label.set_text("Excellent!")
                    self.set_image("excellent", 3)
                    self.play_file("excellent", 3)
                elif time_taken < time_alotted+2:
                    self.excellent=self.excellent+2
                    self.final_score=self.final_score+4
                    self.speak("Very good!")
                    self.label.set_text("Very good!")
                    self.set_image("very-good", 3)
                    self.play_file("very-good", 3)
                elif time_taken < time_alotted+4:
                    self.final_score=self.final_score+3
                    self.speak("Good!")
                    self.label.set_text("Good!")
                    self.set_image("good", 3)
                    self.play_file("good", 3)
                elif time_taken < time_alotted+6:
                    self.excellent=0
                    self.final_score=self.final_score+2
                    self.speak("Not bad!")
                    self.label.set_text("Not bad!")
                    self.set_image("not-bad", 3)
                    self.play_file('not-bad', 3)
                    
                else :
                    self.excellent=-1
                    self.final_score=self.final_score+1
                    self.speak("Okay!")
                    self.label.set_text("Okay!")
                    self.set_image("okay", 3)
                    self.play_file('okay', 3)

            else:
                self.wrong=True
                self.final_score=self.final_score-1
                self.incorrect_answer_count=self.incorrect_answer_count+1
                if self.incorrect_answer_count==3:
                    self.set_image("wrong-anwser-repeted", 2)
                    self.play_file("wrong-anwser-repeted", 3)
                    self.incorrect_answer_count = 0
                    text = "Sorry! the correct answer is "
                    self.label.set_text(text+self.answer)
                    if(len(self.answer.split(".")) > 1):
                        li = list(self.answer.split(".")[1])
                        self.speak(text+self.answer.split(".")[0]+" point "+" ".join(li))
                    else:
                        self.speak(text+self.answer)
                    
                else :
                    self.label.set_text("Sorry! let's try again")
                    self.speak("Sorry! let's try again")
                    self.set_image("wrong-anwser", 3)
                    self.play_file("wrong-anwser", 3)
            GLib.timeout_add_seconds(3,self.next_question)
            self.entry.set_text("")
            
    
    # Function to set next question        
    def next_question(self):
        self.time_start = time.time()
        self.entry.grab_focus()
        
        if self.wrong==True:
            self.label.set_text(self.question)
            threading.Thread(target=self.announce_question,args=[self.question, self.make_sound, self.current_question_index]).start()
            self.set_image("wrong-anwser", 3)
            self.wrong=False
        else:

            if self.excellent >= 3 :
                self.current_question_index = self.current_question_index + self.excellent
                
            else :
                self.current_question_index = self.current_question_index + 1
            if self.current_question_index < len(self.list)-1:
                print(len(self.list))
                if("?" in self.list[self.current_question_index]):
                    question_to_pass = self.list[self.current_question_index].split("===")[0]
                    print("Question_to_pass : "+question_to_pass)
                    self.question = self.question_parser(question_to_pass)
                    number = eval(self.question)
                    if number==math.trunc(number):
                            self.answer = str(math.trunc(number))
                    else:
                        num= round(eval(str(number)),2)
                        self.answer = str(num)
                    print(self.answer)
                else:
                    self.question = self.list[self.current_question_index].split("===")[0]
                    self.answer = self.list[self.current_question_index].split("===")[1]

                self.make_sound = self.list[self.current_question_index].split("===")[3]
                self.label.set_text(self.question)                
                threading.Thread(target=self.announce_question,args=[self.question, self.make_sound, self.current_question_index]).start()
                
                self.entry.set_text("")
                self.set_image("question", 2)
            else:
                minute, seconds = divmod(round(time.time()-self.starting_time), 60)
                text = "Successfully finished! Your score is "+str(self.final_score)+\
                "!\nTime taken "+str(minute)+" minutes and "+str(seconds)+" seconds!"+\
                "\nPress enter to start again.";
                self.speak(text)
                self.label.set_text(text)
                self.set_image("finished", 3)
                self.play_file("finished", 3)
                self.current_question_index = -1
                
                

    # Create random numbers
    def get_randome_number(self, value1, value2):
        if(int(value1) < int(value2)):
            return str(random.randint(int(value1),int(value2)))
        else:
            return str(random.randint(int(value2),int(value1)))


    def question_parser(self, question):
        first = True
        second = False
        digit_one = ""
        digit_two = ""
        output = ""
        for i in range(0, len(question)):
            item = question[i]

            if(item.isdigit()):
                if(second==False):
                    digit_one = digit_one+item
                else:
                    digit_two = digit_two+item
            elif(item == ","):
                second=True
            else:
                second=False
                if(digit_two != ""):
                    output = output+self.get_randome_number(digit_one, digit_two)
                else:
                    output = output+digit_one
                output = output+item

                digit_one = ""
                digit_two = ""

            if(i==len(question)-1):
                if(digit_one != ""):
                    if(digit_two != ""):
                        output = output+self.get_randome_number(digit_one, digit_two)
                    else:
                        output = output+digit_one
        return output;
    
    # Function to Play bell sound according to the numbers
    def announce_question(self, question, make_sound, announcing_question_index):
        print(question, make_sound)
        if(make_sound == '1'):
            item_list = re.split(r'(\d+)', question)[1:-1]
            for item in item_list:
                # To prevent announcement on user answer
                if(announcing_question_index != self.current_question_index):
                    print("STOOOOOOOPPPPPPPPPP")
                    return;
                if item.isnumeric():

                    num = int(item)
                    while(num > 0):
                        num = num-1;
                        self.play_file("coin")
                        time.sleep(0.7)
                else:
                    self.speak(self.convert_signs(item))
                    time.sleep(0.7)
            if(announcing_question_index != self.current_question_index):
                self.speak("equals to? ")
        else:
            self.play_file("question")
            time.sleep(0.7)
            self.speak(self.convert_signs(self.question)+" equals to ? ")

    def on_destroy(self, widget=None, *data):
        print("CLOSE")
        self.spd_cli.close()
        
    def on_quit_clicked(self, widget):
        Gtk.main_quit()


if __name__ == "__main__":
    win = MathsTutorWindow()
