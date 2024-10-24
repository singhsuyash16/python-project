# Importing all the necessary modules
from tkinter import *
from tkinter import filedialog, messagebox
import pygame.mixer as mixer  # pip install pygame
import os
# Initializing the mixer
mixer.init()
# Play, Stop, Load, Pause, Resume, and Next functions
def play_song(song_name: StringVar, songs_list: Listbox, status: StringVar):
    try:
        selected_song = songs_list.get(ACTIVE)
        if selected_song:
            song_name.set(selected_song)
            mixer.music.load(selected_song)
            mixer.music.play()
            status.set("Song PLAYING")
        else:
            status.set("No song selected")
    except Exception as e:
        messagebox.showerror("Error", f"Error playing song: {e}")

def stop_song(status: StringVar):
    mixer.music.stop()
    status.set("Song STOPPED")

def load(listbox):
    directory = filedialog.askdirectory(title='Open a songs directory')
    if directory:
        os.chdir(directory)
        tracks = [track for track in os.listdir() if track.endswith(('.mp3', '.wav', '.ogg'))]
        listbox.delete(0, END)  # Clear the current list
        for track in tracks:
            listbox.insert(END, track)

def pause_song(status: StringVar):
    mixer.music.pause()
    status.set("Song PAUSED")

def resume_song(status: StringVar):
    mixer.music.unpause()
    status.set("Song RESUMED")

def next_song(songs_list: Listbox, song_name: StringVar, status: StringVar):
    try:
        next_index = (songs_list.curselection()[0] + 1) % songs_list.size()
        songs_list.select_clear(0, END)  # Clear current selection
        songs_list.select_set(next_index)  # Select next song
        play_song(song_name, songs_list, status)
    except IndexError:
        status.set("No more songs in the playlist")
# Creating the master GUI
root = Tk()
root.geometry('700x220')
root.title('Music Player')
root.resizable(0, 0)
# All the frames
song_frame = LabelFrame(root, text='Current Song', bg='black', width=400, height=80)
song_frame.place(x=0, y=0)

button_frame = LabelFrame(root, text='Control Buttons', bg='black', width=400, height=120)
button_frame.place(y=80)

listbox_frame = LabelFrame(root, text='Playlist', bg='white')
listbox_frame.place(x=400, y=0, height=200, width=300)
# All StringVar variables
current_song = StringVar(root, value='<Not selected>')
song_status = StringVar(root, value='<Not Available>')


playlist = Listbox(listbox_frame, font=('Helvetica', 11), selectbackground='lightblue')
playlist.pack(fill=BOTH, expand=True, padx=5, pady=5)
# SongFrame Labels
Label(song_frame, text='CURRENTLY PLAYING:', bg='Red', font=('Times', 10, 'bold')).place(x=5, y=20)

song_lbl = Label(song_frame, textvariable=current_song, bg='Goldenrod', font=("Times", 12), width=25)
song_lbl.place(x=150, y=20)
# Control Buttons
pause_btn = Button(button_frame, text='Pause', bg='yellow', font=("Georgia", 13), width=7,
                   command=lambda: pause_song(song_status))
pause_btn.place(x=15, y=10)

next_btn = Button(button_frame, text='Next', bg='red', font=("Georgia", 13), width=7,
                  command=lambda: next_song(playlist, current_song, song_status))
next_btn.place(x=105, y=10)

play_btn = Button(button_frame, text='Play', bg='green', font=("Georgia", 13), width=7,
                  command=lambda: play_song(current_song, playlist, song_status))
play_btn.place(x=195, y=10)

resume_btn = Button(button_frame, text='Resume', bg='Orange', font=("Georgia", 13), width=7,
                    command=lambda: resume_song(song_status))
resume_btn.place(x=285, y=10)

load_btn = Button(button_frame, text='Load Directory', bg='hotpink', font=("Georgia", 13), width=35,
                  command=lambda: load(playlist))
load_btn.place(x=10, y=55)
# Label at the bottom that displays the state of the music
Label(root, textvariable=song_status, bg='black', font=('Times', 9), justify=LEFT).pack(side=BOTTOM, fill=X)
# Finalizing the GUI
root.update()
root.mainloop()