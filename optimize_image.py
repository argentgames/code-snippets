import subprocess
import os, fnmatch

# Convert images (jpg, png, etc.) to webp format using imagemagick.

# https://stackoverflow.com/a/2186673
def find_files(directory, pattern):
    for root, dirs, files in os.walk(directory):
        for basename in files:
            if fnmatch.fnmatch(basename, pattern):
                filename = os.path.join(root, basename)
                yield filename
                
def convert_img(filepath):
    if filepath.endswith('jpg'):
        cmd = "magick convert " + filepath + " -quality 90 -define webp:lossless=false " + filepath.split('.jpg')[0] + ".webp"
        print("Converting jpg...")
        run_cmd = subprocess.call(cmd, shell=True)
        if run_cmd == 0:
            print("Done converting: {}".format(filepath))
            os.remove(filepath)
        else:
            print("FAILED TO CONVERT: {}".format(filepath))
    if filepath.endswith('png'):
        cmd = "magick convert " + filepath + " -quality 90 -define webp:lossless=true " + filepath.split('.png')[0] + ".webp"
        print("Converting png...")
        run_cmd = subprocess.call(cmd, shell=True)
        if run_cmd == 0:
            print("Done converting: {}".format(filepath))
            os.remove(filepath)
        else:
            print("FAILED TO CONVERT: {}".format(filepath))
            
if__name__== "__main__":
    img_folders = ["game/images/Backgrounds", "game/images/CG", "game/images/Sprites"]
    exts = ["*.png", "*.jpg"]
    for ext in exts:
        for folder in img_folders:
            for filepath in find_files(folder, ext):
                convert_img(filepath)
