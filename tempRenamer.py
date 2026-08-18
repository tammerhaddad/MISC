import os
import string
import itertools
import json
from tqdm import tqdm

def get_alphabetical_names(n):
  """Generate alphabetical names for n files using 5 letters."""
  alphabet = string.ascii_lowercase
  names = []
  for name in itertools.product(alphabet, repeat=5):
    names.append(''.join(name))
    if len(names) == n:
      break
  return names

def rename_files(folder_path):
  files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
  # Sort files numerically based on the numeric part of the filename
  files.sort(key=lambda f: int(''.join(filter(str.isdigit, f)) or 0))
  num_files = len(files)
  new_names = get_alphabetical_names(num_files)
  
  name_map = {}
  for old_name, new_name in tqdm(zip(files, new_names), total=num_files, desc="Renaming files"):
    old_path = os.path.join(folder_path, old_name)
    file_extension = os.path.splitext(old_name)[1]
    new_path = os.path.join(folder_path, new_name + file_extension)
    os.rename(old_path, new_path)
    name_map[new_name + file_extension] = old_name
    print(f'Renamed {old_name} to {new_name + file_extension}')
  
  # Save the name map to a file
  with open(os.path.join(folder_path, 'name_map.json'), 'w') as f:
    json.dump(name_map, f)

def reverse_rename_files(folder_path):
  # Load the name map from the file
  with open(os.path.join(folder_path, 'name_map.json'), 'r') as f:
    name_map = json.load(f)
  
  for new_name, old_name in name_map.items():
    new_path = os.path.join(folder_path, new_name)
    old_path = os.path.join(folder_path, old_name)
    os.rename(new_path, old_path)
    # print(f'Renamed {new_name} back to {old_name}')

if __name__ == "__main__":
  folder_path = "epubChunks"
  rename_files(folder_path)
  # To reverse the renaming, uncomment the following line
  # reverse_rename_files(folder_path)