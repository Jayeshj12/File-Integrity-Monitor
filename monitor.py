import hashlib
import json
import os
from datetime import datetime

FOLDER_TO_MONITOR = "monitored_files"
LOG_FILE = "security_log.txt"


def calculate_hash(file_path):
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while chunk := file.read(4096):
            sha256.update(chunk)

    return sha256.hexdigest()


def write_log(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"{timestamp} - {message}\n")


def scan_folder():

    if os.path.exists("hashes.json"):
        with open("hashes.json", "r") as json_file:
            stored_hashes = json.load(json_file)
    else:
        stored_hashes = {}

    print("\nScanning folder...\n")

    for filename in os.listdir(FOLDER_TO_MONITOR):

        file_path = os.path.join(FOLDER_TO_MONITOR, filename)

        if os.path.isfile(file_path):

            current_hash = calculate_hash(file_path)

            if filename in stored_hashes:

                if stored_hashes[filename] == current_hash:
                    print(f"✅ {filename} unchanged")

                else:
                    print(f"⚠️ {filename} modified")
                    write_log(f"WARNING: {filename} modified")

            else:
                print(f"🆕 {filename} added")
                write_log(f"NEW FILE: {filename}")

            stored_hashes[filename] = current_hash

    with open("hashes.json", "w") as json_file:
        json.dump(stored_hashes, json_file, indent=4)


def view_logs():

    print("\n===== SECURITY LOGS =====\n")

    if not os.path.exists(LOG_FILE):
        print("No logs found.")
        return

    with open(LOG_FILE, "r") as log_file:
        logs = log_file.read()

        if logs.strip() == "":
            print("Log file is empty.")
        else:
            print(logs)


while True:

    print("\n=========================")
    print(" FILE INTEGRITY MONITOR")
    print("=========================")
    print("1. Scan Folder")
    print("2. View Security Logs")
    print("3. Exit")

    choice = input("\nChoose an option: ")

    if choice == "1":
        scan_folder()

    elif choice == "2":
        view_logs()

    elif choice == "3":
        print("Exiting...")
        break

    else:
        print("Invalid option. Try again.")