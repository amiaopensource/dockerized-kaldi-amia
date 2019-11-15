# Dockerized speech recognition with Kaldi + American Archive of Public Broadcasting models

### References

  - Kaldi: [http://kaldi-asr.org/](http://kaldi-asr.org/)
  - AAPB Kaldi release and install guide: [https://github.com/dericed/american-archive-kaldi](https://github.com/dericed/american-archive-kaldi)
  - Model files, original from Pop Up Archive: [https://sourceforge.net/projects/popuparchive-kaldi/files/](https://sourceforge.net/projects/popuparchive-kaldi/files/)
  - American Archive of Public Broadcasting (source of training set): [http://americanarchive.org/](http://americanarchive.org/)

## Setup

### Build the Docker Image

- Pull image from Docker Hub (12GB compressed, 24GB uncompressed).

```
docker pull hipstas/kaldi-pop-up-archive:v1
```

- Alternatively you can build the image yourself by running the following command from this directory:

```
docker build -t kaldi-local . 
```
### Check your memory allocation

- Open your Docker preferences and make sure Docker has access to at least 6GB of RAM. The more, the better.

### Run a Docker Container

This  step creates a Docker container named `kaldi-aapb` based on the image we built above. Use one of the following commands. 

Fill in `<image-name>` with either `hipstas/kaldi-pop-up-archive:v1` or `kaldi-local` depending on your build method above.

*Linux:*

```
docker run -it --name kaldi-aapb --volume /audio_in/:/audio_in/ <image-name>
```

*macOS:*

```
docker run -it --name kaldi-aapb --volume ~/Desktop/audio_in/:/audio_in/ <image-name>
```

*Windows:*

```
docker run -it --name kaldi-aapb --volume C:\Users\***username_here***\Desktop\audio_in\:/audio_in/ <image-name>
```
 
### (Now that your container is running...)
   
 If you're using Linux, this will create a shared volume at `/audio_in`. On macOS or Windows, a folder called `audio_in` will appear on your desktop. The `/audio_in` folder is passed as a shared volume into the Docker container.


### Prepare your files

- Kaldi wants to process 16khz .wav files, so we will ensure your local `/audio_in` folder contains them. Prepping the files on your local computer is ideal, because it processing them through the docker container is very slow. In order to use this script you'll have to have `ffmpeg` installed.

- Open a new terminal window. On your local machine, run `scripts/prep_files.py` on the directory of files you wish to process. This will run on WAV, MP3, FLAC, AVI, MOV, MP4, MXF, and MKV files, and will drop the pre-processed  media files into the shared `/audio_in` directory. 
```
scripts/prep_files.py -i <path/to/source/directory>
```
## Run speech-to-text batch

- Return to your Docker terminal session. Enter the following commands to download and run the `setup.sh` script, which will start your job. When the batch is finished, your plain text and JSON transcript files will be written to `/audio_in/transcripts/`.

```
wget https://raw.githubusercontent.com/hipstas/kaldi-pop-up-archive/master/setup.sh
sh ./setup.sh
```

To keep your job from ending when you close the terminal window (or your connection to the server is interrupted), use `nohup sh ./setup.sh` instead, then close the window. If you'd like to monitor the job's status, open a new terminal session (`docker exec -it kaldi-aapb bash`) and use the following command to display the end of your `nohup` log file every 3 seconds:

```
while :; do tail -n 30 nohup.out; sleep 3; done
```

### Notes

- Try running a test with one or two short media files before beginning a big job. If Kaldi doesn't have enough memory, it will crash without explanation. If this happens, try reducing the number of simultaneous jobs as described above.

- Any commas, spaces, pipes, etc. in audio filenames will break the script and halt progress without producing any descriptive errors. To be safe, you may want to rename each file with a unique ID before starting. I'll fix this when I get a chance.

- With this configuration, speech-to-text processing may take 5 times the duration of your audio input, or perhaps even longer. If you have memory to spare, you can speed things up by increasing the number of simultaneous jobs. Use the `free -m` command while Kaldi is running to see how you're doing.



### Optional performance tweaks

- In `/kaldi/egs/american-archive-kaldi/sample_experiment/run.sh`, adjust the following option to set the number of simultaneous jobs:

```
nj=4
```

- In `/kaldi/egs/wsj/s5/utils/run.pl`:

```
$max_jobs_run = 10;
```

In `/kaldi/egs/wsj/s5/steps/decode_fmllr.sh`:

<!--
`/kaldi/egs/wsj/s5/steps/tandem/decode_fmllr.sh`
-->

```
nj=4 in
max_active=2000
```

- In `/kaldi/egs/wsj/s5/steps/decode.sh`:

```
nj=2
```