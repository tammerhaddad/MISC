import os
import shutil
from PIL import Image
import time

manganame = r"One Piece"
start = time.time()
mangasfolder = r"C:\Users\tamme\Documents\Mangas"
mangapath = os.path.join(mangasfolder, manganame)
os.chdir(mangapath)


def chapter_number(chapter):
    """The token after "Chapter" in a folder name, or None if there isn't one."""
    parts = chapter.split(" ")
    if "Chapter" not in parts:
        return None
    number = parts.index("Chapter") + 1
    return parts[number] if number < len(parts) else None


# only count and walk the folders we are actually going to unify
chapters = [c for c in os.listdir()
            if os.path.isdir(c) and chapter_number(c) is not None]
total = sum(len(os.listdir(chapter)) for chapter in chapters)
completed = 0

for chapter in chapters:
    number = chapter_number(chapter)
    for item in os.listdir(chapter):
        newname = number + "_" + item
        os.rename(os.path.join(chapter, item), newname)
        pngname = os.path.splitext(newname)[0] + ".png"
        # convert() loads the pixels, so the source handle is closed before we
        # save -- otherwise a source that is already a .png gets deleted below
        with Image.open(newname) as im:
            converted = im.convert("RGB")
        converted.save(pngname, "png")
        if pngname != newname:
            os.remove(newname)
        completed += 1
        print(f"\rImages: {completed}/{total}", end = "\r")
    shutil.rmtree(chapter)

end = time.time()
print(f"{total} images, {int(end-start)} seconds.")
