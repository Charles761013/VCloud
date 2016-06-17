import os

FILE_DIR = 'video_upload'
FILE_PATH = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/' + FILE_DIR

def handle_uploaded_file(f, filename):
  full_path = os.path.join(FILE_PATH, filename)
  with open(full_path, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)