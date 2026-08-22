import os
from PIL import Image, UnidentifiedImageError
import time

manganame = r"One Piece"
start = time.time()
mangasfolder = r"C:\Users\tamme\Documents\Mangas"
mangapath = os.path.join(mangasfolder, manganame)
os.chdir(mangapath)


def chapter_number(chapter):
    """The chapter number in a folder name, or None if there isn't one.

    Splits on runs of whitespace, so "One Piece  Chapter  11" works, and
    requires the token to start with a digit so that "Chapter Extra" or a
    trailing "Chapter" is rejected rather than producing a blank number.
    """
    parts = chapter.split()
    if "Chapter" not in parts:
        return None
    index = parts.index("Chapter") + 1
    if index >= len(parts):
        return None
    number = parts[index]
    return number if number[:1].isdigit() else None


def free_target(number, item):
    """A .png name for this page that no existing file is using.

    Everything lands in one folder, so two chapters sharing a number, or two
    pages differing only in extension ("01.jpg" and "01.png"), would otherwise
    silently overwrite each other.
    """
    stem = f"{number}_{os.path.splitext(item)[0]}"
    candidate = f"{stem}.png"
    suffix = 2
    while os.path.exists(candidate):
        candidate = f"{stem}-{suffix}.png"
        suffix += 1
    return candidate


# only count and walk the folders we are actually going to unify
entries = sorted(os.listdir())
chapters = [c for c in entries
            if os.path.isdir(c) and chapter_number(c) is not None]
unparsed = [c for c in entries if os.path.isdir(c) and c not in chapters]
total = sum(len(os.listdir(chapter)) for chapter in chapters)
completed = 0
skipped = []

for chapter in chapters:
    number = chapter_number(chapter)
    for item in sorted(os.listdir(chapter)):
        source = os.path.join(chapter, item)
        # Decode before moving anything. The old version renamed the file out
        # of its folder first, so a subdirectory or a stray Thumbs.db raised
        # part way through and left the file stranded in the manga root with
        # every later chapter unprocessed.
        try:
            with Image.open(source) as im:
                converted = im.convert("RGB")
        except (UnidentifiedImageError, OSError):
            skipped.append(source)
            continue
        converted.save(free_target(number, item), "png")
        os.remove(source)
        completed += 1
        print(f"\rImages: {completed}/{total}", end = "\r")
    # only drop the folder once it is genuinely empty, so anything we skipped
    # is left where it is instead of being deleted with it
    leftover = os.listdir(chapter)
    if leftover:
        print(f"\rKept {chapter}: {len(leftover)} item(s) not converted")
    else:
        os.rmdir(chapter)

end = time.time()
print(f"\r{completed} of {total} images, {int(end-start)} seconds.")
if skipped:
    print(f"Skipped {len(skipped)} non-image item(s): {skipped[:5]}")
if unparsed:
    print(f"No chapter number found, left alone: {unparsed[:5]}")
