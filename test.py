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

from spleeter.separator import Separator
from spleeter.audio.adapter import AudioAdapter
async def recognise(name):
    out = await Shazam().recognize_song(name)
    try:
        print("this is the song")
        print(out['track']['title'])
    except:
        print("no song")
        return False
    return True

apikey = 'eXlBfMVRL8qjdkUO7MZBTj9x44Mli-m2fv_aXvyuXC5G'
url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/74608ed7-0fb6-42d7-8436-c2147b518cc6'
