import os
import string
import itertools
import json
from tqdm import tqdm

MAP_NAME = 'name_map.json'
TMP_SUFFIX = '.revert-tmp'

def get_alphabetical_names(n):
  """Generate alphabetical names for n files using 5 letters."""
  alphabet = string.ascii_lowercase
  combos = itertools.islice(itertools.product(alphabet, repeat=5), n)
  return [''.join(name) for name in combos]

def sort_key(name):
  """Numeric part first, then the name, for a stable order.

  Only ASCII digits: '²'.isdigit() is True but int('²') raises, so
  filtering on isdigit alone made a file like 'page².txt' crash the sort.
  """
  digits = ''.join(c for c in name if c in string.digits)
  return (int(digits or 0), name)

def rename_files(folder_path):
  # a map already here means this folder was renamed before, and a second pass
  # would overwrite it and lose the original names for good
  map_path = os.path.join(folder_path, MAP_NAME)
  if os.path.exists(map_path):
    raise FileExistsError(
        f'{map_path} already exists. Run reverse_rename_files first, or delete '
        f'it if the original names are no longer needed.')

  # skip the map itself, otherwise it gets renamed along with the content
  files = [f for f in os.listdir(folder_path)
           if os.path.isfile(os.path.join(folder_path, f)) and f != MAP_NAME]
  # Sort files numerically based on the numeric part of the filename
  files.sort(key=sort_key)
  num_files = len(files)
  new_names = get_alphabetical_names(num_files)

  targets = [new + os.path.splitext(old)[1]
             for old, new in zip(files, new_names)]

  # os.rename overwrites its destination without warning. Walk the planned
  # sequence and object only to a target that is still occupied at the point we
  # would move onto it -- a name held by a file we rename away first is fine.
  remaining = set(os.listdir(folder_path))
  clashes = []
  for old_name, new_name in zip(files, targets):
    remaining.discard(old_name)
    if new_name in remaining:
      clashes.append(new_name)
    remaining.add(new_name)
  if clashes:
    raise FileExistsError(
        f'{len(clashes)} rename(s) in {folder_path} would overwrite an existing '
        f'file, e.g. {clashes[:3]}. Move those out of the way first.')

  # Write the map before renaming anything. Saving it only after the loop meant
  # any failure part way through (a too-long name, a permission error) left
  # files renamed with no record of what they had been called.
  name_map = dict(zip(targets, files))
  with open(map_path, 'w') as f:
    json.dump(name_map, f)

  for old_name, new_name in tqdm(zip(files, targets), total=num_files, desc="Renaming files"):
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)
    # tqdm.write keeps the progress bar from being torn apart by these lines
    tqdm.write(f'Renamed {old_name} to {new_name}')

def reverse_rename_files(folder_path):
  # Load the name map from the file
  with open(os.path.join(folder_path, MAP_NAME), 'r') as f:
    name_map = json.load(f)

  present = set(os.listdir(folder_path))

  # Stage 1: move every renamed file aside first. Restoring them one at a time
  # would overwrite whatever currently sits on a name we are about to restore.
  # A file that has gone missing is skipped rather than aborting the run, and
  # one already staged by an interrupted revert is picked up where it left off.
  staged, missing = [], []
  for new_name, old_name in name_map.items():
    tmp_name = new_name + TMP_SUFFIX
    if tmp_name in present and new_name in present:
      raise FileExistsError(
          f'both {new_name} and {tmp_name} exist in {folder_path}, so there is '
          f'no telling which holds the real content. Sort that out by hand.')
    if tmp_name in present:
      staged.append((tmp_name, old_name))
    elif new_name in present:
      os.rename(os.path.join(folder_path, new_name),
                os.path.join(folder_path, tmp_name))
      present.discard(new_name)
      present.add(tmp_name)
      staged.append((tmp_name, old_name))
    else:
      missing.append(new_name)

  # Stage 2: never restore onto a name something else has taken in the meantime
  blocked = [old_name for _, old_name in staged if old_name in present]
  if blocked:
    raise FileExistsError(
        f'{len(blocked)} original name(s) in {folder_path} are taken by other '
        f'files, e.g. {blocked[:3]}. The renamed files are staged as '
        f'*{TMP_SUFFIX}; move the blockers aside and run this again to resume.')

  for tmp_name, old_name in staged:
    os.rename(os.path.join(folder_path, tmp_name),
              os.path.join(folder_path, old_name))
    # print(f'Renamed {tmp_name} back to {old_name}')

  if missing:
    print(f'{len(missing)} file(s) in the map were gone, e.g. {missing[:3]}')

if __name__ == "__main__":
  # relative to this script, so it works from any working directory
  folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "epubChunks")
  rename_files(folder_path)
  # To reverse the renaming, uncomment the following line
  # reverse_rename_files(folder_path)
