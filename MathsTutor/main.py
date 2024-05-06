###########################################################################
#    Maths-Tutor
#
#    Copyright (C) 2022-2023 Roopasree A P <roopasreeap@gmail.com>
#    Copyright (C) 2023-2024 Greeshna Sarath <greeshnamohan001@gmail.com>
#    Copyright (C) 2024-2025 Nalin Sathyan <nalin.x.linux@gmail.com>
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
from gi.repository import Gtk, Gdk, Pango
from gi.repository import GdkPixbuf


from MathsTutor.tutor import MathsTutorBin
from MathsTutor import speech
from MathsTutor import preferences
from MathsTutor import global_var

import pygame

import webbrowser

import gettext
gettext.bindtextdomain(global_var.app_name, global_var.locale_dir)
gettext.textdomain(global_var.app_name)
_ = gettext.gettext

language_dict = {"en":"English", "hi":"Hindi", "ar":"Arabic", "ta":"Tamil", "ml":"Malayalam", "sa":"Sanskrit"}


class LanguageSelectionDialog(Gtk.Dialog):
    def __init__(self, parent, language):
        Gtk.Dialog.__init__(self, _("Maths-Tutor"), parent, 0,
            (Gtk.STOCK_OK, Gtk.ResponseType.OK,
             Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL))

        self.set_default_size(200, 150)

        # Create a ComboBox with language options
        label_language = Gtk.Label(_("Select Language"))
        self.combobox = Gtk.ComboBoxText()
        for item in language_dict.values():
            self.combobox.append_text(item)
        self.combobox.set_active(language)  # Set the default selection
        label_language.set_mnemonic_widget(self.combobox)
        hbox1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        hbox1.pack_start(label_language, False, False, 0)
        hbox1.pack_start(self.combobox, False, False, 0)

        # Create a CheckButton with remember option
        self.remember_checkbox = Gtk.CheckButton(_("Remember Selection"))

        # Pack the ComboBox into a vertical box
        box = self.get_content_area()
        box.add(hbox1)
        box.add(self.remember_checkbox)

        self.show_all()

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

        # User Preferences
        self.pref = preferences.Preferences()
        self.pref.load_preferences_from_file(global_var.user_preferences_file_path)

        # Store the previous language for checking if a speech synthesizer
        # or language change is needed.
        previous_language = self.pref.language

        if(self.pref.language == -1):
            self.pref.language = 0


        if(self.pref.remember_language == 1):
            selected_language = list(language_dict)[self.pref.language]
        else:
            # Create and show the language selection dialog
            lang_dialog = LanguageSelectionDialog(self, self.pref.language)
            response = lang_dialog.run()

            if response == Gtk.ResponseType.OK:
                # Retrieve the selected language from the ComboBox
                active = lang_dialog.combobox.get_active()
                selected_language = list(language_dict)[active]
                self.pref.language = active
                if(lang_dialog.remember_checkbox.get_active()):
                    self.pref.remember_language = 1
            else:
                return

            lang_dialog.destroy()

        try:
            lang1 = gettext.translation(global_var.app_name, languages=[selected_language])
            lang1.install()
            global _;
            _ = lang1.gettext
        except:
            self.pref.language = 0

        # Checking if a speech synthesizer or speech language change is needed.
        if(previous_language != self.pref.language):
            self.pref.speech_language = -1

        self.operator_mapping = {
            _('Addition (+)'): {
                _('Simple'): 'add_simple.txt',
                _('Easy'): 'add_easy.txt',
                _('Medium'): 'add_med.txt',
                _('Hard'): 'add_hard.txt',
                _('Challenging'): 'add_chlg.txt',
            },
            _('Subtraction (-)'): {
                _('Simple'): 'sub_simple.txt',
                _('Easy'): 'sub_easy.txt',
                _('Medium'): 'sub_med.txt',
                _('Hard'): 'sub_hard.txt',
                _('Challenging'): 'sub_chlg.txt',
            },
            _('Multiplication (*)'): {
                _('Simple'): 'mul_simple.txt',
                _('Easy'): 'mul_easy.txt',
                _('Medium'): 'mul_med.txt',
                _('Hard'): 'mul_hard.txt',
                _('Challenging'): 'mul_chlg.txt',
            },
            _('Division (/)'): {
                _('Simple'): 'div_simple.txt',
                _('Easy'): 'div_easy.txt',
                _('Medium'): 'div_med.txt',
                _('Hard'): 'div_hard.txt',
                _('Challenging'): 'div_chlg.txt',
            },
            _('Percentage (%)'): {
                _('Simple'): 'per_simple.txt',
                _('Easy'): 'per_easy.txt',
                _('Medium'): 'per_med.txt',
            },
        }

        # Create a HeaderBar
        header_bar = Gtk.HeaderBar()
        header_bar.set_show_close_button(True)
        header_bar.set_title(_("Maths-Tutor"))
        self.set_titlebar(header_bar)

        self.icon_pixbuf = GdkPixbuf.Pixbuf.new_from_file(global_var.data_dir+"/icon.png")
        self.set_icon(self.icon_pixbuf)
        
        # Horizontal box for Show/Hide Settings, About, User-Guide, and Quit
        hbox2 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox2.set_margin_start(20)
        hbox2.set_margin_end(20)
        hbox2.set_margin_top(20)
        hbox2.set_margin_bottom(20)

        # Create settings button
        self.show_controls_button = Gtk.Button(label=_("Show Settings"))
        self.show_controls_button.connect("clicked", self.show_controls)
        self.show_controls_button.set_size_request(100, 30)

        # Add an accelerator for Ctrl+Q
        self.my_accelerators = Gtk.AccelGroup()
        self.add_accel_group(self.my_accelerators)
        key, modifier = Gtk.accelerator_parse("<Alt>S")
        self.show_controls_button.add_accelerator("clicked",
                               self.my_accelerators, key, modifier,
                               Gtk.AccelFlags.VISIBLE)

        hbox2.pack_start(self.show_controls_button, False, False, 0)


        # Create about button
        about_button = Gtk.Button(label=_("About"))
        about_button.connect("clicked", self.show_about_dialog)
        about_button.set_size_request(100, 30)
        hbox2.pack_start(about_button, False, False, 0)

        # Create user guide button
        user_guide_button = Gtk.Button(label=_("Help"))
        user_guide_button.connect("clicked", self.on_help_clicked)
        user_guide_button.set_size_request(100, 30)
        hbox2.pack_start(user_guide_button, False, False, 0)

        # Creating quit button
        quit_button = Gtk.Button(label=_("Quit"))
        # Connect the clicked signal to the on_quit_clicked method
        quit_button.connect("clicked", self.on_quit_clicked)
        quit_button.set_size_request(100, 30)
        hbox2.pack_end(quit_button, False, False, 0)

        # Create a VBox to organize components vertically
        self.vbox_controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.vbox_controls.set_margin_start(20)
        self.vbox_controls.set_margin_end(20)
        self.vbox_controls.set_margin_top(20)
        self.vbox_controls.set_margin_bottom(20)

        # Create a HBox for the operator labels and ComboBox
        operator_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        select_operator_label = Gtk.Label(label=_("Select Operation:"), xalign=0, yalign=0.5)
        operator_box.pack_start(select_operator_label, False, False, 0)

        self.operator_combobox = Gtk.ComboBoxText()
        for operator in self.operator_mapping.keys():
            self.operator_combobox.append_text(operator)

        self.operator_combobox.connect("changed", self.on_oprator_combobox_changed)
        operator_box.pack_start(self.operator_combobox, False, False, 0)
        select_operator_label.set_mnemonic_widget(self.operator_combobox)

        # Create a variable to store the selected operator
        self.selected_operator = ""

        # Create a HBox for the level labels and ComboBox
        level_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        select_mode_label = Gtk.Label(label=_("Select Difficulty Level:"), xalign=0, yalign=0.5)
        level_box.pack_start(select_mode_label, False, False, 0)

        self.mode_combobox = Gtk.ComboBoxText()
        level_box.pack_start(self.mode_combobox, False, False, 0)

        select_mode_label.set_mnemonic_widget(self.mode_combobox)

        self.operator_combobox.set_active(self.pref.operator)

        self.mode_combobox.set_active(self.pref.level)

        # Create a variable to store the selected operator
        self.selected_level = ""

        self.vbox_controls.pack_start(operator_box, False, False, 0)
        self.vbox_controls.pack_start(level_box, False, False, 0)

        start_button = Gtk.Button(label=_("Start"))
        start_button.connect("clicked", self.on_start_button_clicked)
        start_button.get_style_context().add_class("button")

        load_button = Gtk.Button(label=_("Load Questions"))
        load_button.connect("clicked", self.on_load_button_clicked)
        load_button.get_style_context().add_class("button")

        self.vbox_controls.pack_start(start_button, False, False, 0)
        self.vbox_controls.pack_start(load_button, False, False, 0)

        self.speech = speech.Speech()
        self.speech_synthesizers_list = self.speech.list_synthesizers()

        label_speech_synthesizer = Gtk.Label(_("Speech Synthesizer"))
        self.combobox_speech_synthesizer = Gtk.ComboBoxText()
        for item in self.speech_synthesizers_list:
            self.combobox_speech_synthesizer.append_text(item)
        self.combobox_speech_synthesizer.connect("changed", self.on_speech_synthesizer_changed)
        label_speech_synthesizer.set_mnemonic_widget(self.combobox_speech_synthesizer)
        hbox_speech_synthesizer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_speech_synthesizer.pack_start(label_speech_synthesizer, False, False, 0)
        hbox_speech_synthesizer.pack_start(self.combobox_speech_synthesizer, False, False, 0)
        self.vbox_controls.pack_start(hbox_speech_synthesizer, False, False, 0)

        label_speech_language = Gtk.Label(_("Speech Language"))
        self.combobox_speech_language = Gtk.ComboBoxText()
        label_speech_language.set_mnemonic_widget(self.combobox_speech_language)
        hbox_speech_language = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_speech_language.pack_start(label_speech_language, False, False, 0)
        hbox_speech_language.pack_start(self.combobox_speech_language, False, False, 0)
        self.vbox_controls.pack_start(hbox_speech_language, False, False, 0)

        label_speech_person = Gtk.Label(_("Speech Person"))
        self.combobox_speech_person = Gtk.ComboBoxText()
        label_speech_person.set_mnemonic_widget(self.combobox_speech_person)
        hbox_speech_person = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=5)
        hbox_speech_person.pack_start(label_speech_person, False, False, 0)
        hbox_speech_person.pack_start(self.combobox_speech_person, False, False, 0)
        self.vbox_controls.pack_start(hbox_speech_person, False, False, 0)

        """
        Speech synthesizer and language selection logic for keeping application
        always speak and preserving user speech preferences as it is.

        If no preferences: use espeak as synthesizer and set language
        If no language change from last preferences: use preferences as it is
        If language changed: try to set language in the same synthesizer.
               if not possible change synthesizer back to espeak-ng or espeak
        """

        if(self.pref.speech_synthesizer == -1):
            self.set_speech_synthesizer_for_all_languages()

        self.combobox_speech_synthesizer.set_active(self.pref.speech_synthesizer)
        self.speech.set_speech_rate(self.pref.speech_rate)

        # Create reset settings button
        button_reset_settings = Gtk.Button(label=_("Reset Settings"))
        button_reset_settings.connect("clicked", self.on_button_reset_settings_clicked)
        button_reset_settings.set_size_request(100, 30)
        self.vbox_controls.pack_start(button_reset_settings, False, False, 0)


        vbox_game_and_controls = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)

        self.game_bin = MathsTutorBin(self.speech, _)
        self.game_bin.connect_game_over_callback_function(self.move_game_to_next_level)
        vbox_game_and_controls.pack_start(self.game_bin, True, False, 0)

        vbox_game_and_controls.pack_start(self.vbox_controls, True, False, 0)

        label = Gtk.Label(_(
            "Note: Adjust the speech rate by pressing the apostrophe or semicolon key, "
            "which are located to the left of the Enter key. Use the Space key to replay "
            "the question, and employ the Shift key to hear the question in verbose mode. "
            "Utilize settings to change arithmetic operation, difficulty, load questions, "
            "speech language, voice, etc. Press Alt+S to open or hide settings."
        ))
        label.set_selectable(True)
        label.set_line_wrap(True)
        label.set_max_width_chars(50)
        label.set_margin_start(20)
        label.set_margin_end(20)
        vbox_game_and_controls.pack_start(label, False, False, 0)

        vbox_game_and_controls.pack_start(hbox2, False, False, 0)


        # Modify the style context of the labels to set text color to black
        label_style_context = Gtk.Label().get_style_context()
        label_style_context.add_class(Gtk.STYLE_CLASS_LABEL)

        self.add(vbox_game_and_controls)

        self.connect("destroy", self.on_quit_clicked)

        self.show_all()

        self.vbox_controls.hide()

        self.maximize()

        self.on_start_button_clicked("None")

        Gtk.main()

    def move_game_to_next_level(self):
        if(self.pref.level+1 < len(self.mode_combobox.get_model())):
            self.pref.level = self.pref.level+1
        else:
            if(self.pref.operator+1 < len(self.operator_combobox.get_model())):
                self.pref.level = 0
                self.pref.operator = self.pref.operator+1
            else:
                self.pref.level = 0
                self.pref.operator = 0

        self.operator_combobox.set_active(self.pref.operator)
        self.mode_combobox.set_active(self.pref.level)

        self.on_start_button_clicked("None")


    def on_button_reset_settings_clicked(self, widget):
        self.pref.set_default_preferences()

        # This won't set the GameBin to the default operator and level,
        # nor will it start the game. Users have to start it using the 'Start Game' option.
        self.operator_combobox.set_active(self.pref.operator)
        self.mode_combobox.set_active(self.pref.level)

        if(self.pref.speech_synthesizer == -1):
            self.set_speech_synthesizer_for_all_languages()

        self.combobox_speech_synthesizer.set_active(self.pref.speech_synthesizer)
        self.speech.set_speech_rate(self.pref.speech_rate)

    def set_speech_synthesizer_for_all_languages(self):
        if("espeak-ng" in self.speech_synthesizers_list):
           self.pref.speech_synthesizer = self.speech_synthesizers_list.index('espeak-ng')
        elif("espeak" in self.speech_synthesizers_list):
            self.pref.speech_synthesizer = self.speech_synthesizers_list.index('espeak')
        else:
           self.pref.speech_synthesizer = 0

    def set_speech_language_using_language(self):
        selected_language = list(language_dict)[self.pref.language]
        language_index = self.speech.get_language_index(selected_language)

        if(language_index != -1):
            self.pref.speech_language = language_index
            return True
        else:
           self.pref.speech_language = 0
           return False

    def on_speech_synthesizer_changed(self, *data):
        module_index = self.combobox_speech_synthesizer.get_active()

        self.pref.speech_synthesizer = module_index

        self.speech.set_synthesizer(self.speech_synthesizers_list[module_index])

        self.speech_language_person_dict = self.speech.get_language_person_dict()

        # Disconnecting for preventng function calls while clearing
        # combobox_speech_language or adding each language to the same
        try:
            self.combobox_speech_language.disconnect(self.on_speech_language_changed)
        except(TypeError):
            pass

        self.combobox_speech_language.remove_all()

        if(len(self.speech_language_person_dict.keys()) == 0):
            self.combobox_speech_language.append_text(_("Default"))
            self.pref.speech_language = 0
        else:
            for item in self.speech_language_person_dict.keys():
                self.combobox_speech_language.append_text(item)

        self.combobox_speech_language.connect("changed", self.on_speech_language_changed)

        # If there is no preferences or change in interface language set speech language using language
        if(self.pref.speech_language == -1):
            if(not self.set_speech_language_using_language()):
                self.set_speech_synthesizer_for_all_languages()
                self.combobox_speech_synthesizer.set_active(self.pref.speech_synthesizer)
                return


        if(self.pref.speech_language < len(self.speech_language_person_dict.keys())):
            self.combobox_speech_language.set_active(self.pref.speech_language)
        else:
            self.combobox_speech_language.set_active(0)
            self.pref.speech_language = 0

    def on_speech_language_changed(self, *data):
        # Disconnecting for preventng function calls while clearing
        # combobox_speech_language or adding each language to the same
        try:
            self.combobox_speech_person.disconnect(self.on_speech_person_changed)
        except(TypeError):
            pass

        self.combobox_speech_person.remove_all()

        if(len(list(self.speech_language_person_dict.keys())) == 0):
            self.combobox_speech_person.append_text(_("Default"))
            self.pref.speech_person = 0
            return

        index_language = self.combobox_speech_language.get_active()
        language = list(self.speech_language_person_dict.keys())[index_language]
        self.pref.speech_language = index_language

        for item in self.speech_language_person_dict[language]:
            self.combobox_speech_person.append_text(item)

        if(self.pref.speech_person >= len(self.speech_language_person_dict[language])):
            self.pref.speech_person = 0

        self.combobox_speech_person.connect("changed", self.on_speech_person_changed)

        self.speech.set_language(language)
        self.combobox_speech_person.set_active(self.pref.speech_person)


    def on_speech_person_changed(self, *data):
        index_language = self.combobox_speech_language.get_active()
        language = list(self.speech_language_person_dict.keys())[index_language]

        index_person = self.combobox_speech_person.get_active()
        if(index_person == -1):
            index_person = 0
        voice = self.speech_language_person_dict[language][index_person]

        self.pref.speech_person = index_person;

        self.speech.set_synthesis_voice(voice)


    def on_start_button_clicked(self, button):
        selected_operator = self.operator_combobox.get_active_text()
        self.pref.operator = self.operator_combobox.get_active()

        selected_mode = self.mode_combobox.get_active_text()
        self.pref.level = self.mode_combobox.get_active()

        file_path = self.operator_mapping.get(selected_operator, {}).get(selected_mode)
        self.start_game(global_var.data_dir+"/lessons/"+file_path)


    def start_game(self, file_path):
        self.game_bin.load_question_file(file_path)
        self.vbox_controls.hide()
        self.game_bin.show()
        self.show_controls_button.set_label(_("Show Settings"))
        self.queue_draw()


    def on_oprator_combobox_changed(self, widget):
        active = widget.get_active()
        self.mode_combobox.remove_all()

        for difficulty in self.operator_mapping[list(self.operator_mapping.keys())[active]].keys():
            self.mode_combobox.append_text(difficulty)

        self.mode_combobox.set_active(0)

    def on_load_button_clicked(self, button):
        # Create a file dialog to choose a file
        dialog = Gtk.FileChooserDialog(_("Please choose a lesson file"), self,
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

    def show_controls(self, button):
        if(self.vbox_controls.get_visible()):
           self.vbox_controls.hide()
           self.game_bin.show()
           self.game_bin.grab_focus_on_entry()
           button.set_label(_("Show Settings"))
        else:
            button.set_label(_("Hide Settings"))
            self.vbox_controls.show()
            self.game_bin.hide()
            self.operator_combobox.grab_focus()
        self.queue_draw()

    def show_about_dialog(self, button):
        about_dialog = Gtk.AboutDialog()

        # Set the relevant properties of the about dialog
        about_dialog.set_program_name("Maths-Tutor")

        about_dialog.set_icon(self.icon_pixbuf)
        about_dialog.set_logo(self.icon_pixbuf)
        about_dialog.set_comments("Maths-Tutor is a game designed to enhance "
        "one's calculation abilities in mathematics and enable them to self-assess.");
        
        about_dialog.set_license("GNU General Public License - GPL-2.0")
        
        about_dialog.set_website_label("Visit home - Zendalona")
        about_dialog.set_copyright("""Copyright (C) 2022-2023 Roopasree A P <roopasreeap@gmail.com>
        Copyright (C) 2022-2023 Greeshna Sarath <greeshnamohan001@gmail.com>
        \nSupervised by Zendalona(2022-2024)""")
        
        about_dialog.set_website("https://www.zendalona.com/maths-tutor")
        about_dialog.set_authors(["Roopasree A P", "Greeshna Sarath"])
        about_dialog.set_documenters(["Roopasree A P", "Greeshna Sarath"])
        about_dialog.set_artists(["Nalin Sathyan" ,"Dr. Saritha Namboodiri",
         "K. Sathyaseelan", "Mukundhan Annamalai", "Ajayakumar A", "Subha I N",
         "Bhavya P V", "Abhirami T", "Ajay Kumar M", "Saheed Aslam M", "Dr. Rajakrishnan V. K.",
          "Girish KK","Suresh S"])
        
        about_dialog.run()
        about_dialog.destroy()
    
    
    def on_help_clicked(self, button):
        url = global_var.user_guide_file_path
        try:
            webbrowser.get("firefox").open(url, new=2)
        except webbrowser.Error:
            webbrowser.open(url, new=2)

    def on_quit_clicked(self, widget):
        self.pref.speech_rate = self.speech.get_speech_rate()
        self.pref.save_preferences_to_file(global_var.user_preferences_file_path)
        self.speech.close()
        self.game_bin.on_quit()
        Gtk.main_quit()


if __name__ == "__main__":
    win = SelectGame()
