import hashlib
import json
import os

def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()

file_name = input("Enter file name: ")

current_hash = calculate_hash(file_name)

if os.path.exists("hashes.json"):
    with open("hashes.json", "r") as json_file:
        stored_hashes = json.load(json_file)

    if file_name in stored_hashes:
        if stored_hashes[file_name] == current_hash:
            print("✅ File is unchanged")
        else:
            print("⚠️ WARNING: File has been modified!")
    else:
        print("New file detected")
else:
    stored_hashes = {}

stored_hashes[file_name] = current_hash

with open("hashes.json", "w") as json_file:
    json.dump(stored_hashes, json_file, indent=4)