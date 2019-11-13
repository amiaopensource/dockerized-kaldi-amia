#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import argparse                     # used for parsing input arguments
import subprocess

def main():

    parser = argparse.ArgumentParser(description="Finds video and audio files and makes 16kHz wav files from them")
    parser.add_argument('-i','--input',dest='i', help="the path to the input directory")

    args = parser.parse_args()


    #handling the input args. This is kind of a mess in this version
    if args.i is None:
        print("Please enter an input path!")
        quit()

    in_path = args.i
    my_dir = os.path.expanduser('~/Desktop')
    out_path_root = my_dir + "/audio_in/"
    out_path_sub = my_dir + "/audio_in/audio_in_16khz/"

    if not os.path.exists(out_path_root):
        os.mkdir(out_path_root)
    if not os.path.exists(out_path_sub):
        os.mkdir(out_path_sub)

    for filename in os.listdir(in_path):

        current_file_path = os.path.join(in_path, filename)
        noextension = os.path.splitext(filename)[0]


        if (filename.endswith(".mp3") or filename.endswith(".wav") or filename.endswith(".flac")):
            cmd = "/usr/local/bin/ffmpeg -hide_banner -loglevel panic -i '" + current_file_path + "' -c:a pcm_s16le -ac 1 -ar 16000 -vn -dn -y '" + out_path_sub + noextension + "_16kHz.wav'"
        elif (filename.endswith(".mp4") or filename.endswith(".avi") or filename.endswith(".mov") or filename.endswith(".mpeg")): #or .avi, .mpeg, whatever.
            cmd = "/usr/local/bin/ffmpeg -hide_banner -loglevel panic -i '" + current_file_path + "' -c:a pcm_s16le -ac 1 -ar 16000 -dn -y '" + out_path_sub + noextension + "_16kHz.wav'"

        #print(cmd)
        ffmpeg_out = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True).communicate()[0]


# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
    main()
