import urllib
import wave
import json
import os
import sys
import threading
import time
import errno
import argparse
import shutil
import atexit
from tensorflow import keras
import ffmpeg
import soundfile
from urllib import request, parse
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource 
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from IPython.display import Audio
from shazamio import Shazam
import time
from time import sleep
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
from tkinter import ttk
from lyrics_extractor import SongLyrics
from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
from lyricsgenius import Genius
import asyncio
async def recognise(name):
    out = await Shazam().recognize_song(name)
    try:
        genius =Genius("yDdB1P2dxTHeaNM1V350gGmV9fCQslK5CQ4O87W8bd - GCAE83QMsAO0MZwnq9PWn")
        print("this is the song")
        # print(out['track']['title'])
        print(out)
        for test in out['track']['sections']:
            print(test)
        print(out['track']['sections'][1]['text'])
        song = genius.search_song(out['track']['title'],out['track']['subtitle'])
        # print(out['track']['title'])
        # print(out["urlparams"]["{trackartist}"])
        artist = genius.search_artist(out['track']['subtitle'])
        artist.save_lyrics()
    except:
        print("no song")
        return False
    return True
root = tk.Tk()
root.withdraw()

global deletetracks
inputapikey = ""
inputurl = ""
deletetracks = False
#gbvsxz mygtdcxdtygxxctk.messagebox.showinfo('Welcome To Clean Song Generator','Welcome, Please pick a .wav file and have Audacity open. This process will take a few minutes')

file_path = "C:/Users/trebr/AppData/Local/Programs/Python/Python39/CleanSong/Clean-Song-Generator/test.mp3"

asyncio.get_event_loop().run_until_complete(recognise(file_path))
# file_path = filedialog.askopenfilename( title='Choose Your WAV', filetypes=
#     (("wav files", "*.wav"), ("all files", "*.*")))
def sel():
    global deletetracks
    temp = not deletetracks
    deletetracks = temp


# root= tk.Tk()
#
# canvas1 = tk.Canvas(root, width = 400, height = 300,  relief = 'raised')
# canvas1.pack()
#
# label1 = tk.Label(root, text='Put In your Watson IBM Info/Settings')
# label1.config(font=('helvetica', 14))
# canvas1.create_window(200, 25, window=label1)
#
#
# entry1 = tk.Entry (root)
# canvas1.create_window(200, 60, window=entry1)
#
# label3 = tk.Label(root, text='Put in your apikey:')
# label3.config(font=('helvetica', 10))
# canvas1.create_window(200, 45, window=label3)
#
#
#
# label2 = tk.Label(root, text='Put in your url:')
# label2.config(font=('helvetica', 10))
# canvas1.create_window(200, 80, window=label2)
#


# entry2 = tk.Entry (root)
# canvas1.create_window(200, 100, window=entry2)
#
# isitchecked = tk.BooleanVar()
# check = tk.Checkbutton(root, text="Delete audacity tracks after finishing", variable=isitchecked, command=sel)
#
# canvas1.create_window(200, 120, window=check)
# def getSquareRoot ():
#
#     inputapikey = entry1.get()
#     inputurl = entry2.get()
#     root.destroy()
#     root.quit()

# button1 = tk.Button(root,text='Press when done', command=getSquareRoot, bg='brown', fg='white', font=('helvetica', 9, 'bold'))
# canvas1.create_window(200, 280, window=button1)
# root.mainloop()

start_time = time.time()
all_paths = os.path.split(file_path)
PATH = all_paths[0]
os.chdir(PATH)

INFILE = all_paths[len(all_paths)-1]

INFOLDER =  INFILE[0:INFILE.find(".")]
in_dir = file_path[0:file_path.find(".")]

out_dir = os.path.join(os.getcwd(),INFILE)
#INFILE = "testfile.wav"


# Using embedded configuration.

start = [f.path for f in os.scandir(PATH) if f.is_dir()]

# separator = Separator('2stem.json', multiprocess=False)
# print(out_dir)
# print(PATH)
# prediction = separator.separate_to_file(out_dir, PATH)
# time.sleep(0.1)
#
#
# end =[f.path for f in os.scandir(PATH) if f.is_dir()]
#
#
# list_difference = [item for item in end if item not in start]
#
# in_dir = list(set(end) - set(start))[0]
#
#
# new_dir = os.path.split(in_dir)
# INFOLDER = new_dir[1]
# os.rename(new_dir[1], 'temp')
#
# in_dir = os.path.join(new_dir[0],'temp')
#
# vocals = os.path.join(in_dir,"vocals.wav")
#
# accompaniment = os.path.join(in_dir,"accompaniment.wav")
# if inputapikey == "" or inputurl == "":
#
#     apikey = 'eXlBfMVRL8qjdkUO7MZBTj9x44Mli-m2fv_aXvyuXC5G'
#     url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/74608ed7-0fb6-42d7-8436-c2147b518cc6'
# else:
#     apikey = inputapikey
#     url = inputurl
#
#
# # Platform specific file name and file path.
# # PATH is the location of files to be imported / exported.
#
#
# authenticator = IAMAuthenticator(apikey)
# stt = SpeechToTextV1(authenticator=authenticator)
# stt.set_service_url(url)
#
# mytimestamps = []
#
# finaltimestamps = []
# with open(vocals, 'rb') as f:
#     res = stt.recognize(audio=f, content_type='audio/wav', model='en-US_Telephony',timestamps = True ).get_result()
#
# for temp in res['results']:
#
#     for alts in temp['alternatives']:
#         for times in alts['timestamps']:
#             print(times)
#             if  "*" in  times[0]:
#
#                 mytimestamps.append(times)
#
# print(mytimestamps)
# #PATH = './'


# # Platform specific constants
# if sys.platform == 'win32':
#     print("recording-test.py, running on windows")
#     PIPE_TO_AUDACITY = '\\\\.\\pipe\\ToSrvPipe'
#     PIPE_FROM_AUDACITY = '\\\\.\\pipe\\FromSrvPipe'
#     EOL = '\r\n\0'
# else:
#     print("recording-test.py, running on linux or mac")
#     PIPE_TO_AUDACITY = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
#     PIPE_FROM_AUDACITY = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
#     EOL = '\n'
#
#
# print("Write to  \"" + PIPE_TO_AUDACITY +"\"")
# if not os.path.exists(PIPE_TO_AUDACITY):
#     print(""" ..does not exist.
#     Ensure Audacity is running with mod-script-pipe.""")
#     sys.exit()
#
# print("Read from \"" + PIPE_FROM_AUDACITY +"\"")
# if not os.path.exists(PIPE_FROM_AUDACITY):
#     print(""" ..does not exist.
#     Ensure Audacity is running with mod-script-pipe.""")
#     sys.exit()
#
# print("-- Both pipes exist.  Good.")
#
# TOPIPE = open(PIPE_TO_AUDACITY, 'w')
#
# FROMPIPE = open(PIPE_FROM_AUDACITY, 'r')
#
#
#
#
# def send_command(command):
#     """Send a command to Audacity."""
#     TOPIPE.write(command + EOL)
#     TOPIPE.flush()
#
#
# def get_response():
#     """Get response from Audacity."""
#     line = FROMPIPE.readline()
#     result = ""
#     while True:
#         result += line
#         line = FROMPIPE.readline()
#
#         if line == '\n':
#             return result
#
#
# def do_command(command):
#     """Do the command. Return the response."""
#     send_command(command)
#     # time.sleep(0.1) # may be required on slow machines
#     response = get_response()
#     return response
#
# def split_delete(start,end):
#     do_command("SelectNone")
#
#     do_command("Select: Start=" +str(start)+" RelativeTo=ProjectStart End="+str(end)+" Track =0")
#     do_command("SplitCut")
#
#
#
#
# def play_record():
#     """Import track and record to new track.
#     Note that a stop command is not required as playback will stop at end of selection.
#     """
#     do_command(f"Import2: Filename={vocals}")
#     do_command(f"Import2: Filename={accompaniment}")
#
#     while len(mytimestamps)>0:
#         temp = mytimestamps.pop(0)
#         finaltimestamps.append([temp[1],temp[2]])
#         split_delete(temp[1],temp[2])
#
#
#
#
#
#
# def export(filename):
#     """Export the new track, and deleted both tracks."""
#     final = filename.replace(" ","_")
#     print(do_command(f"Export2: Filename={os.path.join(PATH,final)} NumChannels=2.0"))
#
#     if deletetracks == 1:
#         do_command("SelectAll")
#         do_command("RemoveTracks")
#
# def do_one_file():
#     """Run test with one input file only."""
#
#     play_record()
#     final_name =INFOLDER.replace(".","") + "-out.wav"
#     export(final_name)
#
#
# # Run the test with "testfile.wav" in the specified PATH.
#
# do_one_file()
# multiple = "word"
#
# if len(finaltimestamps)>1:
#     multiple = "words"
# elif len(finaltimestamps) == 0:
#     multiple = "no words"
#
#
#
# def cleanup_directories():
#     dir_path = in_dir
#
#     try:
#         shutil.rmtree(dir_path)
#     except OSError as e:
#         print("Error: %s : %s" % (dir_path, e.strerror))
#
#
# cleanup_directories()
# print( "My program took "+ str(time.time() - start_time)+ " to run")
# alltimestamps = ""
# for temp in finaltimestamps:
#     alltimestamps = alltimestamps + "["+str(temp[0]) +", " +str(temp[1]) + "] "
#
#
# finaltext = 'Song Cleaning finished. Removed '+multiple +' at : '+ alltimestamps
# finaltitle = 'Program Finished. It took : '+ str(time.time() - start_time)+ "to run"
# tk.messagebox.showinfo(finaltitle,finaltext)

#atexit.register(cleanup_directories)















    

