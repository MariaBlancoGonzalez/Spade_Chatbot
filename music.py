import os
import subprocess
import pytube

def download(ruta):
    
    yt = pytube.YouTube(ruta)

    vids= yt.streams.all()
    for i in range(len(vids)):
        print(i,'. ',vids[i])

    vnum = int(input("Enter video id: "))

    parent_dir = r"musica"
    vids[vnum].download(parent_dir)

    new_filename = input("Enter filename (including extension): ")  # e.g. new_filename.mp3

    default_filename = vids[vnum].default_filename  # get default name using pytube API
    subprocess.run([
        'ffmpeg',
        '-i', os.path.join(parent_dir, default_filename),
        os.path.join(parent_dir, new_filename)
    ])

