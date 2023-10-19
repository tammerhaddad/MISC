import os

Folderpath = r"C:\Users\tamme\Documents\Mangas\Test Folder"

size = 0

for path, dirs, files in os.walk(Folderpath):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)

print(size)