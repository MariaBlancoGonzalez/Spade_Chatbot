import os
import subprocess
import pytube


def download(route, name):
    try:
        yt = pytube.YouTube(route)
    except:
        return 1
    
    vids= yt.streams.all()

    vnum = 0

    parent_dir = "../musica"
    vids[vnum].download("../musica")

    new_filename = name  # e.g. new_filename.mp3

    default_filename = vids[vnum].default_filename  
    subprocess.run([
        'ffmpeg',
        '-i', os.path.join(parent_dir, default_filename),
        os.path.join(parent_dir, new_filename)
    ])
    return 0
