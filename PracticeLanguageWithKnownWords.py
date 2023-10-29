import time
import tkinter as tk
import re
import tkinter.filedialog
import os
import glob
import math
import vlc
import random
from googletrans import Translator
from moviepy.editor import VideoFileClip
# End timings of clips needs flixing as well as being able to close them.
# Will soon work on Anki export function - Does not like you clicking on unknown word list.



KNOWN_WORDS_FILE_NAME = 'known_words.txt'
ALL_WORDS_FILE_NAME = 'all_words.txt'
AVAILABLE_WORDS_FILE_NAME = 'available_words.txt'

audio_subtitle_ending = ".essub.txt"

all_known_spanish_words=[]

def play_item_in_vlc(filepath):
    Start_Time_Minutes = 2
    End_Time_Minutes = 3

    # Create a VLC instance
    vlc_instance = vlc.Instance()

    # Create a media player
    player = vlc_instance.media_player_new()

    # Replace 'FULL Family Saga Summer 23.mp4' with the path to your media file
    media = vlc_instance.media_new(filepath)

    # Set the media to the player
    player.set_media(media)

    time.sleep(1)

    # Play the media
    player.play()

    # Set the start time (in milliseconds)
    start_time = Start_Time_Minutes * 60 * 1000  # 2 minutes in milliseconds

    # Set the player's position to the start time
    player.set_time(start_time)

    # Calculate the end time (e.g., 5 minutes in milliseconds)
    end_time = End_Time_Minutes  * 60 * 1000  # 5 minutes after the start time

    # Wait until the video reaches the end time
    while True:
        if player.get_state() == vlc.State.Ended or player.get_time() >= end_time:
            break
            time.sleep(1)

            # Stop the player
            player.stop()

            # Release the player and instance
            player.release()
            vlc_instance.release()

def play_clip_in_vlc(filepath,start_time_string,end_time_string):
    if filepath[-4:] == ".srt":
        #find and use the video files
        video_file_path_options = glob.glob(os.path.join(lbl_video_folder_path.cget("text"), filepath[:-7] + ".*"))
        print(video_file_path_options)
        allowed_extensions = [".mp4"]
        for path in video_file_path_options:
            for extensions in allowed_extensions:
                if path[-4:] == extensions:
                    filepath = path
    elif filepath[-4:] == ".mp4":
        print("fine")
    else:
        print("problem: " + filepath)
        return "NOPE"

    if filepath[-4:] != ".mp4":
        return "NOPE"
    Start_Time_Seconds = int(start_time_string[0:2])*3600 + int(start_time_string[3:5])*60 + int(start_time_string[6:8])
    End_Time_Seconds = int(end_time_string[0:2])*3600 + int(end_time_string[3:5])*60 + int(end_time_string[6:8])

    # Create a VLC instance
    vlc_instance = vlc.Instance()

    # Create a media player
    player = vlc_instance.media_player_new()

    # Replace 'FULL Family Saga Summer 23.mp4' with the path to your media file
    media = vlc_instance.media_new(filepath)

    # Set the start time (in milliseconds)
    start_time = Start_Time_Seconds * 1000

    # Calculate the end time (e.g., 5 minutes in milliseconds)
    end_time = End_Time_Seconds  * 1000

    print(start_time,end_time)

    # Set the media to the player
    player.set_media(media)

    time.sleep(1)

    # Play the media
    player.play()

    time.sleep(1)

    # Set the player's position to the start time
    player.set_time(start_time)

    # Wait until the video reaches the end time
    while True:
        if player.get_state() == vlc.State.Ended or player.get_time() >= end_time:
            time.sleep(1)

            # Stop the player
            player.stop()

            # Release the player and instance
            player.release()
            vlc_instance.release()
            break

def play_full_item_in_vlc(filepath):
    # Create a VLC instance
    vlc_instance = vlc.Instance()

    # Create a media player
    player = vlc_instance.media_player_new()

    # Replace 'FULL Family Saga Summer 23.mp4' with the path to your media file
    media = vlc_instance.media_new(filepath)

    # Set the media to the player
    player.set_media(media)

    time.sleep(1)

    # Play the media
    player.play()

    # Wait until the video reaches the end time
    while True:
        if player.get_state() == vlc.State.Ended:
            break
            time.sleep(1)

            # Stop the player
            player.stop()

            # Release the player and instance
            player.release()
            vlc_instance.release()

def length_finder_given_start_and_end_time(start_time,end_time):
    # Convert both to seconds and convert back
    total_start_time = int(start_time[0:2])*3600 + int(start_time[3:5])*60 + int(start_time[6:8])
    total_end_time = int(end_time[0:2])*3600 + int(end_time[3:5])*60 + int(end_time[6:8])
    clip_length = total_end_time - total_start_time
    clip_length_readable = seconds_to_readable_time(clip_length)
    return clip_length_readable

def translate_spanish_to_english(word):
    translator = Translator()
    translation = translator.translate(word, src='es', dest='en')
    return translation.text

def Anki_Export_FlashCards(filename, Spanish_word_list):
    English_Word_List = []
    Deck_Name = filename + str(random.randint(1,1000))
    FIRST_LINE = "#separator:tab\n" # DO NOT TOUCH
    SECOND_LINE = "#html:true\n" # DO NOT TOUCH
    THIRD_LINE = "#deck column:1\n" # DO NOT TOUCH
    FOURTH_LINE = "#tags column:4\n" # DO NOT TOUCH
    try:
        with open(Deck_Name + ".txt",'w',encoding='utf-8') as write_anki_deck:
            write_anki_deck.write(FIRST_LINE)
            write_anki_deck.write(SECOND_LINE)
            write_anki_deck.write(THIRD_LINE)
            write_anki_deck.write(FOURTH_LINE)
            for Spanish_Word in Spanish_word_list:
                write_anki_deck.write(Deck_Name + "\t" + Spanish_Word + "\t" + translate_spanish_to_english(Spanish_Word) + "\n")

    except FileNotFoundError:
        print(f"No file for known words")
        return

    write_anki_deck.close()



def view_clip_options(filepath,clip_options, clip_starts, clip_finishes, real_filepath, known_words_in_spanish):
    def update_word_listbox(event):
    # Get the selected item from the first listbox
        selected_item = clip_listbox.get(clip_listbox.curselection())

        # print(clip_listbox.curselection()[0])
        ### Extra fluff
        lbl_clip_times.config(text=clip_starts[clip_listbox.curselection()[0]] + " --> " + clip_finishes[clip_listbox.curselection()[0]])
        lbl_clip_length.config(text=length_finder_given_start_and_end_time(clip_starts[clip_listbox.curselection()[0]],clip_finishes[clip_listbox.curselection()[0]]))


        # Clear the second listbox
        words_in_clip_listbox.delete(0, tk.END)
        unknown_words_in_clip_listbox.delete(0,tk.END)
        #words_in_clip_listbox.insert(tk.END,"Name-" + str(random.randint(0,20)))

        WORD_LIST = []
        # Add items to the second listbox based on the selected item
        words = selected_item.split()
        for word in words:
            # Check if the word is in Spanish
            spanish_word_pattern = r'\b[abcdefghijklmnopqrstuvwxyzáéíñóúü]+\b'
            # Use re.search to find the first match in the word
            match_spanish = re.search(spanish_word_pattern, word)
            if match_spanish is not None:
                word = match_spanish.group().lower()
                WORD_LIST.append(word)
        KNOWN_WORDS_LIST = []
        UNKNOWN_WORDS_LIST = []
        for item in WORD_LIST:
            for known_wordy in known_words_in_spanish:
                if  item == known_wordy:
                    KNOWN_WORDS_LIST.append(item)
                    words_in_clip_listbox.insert(tk.END, item)
        lbl_clip_word_number.config(text=str(len(WORD_LIST)))

        # Add unknown words here code
        for item in WORD_LIST:
            ADD = True
            for known_wordso in KNOWN_WORDS_LIST:
                if item == known_wordso:
                    ADD = False
            if ADD == True:
                UNKNOWN_WORDS_LIST.append(item)
        for item in UNKNOWN_WORDS_LIST:
            unknown_words_in_clip_listbox.insert(tk.END,item)

    def grab_unkown_word():
        # Get the total number of items in the Listbox
        num_items = unknown_words_in_clip_listbox.size()

        # Iterate through the items and print each one
        UNKNOWN_WORDS_FOR_ANKI = []
        for i in range(num_items):
            item = unknown_words_in_clip_listbox.get(i)
            UNKNOWN_WORDS_FOR_ANKI.append(item)
        Anki_Export_FlashCards(filepath,UNKNOWN_WORDS_FOR_ANKI)

    def update_time_label(event):
        pass

    def update_length_label(event):
        pass

    def Play_Clip_Without_Subs():
        selected_clip_in_box = clip_listbox.curselection()
        if selected_clip_in_box:
            index = selected_clip_in_box[0]
            clip_subs = clip_listbox.get(index)
            print("No subs for clip: " + clip_subs)
            print(real_filepath,clip_starts[index],clip_finishes[index])
            play_clip_in_vlc(real_filepath,clip_starts[index],clip_finishes[index])

    def Play_Clip_With_Spanish_Subs():
        selected_clip_in_box = clip_listbox.curselection()
        if selected_clip_in_box:
            index = selected_clip_in_box[0]
            clip_subs = clip_listbox.get(index)
            print("Spanish subs for clip: " + clip_subs)

    def Play_Clip_With_English_Subs():
        selected_clip_in_box = clip_listbox.curselection()
        if selected_clip_in_box:
            index = selected_clip_in_box[0]
            clip_subs = clip_listbox.get(index)
            print("English subs for clip: " + clip_subs)

    def Play_Clip_With_Both_Subs():
        selected_clip_in_box = clip_listbox.curselection()
        if selected_clip_in_box:
            index = selected_clip_in_box[0]
            clip_subs = clip_listbox.get(index)
            print("Both subs for clip: " + clip_subs)

    popup_view_clips = tk.Toplevel(window)
    popup_view_clips.title(filepath + "Clips")

    clip_listbox = tk.Listbox(popup_view_clips)
    for clip in clip_options:
        clip_listbox.insert(tk.END, clip)
    clip_listbox.grid(row=0, column=0, rowspan=4, sticky="nsew")

    words_in_clip_listbox = tk.Listbox(popup_view_clips)
    words_in_clip_listbox.grid(row=0, column=1, rowspan=2, sticky="nsew")

    unknown_words_in_clip_listbox = tk.Listbox(popup_view_clips)
    unknown_words_in_clip_listbox.grid(row=2, column=1, rowspan=2, sticky="nsew")

    """
    words_in_clip_listbox = tk.Listbox(popup_view_clips)
    for clip in clip_options:
        words_in_clip_listbox.insert(tk.END, clip)
    words_in_clip_listbox.grid(row=0, column=1, rowspan=4, sticky="nsew")
    """


    btn_clip_play_no_subtitle = tk.Button(popup_view_clips, text="Play clip without subtitles", command=Play_Clip_Without_Subs)
    btn_clip_play_no_subtitle.grid(row=0, column=2)

    btn_clip_play_no_subtitle = tk.Button(popup_view_clips, text="Play clip with Spanish subtitles", command=Play_Clip_With_Spanish_Subs)
    btn_clip_play_no_subtitle.grid(row=1, column=2)

    btn_clip_play_no_subtitle = tk.Button(popup_view_clips, text="Play clip with English subtitles", command=Play_Clip_With_English_Subs)
    btn_clip_play_no_subtitle.grid(row=2, column=2)

    btn_clip_play_no_subtitle = tk.Button(popup_view_clips, text="Play clip with both subtitles", command=Play_Clip_With_Both_Subs)
    btn_clip_play_no_subtitle.grid(row=3, column=2)

    lbl_clip_times = tk.Label(popup_view_clips, text="Time Start --> Time End")
    lbl_clip_times.grid(row=4,column=0)
    btn_unknown_word_export_anki = tk.Button(popup_view_clips, text="Anki Unknown Word Export", command=grab_unkown_word)
    btn_unknown_word_export_anki.grid(row=4,column=1)
    lbl_clip_length = tk.Label(popup_view_clips, text="Length")
    lbl_clip_length.grid(row=5,column=0)
    lbl_clip_word_number = tk.Label(popup_view_clips, text="Words Total")
    lbl_clip_word_number.grid(row=4,column=2)



    clip_listbox.bind("<<ListboxSelect>>", update_word_listbox)



def manage_known_words(available_words_list_displayed, known_words_list_displayed):
    def add_word():
        selected = available_listbox.curselection()
        if selected:
            index = selected[0]
            word = available_listbox.get(index)
            known_words_list_displayed.append(word)
            available_words_list_displayed.remove(word)
            update_lists()

    def remove_word():
        selected = known_listbox.curselection()
        if selected:
            index = selected[0]
            word = known_listbox.get(index)
            available_words_list_displayed.append(word)
            known_words_list_displayed.remove(word)
            update_lists()

    def update_lists():
        available_listbox.delete(0, tk.END)
        known_listbox.delete(0, tk.END)
        for word in available_words_list_displayed:
            available_listbox.insert(tk.END, word)
        for word in known_words_list_displayed:
            known_listbox.insert(tk.END, word)


    popup = tk.Toplevel(window)
    popup.title("Words Management")

    # Create a 2x3 grid to organize the widgets
    for i in range(3):
        popup.grid_rowconfigure(i, weight=1)
        popup.grid_columnconfigure(i, weight=1)

    lbl_available = tk.Label(popup, text="Available words:")
    lbl_available.grid(row=0,column=0)

    lbl_known = tk.Label(popup, text="Known words:")
    lbl_known.grid(row=0,column=2)

    # Create Listbox for "Available Words" in the first column
    available_listbox = tk.Listbox(popup)
    for word in available_words_list_displayed:
        available_listbox.insert(tk.END, word)
    available_listbox.grid(row=1, column=0, rowspan=2, sticky="nsew")

    # Create a Button in the first row, second column
    btn_add_known_word_in_popup = tk.Button(popup, text="Add known", command=add_word)
    btn_add_known_word_in_popup.grid(row=1, column=1, sticky="nsew")

    # Create a Button in the second row, second column
    btn_remove_known_word_in_popup = tk.Button(popup, text="Remove known", command=remove_word)
    btn_remove_known_word_in_popup.grid(row=2, column=1, sticky="nsew")

    # Create Listbox for "Known Words" in the last column
    known_listbox = tk.Listbox(popup)
    for word in known_words_list_displayed:
        known_listbox.insert(tk.END, word)
    known_listbox.grid(row=1, column=2, rowspan=2, sticky="nsew")


def read_all_known_spanish_words():
    SPANISH_WORDS_KNOWN = []

    try:
        with open(KNOWN_WORDS_FILE_NAME, 'r', encoding='utf-8') as read_known_spanish_words_file:
            for line in read_known_spanish_words_file:
                # Remove any leading or trailing whitespace (including newline characters)
                line = line.strip()
                SPANISH_WORDS_KNOWN.append(line)

        #print(SPANISH_WORDS_KNOWN)
        return SPANISH_WORDS_KNOWN
        read_known_spanish_words_file.close()

    except FileNotFoundError:
        print(f"File not found: {KNOWN_WORDS_FILE_NAME}")


def store_all_known_spanish_words(known_spanish_words_list):
    try:
        with open(KNOWN_WORDS_FILE_NAME,'w',encoding='utf-8') as write_known_spanish_words_file:
            sorted_known_spanish_words_list = sorted(known_spanish_words_list)
            for word in known_spanish_words_list:
                write_known_spanish_words_file.write(word+"\n")

    except FileNotFoundError:
        print(f"No file for known words")
        return

    write_known_spanish_words_file.close()

def store_all_spanish_words(spanish_word_list):
    try:
        with open(ALL_WORDS_FILE_NAME,'w',encoding='utf-8') as write_all_spanish_words_file:
            spanish_word_list_sorted=sorted(spanish_word_list)
            for word in spanish_word_list_sorted:
                write_all_spanish_words_file.write(word+"\n")

    except FileNotFoundError:
        print(f"No file for all words")
        return

    write_all_spanish_words_file.close()

def read_all_spanish_words():
    ALL_SPANISH_WORDS = []

    try:
        with open(ALL_WORDS_FILE_NAME, 'r', encoding='utf-8') as read_all_spanish_words_file:
            for line in read_all_spanish_words_file:
                # Remove any leading or trailing whitespace (including newline characters)
                line = line.strip()
                ALL_SPANISH_WORDS.append(line)

        #print(ALL_SPANISH_WORDS)
        return ALL_SPANISH_WORDS
    except FileNotFoundError:
        print(f"File not found: {ALL_WORDS_FILE_NAME}")
        return []

    read_all_spanish_words_file.close()

def save_and_exit(spanish_words_known_list):
    store_all_known_spanish_words(spanish_words_known_list)
    window.destroy()

def get_all_words_from_subtitles_in_folders():
    if (lbl_audio_folder_path.cget("text") != 'path' )|(lbl_video_folder_path.cget("text") != 'path' ) :
        if (lbl_audio_folder_path.cget("text") != 'path' ):
            #Scan for audios in full
            # Create a list of file paths that match the pattern
            #print(lbl_audio_folder_path.cget("text"))
            audio_file_paths = glob.glob(os.path.join(lbl_audio_folder_path.cget("text"), "*.essub.txt"))

            # Iterate through the list of file paths and read and print each line
            for audio_file_path in audio_file_paths:
                """with open(audio_file_path, 'r', encoding='utf-8') as audio_file:
                    print(f"Contents of {audio_file_path}:")
                    for audio_line in audio_file:
                        print(audio_line.strip())  # strip() to remove leading/trailing whitespace
                    print("\n")"""
                scanned_espanol_words = scan_specific_file(audio_file_path)
                existing_espanol_words = read_all_spanish_words()
                for scanned_espanol_word in scanned_espanol_words:
                    ALREADY_IN_LIST = 0 # Good
                    for existing_espanol_word in existing_espanol_words:
                        if scanned_espanol_word == existing_espanol_word:
                            ALREADY_IN_LIST = 1
                    if ALREADY_IN_LIST == 0:
                        existing_espanol_words.append(scanned_espanol_word)
                store_all_spanish_words(existing_espanol_words)




        if (lbl_video_folder_path.cget("text") != 'path' ):
            #Scan SRT files for words in video ##############
            #Scan for audios in full
            # Create a list of file paths that match the pattern
            print(lbl_video_folder_path.cget("text"))
            video_file_paths = glob.glob(os.path.join(lbl_video_folder_path.cget("text"), "*.es.srt"))

            # Iterate through the list of file paths and read and print each line
            for video_file_path in video_file_paths:
                """with open(audio_file_path, 'r', encoding='utf-8') as audio_file:
                    print(f"Contents of {audio_file_path}:")
                    for audio_line in audio_file:
                        print(audio_line.strip())  # strip() to remove leading/trailing whitespace
                    print("\n")"""
                scanned_espanol_words = scan_specific_file(video_file_path)
                existing_espanol_words = read_all_spanish_words()
                for scanned_espanol_word in scanned_espanol_words:
                    ALREADY_IN_LIST = 0 # Good
                    for existing_espanol_word in existing_espanol_words:
                        if scanned_espanol_word == existing_espanol_word:
                            ALREADY_IN_LIST = 1
                    if ALREADY_IN_LIST == 0:
                        existing_espanol_words.append(scanned_espanol_word)
                store_all_spanish_words(existing_espanol_words)

    else:
        print("No folders selected, failed")

def scan_specific_file(file_path):
     # Create an empty list to store Spanish words
    spanish_words = []

    # Open the file and scan for Spanish words
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                words = line.split()
                for word in words:
                    # Check if the word is in Spanish
                    spanish_word_pattern = r'\b[abcdefghijklmnopqrstuvwxyzáéíñóúü]+\b'
                    # Use re.search to find the first match in the word
                    match_spanish = re.search(spanish_word_pattern, word)
                    if match_spanish is not None:
                        word = match_spanish.group().lower()
                        # Check if the word is not already in the list
                        if word not in spanish_words:
                            spanish_words.append(word)

    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    # Print the list of Spanish words
    print("Spanish words found in the file:")
    for word in spanish_words:
        print(word)
    print(len(spanish_words))
    return(spanish_words)

    # Close the file
    file.close()

def is_spanish_word(word):
    # You'll need to implement a way to check if a word is Spanish, such as using a list of Spanish words
    # or a language detection library. For simplicity, we'll assume all words are Spanish in this example.
    return True

def select_folder_audio():
    folder_selected = tk.filedialog.askdirectory()
    lbl_audio_folder_path.config(text = folder_selected)

def select_folder_video():
    folder_selected = tk.filedialog.askdirectory()
    lbl_video_folder_path.config(text = folder_selected)

def scan_srt_files():
    if (lbl_audio_folder_path.cget("text") != 'path' )|(lbl_video_folder_path.cget("text") != 'path' ) :
        print("This works. Will search the SRT files for words now")
    else:
        print("no go, no folders selected.")

def determine_available_words_list(all_words_list, known_words_list):
    available_word_list_return = []
    for word_in_all_word_list in all_words_list:
        AVAILABLE = 1
        for word_known in known_words_list:
            if word_in_all_word_list == word_known:
                AVAILABLE = 0
                break
        if AVAILABLE == 1:
            available_word_list_return.append(word_in_all_word_list)
    return available_word_list_return

def show_both_results(known_words_list):
    audio_results(known_words_list)
    video_results(known_words_list)

def audio_results(known_words_list_audio_results):
    if (lbl_audio_folder_path.cget("text") != 'path' ):
        audio_file_paths = glob.glob(os.path.join(lbl_audio_folder_path.cget("text"), "*.essub.txt"))

        FILE_NUMBER = 0
        # Iterate through all the audios and determine if any of them match the criteria
        for audio_file_path in audio_file_paths:


            scanned_espanol_words = scan_specific_file(audio_file_path)
            known_words_list_audio = known_words_list_audio_results
            TOTAL_DIFFERENT_WORDS = len(scanned_espanol_words)
            KNOWN_WORDS_TOTAL = 0
            for scanned_espanol_word in scanned_espanol_words:
                KNOWN = 0 # Good
                for known_wordos in known_words_list_audio:
                    if known_wordos == scanned_espanol_word:
                        KNOWN = 1
                if KNOWN == 1:
                    KNOWN_WORDS_TOTAL+=1
            Percentage_Known = (KNOWN_WORDS_TOTAL/TOTAL_DIFFERENT_WORDS)*100

            ROW_OF_FILE = math.floor(FILE_NUMBER/4)
            COLUMN_OF_FILE = FILE_NUMBER - math.floor(FILE_NUMBER/4) * 4

            frm_specific_audio_result = tk.Frame(master = frm_audio_results, relief = tk.RIDGE, borderwidth = 10)
            frm_specific_audio_result.grid(row=ROW_OF_FILE,column=COLUMN_OF_FILE,rowspan=3)
            btn_play = tk.Button(master=frm_specific_audio_result,text="Play", command=lambda: play_full_item_in_vlc(audio_file_path[:-10] + ".mp3"))
            btn_play.grid(row=0,column=0)
            lbl_specific_audio_name = tk.Label(master=frm_specific_audio_result,text=audio_file_path[find_index_of_last_slash(audio_file_path):-10])
            lbl_specific_audio_name.grid(row=1,column=0)
            lbl_specific_audio_percentage = tk.Label(master=frm_specific_audio_result,text=str(Percentage_Known) + "%")
            lbl_specific_audio_percentage.grid(row=2,column=0)

            FILE_NUMBER+=1

def find_index_of_last_slash(string):
    if len(string) <= 0:
        return 0
    else:
        index_backslash = 0
        for spot in range(len(string)):
            if string[spot] == "\\":
                index_backslash = spot
        return index_backslash+1



####################################################### My own code


def analyze_srt_file(minimum_percentage_known, srt_filepath, known_words):
    combined_lines = []
    start_times = []
    end_times = []
    subtitle_number = []
    average_percentages = []

    current_lines = []
    current_start_time = ""
    current_end_time = ""
    total_known_words = 0
    total_words = 0

    current_subtitle_number = 0
    previous_subtitle_known_number = 0

    # Read the SRT file
    with open(srt_filepath, 'r', encoding='utf-8') as srt_file:
        for line in srt_file:
            line = line.strip()  # Remove leading/trailing whitespace

            if line.isdigit():
                # This is the subtitle number
                num_sub = int(line)
                if current_lines:
                    # Calculate the percentage of known words
                    percentage_known = (total_known_words / total_words) * 100

                    #print(percentage_known)

                    if percentage_known >= minimum_percentage_known:
                        subtitle_number.append(num_sub)
                        combined_lines.append(" ".join(current_lines))
                        start_times.append(current_start_time)
                        end_times.append(current_end_time)
                        average_percentages.append(percentage_known)

                # Reset for the new subtitle
                current_lines = []
                current_start_time, current_end_time = re.findall(r'(\d{2}:\d{2}:\d{2},\d{3})', next(srt_file))
                total_known_words = 0
                total_words = 0
            else:
                # Split the line into words
                words = line.split()
                total_words += len(words)

                # Count the number of known words
                total_known_words += sum(1 for word in words if word.lower() in known_words)

                current_lines.append(line)

    # Add the last subtitle as a clip
    if current_lines:
        percentage_known = (total_known_words / total_words) * 100
        if percentage_known >= minimum_percentage_known:
            subtitle_number.append(num_sub)
            combined_lines.append(" ".join(current_lines))
            start_times.append(current_start_time)
            end_times.append(current_end_time)
            average_percentages.append(percentage_known)

    #This is where we actually combine them together.
    REAL_COMBINED_LIST = []
    REAL_START_TIMES = []
    REAL_END_TIMES = []
    REAL_PERCENTAGES = []
    Previous_Sub_Number = 0
    sub_number_sets = []
    sub_number_set = []
    for number_of_Sub in subtitle_number:
        if Previous_Sub_Number == number_of_Sub-1:
            sub_number_set.append(number_of_Sub)
            Previous_Sub_Number = number_of_Sub
             #Execute code to combine to new lists
        else:
            if sub_number_set != []:
                sub_number_sets.append(sub_number_set)
            sub_number_set = []
            sub_number_set.append(number_of_Sub)
            Previous_Sub_Number = number_of_Sub

    counter = 0
    for set in sub_number_sets:
        THOSE_WORDS = ""
        average_percentages_sum = 0
        REAL_START_TIMES.append(start_times[counter])
        for item in set:
            THOSE_WORDS += combined_lines[counter] + " - "
            average_percentages_sum += average_percentages[counter]
            counter+=1
        REAL_COMBINED_LIST.append(THOSE_WORDS)
        REAL_END_TIMES.append(end_times[counter])
        REAL_PERCENTAGES.append(average_percentages_sum/len(set))

    print(sub_number_sets)
    #print(combined_lines,start_times,end_times)
    #print(REAL_COMBINED_LIST, REAL_START_TIMES, REAL_END_TIMES, REAL_PERCENTAGES)
    #for craspps in range(len(REAL_COMBINED_LIST)):
    #    print(REAL_COMBINED_LIST[craspps], REAL_START_TIMES[craspps], REAL_END_TIMES[craspps], REAL_PERCENTAGES[craspps])
    return REAL_COMBINED_LIST, REAL_START_TIMES, REAL_END_TIMES, REAL_PERCENTAGES

#########################################################

def find_percentage_of_line(line,known_words_list_func):
    words = line.split()
    total_words = len(words)
    known_words_in_line = 0
    for word in words:
        for known_word in known_words_list_func:
            if word == known_word:
                known_words_in_line += 1
    POL = (known_words_in_line/total_words) * 100
    return POL

def find_length_of_video(sub_file_path):
    video_file_path_options = glob.glob(os.path.join(lbl_video_folder_path.cget("text"), sub_file_path[:-7] + ".*"))
    print(video_file_path_options)
    allowed_extensions = [".mp4"]
    for path in video_file_path_options:
        for extensions in allowed_extensions:
            if path[-4:] == extensions:
                try:
                    video_clip = VideoFileClip(path)
                    duration = video_clip.duration
                    #print(seconds_to_readable_time(duration))
                    video_clip.reader.close()
                    return seconds_to_readable_time(duration)
                except Exception as e:
                    print(f"Error: {e}")
                    return None

def video_results(known_words_list_video_results):
    if (lbl_video_folder_path.cget("text") != 'path' ):
        video_file_paths_whole = glob.glob(os.path.join(lbl_video_folder_path.cget("text"), "*.essub.txt"))
        video_file_paths_srt = glob.glob(os.path.join(lbl_video_folder_path.cget("text"), "*.es.srt"))

        FILE_NUMBER = 0

        # Whole videos analysed and bought back
        if ((video_file_paths_whole != None) and (video_file_paths_whole != [])):
            pass

        # SRT files, these should load a popup to give all the options for what part of the video/movie to watch and with/without subtitles.
        if ((video_file_paths_srt != None) and (video_file_paths_srt != [])):
            for vfp in video_file_paths_srt:
                print("film 1: " + vfp)
                # Start of each film/video

                ### Analyse the video
                TheSelectedClips = (analyze_srt_file(scl_percentage_known.get(),vfp,known_words_list_video_results))[0]
                Start_TheSelectedClips = (analyze_srt_file(scl_percentage_known.get(),vfp,known_words_list_video_results))[1]
                End_TheSelectedClips = (analyze_srt_file(scl_percentage_known.get(),vfp,known_words_list_video_results))[2]


                ##### Create the 4 columns of buttons for the videos
                ROW_OF_FILE = math.floor(FILE_NUMBER/4)
                COLUMN_OF_FILE = FILE_NUMBER - math.floor(FILE_NUMBER/4) * 4

                frm_specific_video_result = tk.Frame(master = frm_video_results, relief = tk.RIDGE, borderwidth = 10)
                frm_specific_video_result.grid(row=ROW_OF_FILE,column=COLUMN_OF_FILE,rowspan=3)
                btn_play = tk.Button(master=frm_specific_video_result,text=vfp[find_index_of_last_slash(vfp):-7], command=lambda: view_clip_options(vfp[find_index_of_last_slash(vfp):-7],TheSelectedClips, Start_TheSelectedClips, End_TheSelectedClips,vfp, known_words_list_video_results))
                btn_play.grid(row=0,column=0)
                find_length_of_video(vfp)
                lbl_specific_video_name = tk.Label(master=frm_specific_video_result,text=find_length_of_video(vfp))
                lbl_specific_video_name.grid(row=1,column=0)
                lbl_specific_clips = tk.Label(master=frm_specific_video_result,text="Clips: " + str(len(TheSelectedClips)))
                lbl_specific_clips.grid(row=2,column=0)

                FILE_NUMBER +=1

def seconds_to_readable_time(seconds):
    hours = math.floor(seconds/3600)
    minutes = math.floor((seconds-hours*3600)/60)
    seconds1 = math.floor(seconds - hours*3600 - minutes*60)
    formatted_time = f'{hours:02}:{minutes:02}:{seconds1:02}'
    return formatted_time

window = tk.Tk()
window.title("Practice a Language with Known Words")
all_known_spanish_words = read_all_known_spanish_words()

frm_settings = tk.Frame(master = window, relief = tk.RIDGE, borderwidth = 10)
window.columnconfigure(0, weight=1, minsize=150)
window.rowconfigure(0, weight=1, minsize=350)
frm_settings.grid(row=0,column=0)

frm_words_vocab = tk.Frame(master = window, relief = tk.RIDGE, borderwidth = 10)
window.columnconfigure(0, weight=1, minsize=150)
window.rowconfigure(1, weight=1, minsize=150)
frm_words_vocab.grid(row=1, column=0)

frm_results = tk.Frame(master = window, relief = tk.RIDGE, borderwidth = 10)
window.columnconfigure(1, weight=1, minsize=650)
window.rowconfigure(0, weight=1, minsize=500)
frm_results.grid(row=0,column=1, rowspan=2)


lbl_name = tk.Label(master=frm_settings,text="Practice Language with Known Words")
lbl_name.pack()
lbl_settings = tk.Label(master=frm_settings,text="Settings")
lbl_settings.pack()
lbl_percentage_words_known = tk.Label(master=frm_settings,text="Percentage of words known minimum:")
lbl_percentage_words_known.pack()
scl_percentage_known = tk.Scale(frm_settings, from_=0, to=100, orient=tk.HORIZONTAL)
scl_percentage_known.pack()
scl_percentage_known.set(100)

frm_number_of_words_in_settings = tk.Label(master=frm_settings,borderwidth=5)
frm_number_of_words_in_settings.pack()
lbl_word_range = tk.Label(master=frm_number_of_words_in_settings,text="Word range:")
lbl_word_range.grid(row=0,column=0)
ent_word_range_min = tk.Entry(master=frm_number_of_words_in_settings)
ent_word_range_min.grid(row=0,column=1)
ent_word_range_min.insert(0,"0")
lbl_word_range_to = tk.Label(master=frm_number_of_words_in_settings,text=" to ")
lbl_word_range_to.grid(row=0,column=2)
ent_word_range_max = tk.Entry(master=frm_number_of_words_in_settings)
ent_word_range_max.grid(row=0,column=3)
ent_word_range_max.insert(0,"0")

frm_length_of_practice_audio_clip_in_settings = tk.Label(master=frm_settings,borderwidth=5)
frm_length_of_practice_audio_clip_in_settings.pack()
lbl_length_range = tk.Label(master=frm_length_of_practice_audio_clip_in_settings,text="Word range:")
lbl_length_range.grid(row=0,column=0)
ent_length_range_min = tk.Entry(master=frm_length_of_practice_audio_clip_in_settings)
ent_length_range_min.grid(row=0,column=1)
ent_length_range_min.insert(0,"0")
lbl_word_range_to = tk.Label(master=frm_length_of_practice_audio_clip_in_settings,text=" to ")
lbl_word_range_to.grid(row=0,column=2)
ent_length_range_max = tk.Entry(master=frm_length_of_practice_audio_clip_in_settings)
ent_length_range_max.grid(row=0,column=3)
ent_length_range_max.insert(0,"0")

frm_audio_folder_in_settings = tk.Label(master=frm_settings,borderwidth=5)
frm_audio_folder_in_settings.pack()
lbl_audio_folder = tk.Label(master=frm_audio_folder_in_settings,text="Audio folder:")
lbl_audio_folder.grid(row=0,column=0)
btn_audio_folder = tk.Button(master=frm_audio_folder_in_settings,text="Choose Folder", command=select_folder_audio)
btn_audio_folder.grid(row=0,column=1)
lbl_audio_folder_path = tk.Label(master=frm_audio_folder_in_settings,text="path")
lbl_audio_folder_path.grid(row=0,column=2)

frm__video_folder_in_settings = tk.Label(master=frm_settings,borderwidth=5)
frm__video_folder_in_settings.pack()
lbl_video_folder = tk.Label(master=frm__video_folder_in_settings,text="Video folder:")
lbl_video_folder.grid(row=0,column=0)
btn_video_folder = tk.Button(master=frm__video_folder_in_settings,text="Choose Folder", command=select_folder_video)
btn_video_folder.grid(row=0,column=1)
lbl_video_folder_path = tk.Label(master=frm__video_folder_in_settings,text="path")
lbl_video_folder_path.grid(row=0,column=2)

btn_refresh = tk.Button(master=frm_settings,text="Submit and Refresh", command=lambda: show_both_results(all_known_spanish_words))
btn_refresh.pack()


available_words_list=determine_available_words_list(read_all_spanish_words(),all_known_spanish_words)


lbl_words_vocab = tk.Label(master=frm_words_vocab,text="Words/Vocabulary Known")
lbl_words_vocab.pack()
frm_add_word = tk.Label(master=frm_words_vocab,borderwidth=5)
frm_add_word.pack()
ent_word_known = tk.Entry(master=frm_add_word)
ent_word_known.grid(row=0,column=0)
btn_add_words = tk.Button(master=frm_add_word,text="Add word")
btn_add_words.grid(row=0,column=1)
btn_manage_words = tk.Button(master=frm_words_vocab,text="Manage words", command =lambda: manage_known_words(available_words_list,all_known_spanish_words))
btn_manage_words.pack()
btn_scan_for_words = tk.Button(master=frm_words_vocab,text="Scan for words",command=get_all_words_from_subtitles_in_folders)
btn_scan_for_words.pack()
btn_TEST = tk.Button(master=frm_words_vocab,text="Test",command= lambda: scan_specific_file("C:/Users/bohda/OneDrive/Documents/Revise and Learn Language with Known Words Project/Audio/5 ideas para mejorar tu pronunciación.essub.txt"))
btn_TEST.pack()
btn_save_and_exit = tk.Button(master=frm_words_vocab,text="Save and Exit",command= lambda: save_and_exit(all_known_spanish_words))
btn_save_and_exit.pack()





lbl_results = tk.Label(master=frm_results,text="Results")
lbl_results.grid(row=0,column=0)

frm_audio_results = tk.Frame(master = frm_results, relief = tk.RIDGE, borderwidth = 10)
frm_audio_results.grid(row=1,column=0, columnspan=3)
lbl_audio_results = tk.Label(master=frm_audio_results,text="Audios")
lbl_audio_results.grid(row=0, column=0)

frm_video_results = tk.Frame(master = frm_results, relief = tk.RIDGE, borderwidth = 10)
frm_video_results.grid(row=4,column=0, columnspan = 3)
lbl_video_results = tk.Label(master=frm_video_results,text="Videos")
lbl_video_results.grid(row=0, column=0)
"""

frm_audio_results = tk.Frame(master = frm_results, relief = tk.RIDGE, borderwidth = 10)
frm_audio_results.grid(row=0,column=0)
lbl_audio_results = tk.Label(master=frm_audio_results,text="Audios")
lbl_audio_results.grid(row=0, column=0)
"""
read_all_known_spanish_words()
window.mainloop()
