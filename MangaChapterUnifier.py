import os
import shutil
from PIL import Image
import time

manganame = r"One Piece"
start = time.time()
mangasfolder = r"C:\Users\tamme\Documents\Mangas"
mangapath = mangasfolder+"\\"+manganame
os.chdir(mangapath)
chapters = os.listdir()
total = 0
completed = 0

for chapter in chapters:
    for item in os.listdir(chapter):
        total += 1

for chapter in chapters:
    if not os.path.isfile(chapter) and "Chapter" in chapter:
        for item in os.listdir(chapter):
            newname = chapter.split(" ")[chapter.split(" ").index("Chapter") + 1] + "_" + item
            os.rename(chapter + "\\" + item, newname)
            im = Image.open(newname).convert("RGB")
            im.save(newname.split(".")[0] + ".png", "png")
            os.remove(newname)
            completed += 1
            print(f"\rImages: {completed}/{total}", end = "\r")
        shutil.rmtree(chapter)

end = time.time()
print(f"{total} images, {int(end-start)} seconds.")