import os
import sys
from shazamio import Shazam
import time
from better_profanity import profanity
import whisper
from time import sleep
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
from tkinter import ttk
from spleeter.separator import Separator
import asyncio
from difflib import SequenceMatcher
from pydub import AudioSegment
import shutil
import patoolib
import json

#Note this will not install unless your Visual Studio is set up with cmake
from lhotse import CutSet, RecordingSet, align_with_torchaudio, annotate_with_whisper, Recording
from tqdm import tqdm


def sort_key(company):
    return company[1]


async def recognise(name):
    out = await Shazam().recognize_song(name)
    try:
        return out['track']['sections'][1]['text']
    except:
        return None

def censor(file_path, useshazam,useaudacity,deleteaudacity) :
    root = tk.Tk()
    root.withdraw()

    print("Started Censoring")
    if useshazam:
        shazamresult = asyncio.get_event_loop().run_until_complete(recognise(file_path))

    start_time = time.time()
    all_paths = os.path.split(file_path)
    PATH = all_paths[0]
    os.chdir(PATH)
    print("Started Seperating, this may take a while")
    INFILE = all_paths[len(all_paths)-1]

    INFOLDER =  INFILE[0:INFILE.find(".")]
    in_dir = file_path[0:file_path.find(".")]

    out_dir = os.path.join(os.getcwd(),INFILE)

    # Using embedded configuration.
    start = [f.path for f in os.scandir(PATH) if f.is_dir()]

    separator = Separator('2stem.json', multiprocess=False)

    prediction = separator.separate_to_file(out_dir, PATH)
    time.sleep(0.1)


    end =[f.path for f in os.scandir(PATH) if f.is_dir()]


    in_dir = list(set(end) - set(start))[0]

    if os.path.isdir('./temp'):
        shutil.rmtree('./temp')
    new_dir = os.path.split(in_dir)
    INFOLDER = new_dir[1]
    os.rename(new_dir[1], 'temp')

    in_dir = os.path.join(new_dir[0],'temp')

    vocals = os.path.join(in_dir,"vocals.wav")

    accompaniment = os.path.join(in_dir,"accompaniment.wav")

    sound = AudioSegment.from_mp3(file_path)
    sound = sound.set_channels(1)
    sound.export("result.mp3", format="mp3")
    recordings = RecordingSet.from_recordings([Recording.from_file(path=file_path)])
    cuts = annotate_with_whisper(recordings,model_name='large')
    cuts_aligned = align_with_torchaudio(cuts)
    with CutSet.open_writer("cuts.jsonl.gz") as writer:
        for cut in tqdm(cuts_aligned, desc="Progress"):
            writer.write(cut)
    patoolib.extract_archive("cuts.jsonl.gz", outdir=".")
    os.remove("cuts.jsonl.gz")
    fObj = open('cuts.jsonl',)
    mytimestamps = []
    ogdata = json.load(fObj)
    alltimestamps = []
    fullstatementnormal = ""
    fullstatementtimestamps = []
    print("Finished Seperating")
    print("Findining Timestamps")
    for supervision in ogdata['supervisions']:
        try:
            fullstatementnormal = fullstatementnormal + supervision['text'] + " "
            #print(supervision['text'])
            for word in supervision['alignment']['word']:
                fullstatementtimestamps.append([word[1], word[1] + word[2]])
                if profanity.contains_profanity(word[0]):
                    mytimestamps.append([word[0],word[1],word[2],supervision['text'],supervision['alignment']['word']])
                alltimestamps.append([word[0], word[1], word[1] + word[2], supervision['text'], supervision['alignment']['word']])
        except:
            print("no alignment")

    print("Finished Findining Timestamps")
    if useshazam and not shazamresult is None:
        print("Started Shazam Processing")
        timestampstoappend = []
        fullstatementshazam = ""
        swears = []
        for phrase in shazamresult:
            fullstatementshazam = fullstatementshazam + phrase + " "
            if "*" in profanity.censor(phrase):
                swears.append(phrase)

        for swear in swears:
            for val in alltimestamps:
                if SequenceMatcher(None, val[3], swear).ratio() > .85:
                    for timestamp in mytimestamps:
                        if timestamp[3] == val[3] and timestamp[1] == val[1]:
                            intimestamp = True
                            break
                    if timestamp:
                        continue
                    else:
                        if len(timestamp[3].split(" ")) == len(val[3].split(" ")) or len(timestamp[3].split(" ")) > len(val[3].split(" ")):
                            index = 0
                            for word in val[3].split(" "):

                                if "*" in profanity.censor(word):
                                    word = timestamp[4][index]
                                    timestampstoappend.append([word[0], word[1], word[1] + word[2]])
                                index = index + 1
                        else:
                            sizetimestamp = len(timestamp[3].split(" "))
                            index = 0
                            for word in val[3].split(" "):

                                if "*" in profanity.censor(word):
                                    word = timestamp[4][index]
                                    timestampstoappend.append([word[0], word[1], word[1] + word[2]])
                                index = index + 1
                                if index>=sizetimestamp:
                                    timestampstoappend.append([word[0], word[1], word[1] + word[2]])
                                    break
        mytimestamps= mytimestamps + timestampstoappend
        mytimestamps.sort(key=sort_key, reverse=False)
        print("Finished Shazam Processing")

    vocalssound = AudioSegment.from_file(vocals, format="wav")
    accompanimentsound = AudioSegment.from_file(accompaniment, format="wav")
    finalresult = None
    index = 0
    prevtimestamp = 0
    print("Creating Final File")
    for timestamp in mytimestamps:
        if index ==0:
            finalresult = vocalssound[prevtimestamp:timestamp[1] * 1000]
        else:
            finalresult = finalresult +vocalssound[prevtimestamp:timestamp[1]*1000]
        audiosnippet = vocalssound[timestamp[1]*1000:(timestamp[1]+timestamp[2])*1000]
        audiosnippet = audiosnippet -100
        finalresult = finalresult +audiosnippet
        prevtimestamp = (timestamp[1]+timestamp[2])*1000
        if index == len(mytimestamps)-1:
            finalresult = finalresult + vocalssound[(timestamp[1]+timestamp[2])*1000:]
        index = index +1

    if finalresult is None:
        finalresult = vocalssound
    finalresult.export("justvocals.mp3",format="mp3")
    overlay = finalresult.overlay(accompanimentsound, position=0)
    overlay.export("CompletedResult.mp3",format="mp3")
    print("Finished Creating Final File Titled CompletedResult")

    finaltimestamps = []
    # Platform specific constants
    if useaudacity:
        print("Entering Audacity")
        if sys.platform == 'win32':
            print("recording-test.py, running on windows")
            PIPE_TO_AUDACITY = '\\\\.\\pipe\\ToSrvPipe'
            PIPE_FROM_AUDACITY = '\\\\.\\pipe\\FromSrvPipe'
            EOL = '\r\n\0'
        else:
            print("recording-test.py, running on linux or mac")
            PIPE_TO_AUDACITY = '/tmp/audacity_script_pipe.to.' + str(os.getuid())
            PIPE_FROM_AUDACITY = '/tmp/audacity_script_pipe.from.' + str(os.getuid())
            EOL = '\n'


        print("Write to  \"" + PIPE_TO_AUDACITY +"\"")
        if not os.path.exists(PIPE_TO_AUDACITY):
            print(""" ..does not exist.
            Ensure Audacity is running with mod-script-pipe.""")
            sys.exit()

        print("Read from \"" + PIPE_FROM_AUDACITY +"\"")
        if not os.path.exists(PIPE_FROM_AUDACITY):
            print(""" ..does not exist.
            Ensure Audacity is running with mod-script-pipe.""")
            sys.exit()

        print("-- Both pipes exist.  Good.")

        TOPIPE = open(PIPE_TO_AUDACITY, 'w')

        FROMPIPE = open(PIPE_FROM_AUDACITY, 'r')




        def send_command(command):
            """Send a command to Audacity."""
            TOPIPE.write(command + EOL)
            TOPIPE.flush()


        def get_response():
            """Get response from Audacity."""
            line = FROMPIPE.readline()
            result = ""
            while True:
                result += line
                line = FROMPIPE.readline()

                if line == '\n':
                    return result


        def do_command(command):
            """Do the command. Return the response."""
            send_command(command)
            # time.sleep(0.1) # may be required on slow machines
            response = get_response()
            return response

        def split_delete(start,end):
            do_command("SelectNone")

            do_command("Select: Start=" +str(start)+" RelativeTo=ProjectStart End="+str(end)+" Track =0")
            do_command("SplitCut")




        def play_record():
            """Import track and record to new track.
            Note that a stop command is not required as playback will stop at end of selection.
            """
            do_command(f"Import2: Filename={vocals}")
            do_command(f"Import2: Filename={accompaniment}")

            while len(mytimestamps)>0:
                temp = mytimestamps.pop(0)
                finaltimestamps.append([temp[1],temp[2]])
                split_delete(temp[1],temp[2])






        def export(filename):
            """Export the new track, and deleted both tracks."""
            final = filename.replace(" ","_")
            print(do_command(f"Export2: Filename={os.path.join(PATH,final)} NumChannels=2.0"))

            if deleteaudacity:
                 do_command("SelectAll")
                 do_command("RemoveTracks")

        def do_one_file():
            """Run test with one input file only."""

            play_record()
            final_name =INFOLDER.replace(".","") + "-out.wav"
            export(final_name)


        # Run the test with "testfile.wav" in the specified PATH.

        do_one_file()

        def cleanup_directories():
            dir_path = in_dir

            try:
                shutil.rmtree(dir_path)
            except OSError as e:
                print("Error: %s : %s" % (dir_path, e.strerror))


        cleanup_directories()
        print("Finished Audacity")
    multiple = "word"

    if len(finaltimestamps) > 1:
        multiple = "words"
    elif len(finaltimestamps) == 0:
        multiple = "no words"
    print( "My program took "+ str(time.time() - start_time)+ " to run")
    alltimestamps = ""
    for temp in finaltimestamps:
        alltimestamps = alltimestamps + "["+str(temp[0]) +", " +str(temp[1]) + "] "


    finaltext = 'Song Cleaning finished. Removed '+multiple +' at : '+ alltimestamps
    finaltitle = 'Program Finished. It took : '+ str(time.time() - start_time)+ "to run"
    tk.messagebox.showinfo(finaltitle,finaltext)
    print("Finished Censoring")
    #atexit.register(cleanup_directories)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()

    tk.messagebox.showinfo('Welcome To Clean Song Generator',
                           'Welcome, Please pick a .mp3 file and have Audacity open. This process will take a few minutes')
    file_path = filedialog.askopenfilename(title='Choose Your WAV',
                                           filetypes=(("mp3 files", "*.mp3"), ("all files", "*.*")))

    root = tk.Tk()

    canvas1 = tk.Canvas(root, width=400, height=300, relief='raised')
    canvas1.pack()

    checkshazam = tk.BooleanVar()
    usingshazam = tk.Checkbutton(root, text="Use Shazam to get extra timestamps", variable=checkshazam, command="sel")
    canvas1.create_window(200, 100, window=usingshazam)  # Adjusted y-coordinate

    checkaudacity = tk.BooleanVar()
    usingaudacity = tk.Checkbutton(root, text="Use Audacity", variable=checkaudacity, command="sel")
    canvas1.create_window(200, 140, window=usingaudacity)  # Adjusted y-coordinate

    deleteaudacity = tk.BooleanVar()
    check = tk.Checkbutton(root, text="Delete Audacity tracks after finishing", variable=deleteaudacity, command="sel")
    canvas1.create_window(200, 180, window=check)  # Adjusted y-coordinate


    def getSquareRoot():
        root.destroy()
        root.quit()


    button1 = tk.Button(root, text='Press when done', command=getSquareRoot, bg='brown', fg='white',
                        font=('helvetica', 9, 'bold'))
    canvas1.create_window(200, 250, window=button1)  # Adjusted y-coordinate

    root.mainloop()
    censor(file_path, checkshazam,checkaudacity,deleteaudacity)
    sleep(.02)
    os.remove("cuts.jsonl")