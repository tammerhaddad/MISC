import os
import string
import itertools
import json
from tqdm import tqdm

MAP_NAME = 'name_map.json'

def get_alphabetical_names(n):
  """Generate alphabetical names for n files using 5 letters."""
  alphabet = string.ascii_lowercase
  combos = itertools.islice(itertools.product(alphabet, repeat=5), n)
  return [''.join(name) for name in combos]

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
  # Sort files numerically based on the numeric part of the filename, with the
  # name as a tiebreaker so that files without digits get a stable order
  # instead of whatever os.listdir happened to return
  files.sort(key=lambda f: (int(''.join(filter(str.isdigit, f)) or 0), f))
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

  name_map = {}
  for old_name, new_name in tqdm(zip(files, targets), total=num_files, desc="Renaming files"):
    old_path = os.path.join(folder_path, old_name)
    new_path = os.path.join(folder_path, new_name)
    os.rename(old_path, new_path)
    name_map[new_name] = old_name
    # tqdm.write keeps the progress bar from being torn apart by these lines
    tqdm.write(f'Renamed {old_name} to {new_name}')

  # Save the name map to a file
  with open(map_path, 'w') as f:
    json.dump(name_map, f)

def reverse_rename_files(folder_path):
  # Load the name map from the file
  with open(os.path.join(folder_path, MAP_NAME), 'r') as f:
    name_map = json.load(f)

  # Restore through temporary names. Going straight to the originals overwrites
  # any file currently sitting on a name we are about to restore -- which
  # happens whenever an original name matches one of the generated ones.
  staged = []
  for new_name, old_name in name_map.items():
    tmp_name = new_name + '.revert-tmp'
    os.rename(os.path.join(folder_path, new_name),
              os.path.join(folder_path, tmp_name))
    staged.append((tmp_name, old_name))

  for tmp_name, old_name in staged:
    os.rename(os.path.join(folder_path, tmp_name),
              os.path.join(folder_path, old_name))
    # print(f'Renamed {tmp_name} back to {old_name}')

if __name__ == "__main__":
  folder_path = "epubChunks"
  rename_files(folder_path)
  # To reverse the renaming, uncomment the following line
  # reverse_rename_files(folder_path)
