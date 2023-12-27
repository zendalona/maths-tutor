###########################################################################
#    Maths-Tutor
#
#    Copyright (C) 2022-2023 Roopasree A P <roopasreeap@gmail.com>
#    Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>
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
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

from MathsTutor.tutor import MathsTutorWindow
from MathsTutor import global_var


import pygame

operator_mapping = {
    'Addition(+)': {
        'Easy': 'add_easy.txt',
        'Medium': 'add_med.txt',
        'Hard': 'add_hard.txt',
    },
    'Subtraction(-)': {
        'Easy': 'sub_easy.txt',
        'Medium': 'sub_med.txt',
        'Hard': 'sub_hard.txt',
    },
    'Multiplication(*)': {
        'Easy': 'mul_easy.txt',
        'Medium': 'mul_med.txt',
        'Hard': 'mul_hard.txt',
    },
    'Division(/)': {
        'Easy': 'div_easy.txt',
        'Medium': 'div_med.txt',
        'Hard': 'div_hard.txt',
    },
}

class SelectGame(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self)
        # Initialize pygame mixer
        pygame.mixer.init()

        # Load and play the background music
        pygame.mixer.music.load(global_var.data_dir+'/sounds/backgroundmusic.ogg')
        # Set the volume
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # -1 will loop the music indefinitely

        # Set background color to white
        self.modify_bg(Gtk.StateType.NORMAL, Gdk.color_parse("white"))

        # Create a HeaderBar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title("Maths-Tutor")
        self.set_titlebar(header_bar)

        
        # Horizontal box for About, User-Guide, and Quit
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)

        # Create about button
        about_button = Gtk.Button(label="About")
        about_button.connect("clicked", self.show_about_dialog)
        about_button.set_size_request(100, 30)
        hbox2.pack_start(about_button, False, False, 0)

        # Create user guide button
        user_guide_button = Gtk.Button(label="Help")
        user_guide_button.connect("clicked", self.on_user_guide_clicked)
        user_guide_button.set_size_request(100, 30)
        hbox2.pack_start(user_guide_button, False, False, 0)

        # Creating quit button
        quit_button = Gtk.Button(label="Quit")
        # Connect the clicked signal to the on_quit_clicked method
        quit_button.connect("clicked", self.on_quit_clicked)
        quit_button.set_size_request(100, 30)
        hbox2.pack_end(quit_button, False, False, 0)

        # Create a VBox to organize components vertically
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        vbox.set_margin_start(20)
        vbox.set_margin_end(20)
        vbox.set_margin_top(20)
        vbox.set_margin_bottom(20)
        vbox.set_size_request(400, 400)  # Set a fixed width
        # Add hbox2 to the main layout
        vbox.pack_end(hbox2, False, False, 0)

        # Create a HBox for the operator labels and ComboBox
        operator_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        select_operator_label = Gtk.Label(label="Choose the Operator:", xalign=0, yalign=0.5)
        select_operator_label.override_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 0, 1, 1))  # Blue color
        operator_box.pack_start(select_operator_label, False, False, 0)

        self.operator_combobox = Gtk.ComboBoxText()
        for operator in operator_mapping.keys():
            self.operator_combobox.append_text(operator)
        self.operator_combobox.set_active(0)
        operator_box.pack_start(self.operator_combobox, False, False, 0)

        # Create a variable to store the selected operator
        self.selected_operator = ""

        # Create a HBox for the level labels and ComboBox
        level_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        select_mode_label = Gtk.Label(label="Choose the Difficulty:", xalign=0, yalign=0.5)
        select_mode_label.override_color(Gtk.StateType.NORMAL, Gdk.RGBA(0, 0, 1, 1))  # Blue color
        level_box.pack_start(select_mode_label, False, False, 0)

        self.mode_combobox = Gtk.ComboBoxText()

        for difficulty in operator_mapping[list(operator_mapping.keys())[0]].keys():
            self.mode_combobox.append_text(difficulty)
        self.mode_combobox.set_active(0)
        level_box.pack_start(self.mode_combobox, False, False, 0)

        # Create a variable to store the selected operator
        self.selected_level = ""

        # Add components to the VBox
        vbox.pack_start(operator_box, False, False, 0)
        vbox.pack_start(level_box, False, False, 0)

        start_button = Gtk.ToggleButton(label="Start")
        start_button.connect("clicked", self.on_start_button_clicked)
        start_button.get_style_context().add_class("button")

        load_button = Gtk.ToggleButton(label="Load Questions")
        load_button.connect("clicked", self.on_load_button_clicked)
        load_button.get_style_context().add_class("button")

        vbox.pack_start(start_button, False, False, 0)
        vbox.pack_start(load_button, False, False, 0)


        # Modify the style context of the labels to set text color to black
        label_style_context = Gtk.Label().get_style_context()
        label_style_context.add_class(Gtk.STYLE_CLASS_LABEL)

        self.add(vbox)

        # Disable window maximizing
        self.set_resizable(False)
        
        self.connect("destroy", Gtk.main_quit)

        self.show_all()

        Gtk.main()

    def on_start_button_clicked(self, button):
        selected_operator = self.operator_combobox.get_active_text()
        selected_mode = self.mode_combobox.get_active_text()
        file_path = operator_mapping.get(selected_operator, {}).get(selected_mode)
        self.start_game(global_var.data_dir+"/lessons/"+file_path)


    def start_game(self, file_path):
        print("Starting game with file : "+file_path)

        # Destroy the current window
        self.destroy()
        
        game_window = MathsTutorWindow(file_path)
        game_window.show_all()

    def on_load_button_clicked(self, button):
        # Create a file dialog to choose a file
        dialog = Gtk.FileChooserDialog("Please choose a lesson file", self,
        Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
        Gtk.STOCK_OPEN, Gtk.ResponseType.OK))

        # Add filters to display only text files
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)

        # Run the dialog and check the response
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            # Get the selected file
            selected_file = dialog.get_filename()
            dialog.destroy()
            self.start_game(selected_file)

        elif response == Gtk.ResponseType.CANCEL:
            dialog.destroy()

    def show_about_dialog(self, button):
        about_dialog = Gtk.AboutDialog()

        # Set the relevant properties of the about dialog
        about_dialog.set_program_name("MATHS TUTOR GAME\n 0.1 \n\nMATHS TUTOR is a game to develop students calculation ability in maths and to judge themselves.\n Which is helpful to the students who have basic knowledge in maths. \n They  want to answer the questions they got and can lead into progress if they can answer the questions correctly.  \n\n   Copyright(C) 2022-2023 ROOPASREE A P <roopasreeap@gmail.com>\n\n   Supervised by  Zendalona(2022-2023)\n\n This program is free software you can redistribute it and or modify \nit under the terms of GNU General Public License as published by the free software foundation \n either gpl3 of the license.This program is distributed in the hope that it will be useful,\n but without any warranty without even the implied warranty of merchantability or fitness for a particular purpose.\n see the GNU General Public License for more details") 
        
        #self.set_version("")
        
        about_dialog.set_website_label("GNU General Public License,version 0.1\n\n" "Visit MATHS TUTOR Home page")
        
        about_dialog.set_website("http://wwww,zendalona.com/maths-tutor")
        about_dialog.set_authors(["Roopasree A P"])
        about_dialog.set_documenters(["Roopasree A P"])
        about_dialog.set_artists(["Nalin Sathyan" ,"Dr.Saritha Namboodiri", "Subha I N", "Bhavya P V", "K.Sathyaseelan"])
        
        about_dialog.run()
        about_dialog.destroy()
    
    
    def on_user_guide_clicked(self, button):
        # Add code to show the user guide or perform other actions
        print("USER-GUIDE")

    def on_quit_clicked(self, widget):
        Gtk.main_quit()


if __name__ == "__main__":
    win = SelectGame()
