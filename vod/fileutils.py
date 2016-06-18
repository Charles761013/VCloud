import os
from shutil import copy
import subprocess
import shlex

FILE_DIR = 'video_upload'
FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/' + FILE_DIR
FILE_REAL_PATH = FILE_PATH
TEMP_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/temp/'
THUMB_SUBDIR = '/media/thumbnail/'
THUMB_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + THUMB_SUBDIR

def handle_uploaded_file(f, filename):
  full_path = os.path.join(FILE_PATH, filename)
  with open(full_path, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)
    destination.close()
    copy(full_path, TEMP_DIR) #this is workaround to make video thumbnail

def delete_uploaded_file(filename):
  full_path = os.path.join(FILE_REAL_PATH, filename)
  try:
    os.remove(full_path)
  except:
    print("delete fail")

def do_thumbnail(filename):
  full_path = os.path.join(TEMP_DIR, filename)
  filename_org = filename.split(".")[0] + ".jpg"

  output_path = os.path.join(THUMB_DIR, filename_org)
  print output_path
  command = "ffmpeg -ss 00:00:10 -i {0} -vframes 1 -q:v 2 {1}".format(full_path, output_path)
  subprocess.call(shlex.split(command))
  try:
    os.remove(full_path)
  except:
    print("delete fail")

  return  (THUMB_SUBDIR + filename_org)

def delete_thumbnail(filename):
  filename_org = filename.split(".")[0] + ".jpg"
  full_path = os.path.join(THUMB_DIR, filename_org)
  print full_path
  try:
    os.remove(full_path)
  except:
    print("delete fail")

