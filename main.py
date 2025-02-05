import json
import importlib.util
import os
import threading
import time
import random
import uuid
from github import Github
import hashlib
import sys

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_NAME = "..." # de repo naam
MODULES_PATH = "modules"
DATA_PATH = "data"
CONFIG_FILE_PATH = "config.json"

def generate_uuid():
    return str(uuid.uuid4())

def download_file_from_github(repo, file_path, local_path):
    contents = repo.get_contents(file_path)
    with open(local_path, "w") as file:
        file.write(contents.decoded_content.decode("utf-8"))

def download_modules(repo, module_name):
    module_path = f"{MODULES_PATH}/{module_name}.py"
    download_file_from_github(repo, f"{MODULES_PATH}/{module_name}.py", module_path)
    return module_path

def load_and_execute_module(module_name, config, functions):
    module_path = f"{MODULES_PATH}/{module_name}.py"

    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    for key, value in config.items():
        setattr(module, key, value)

    threads = []
    for func_name, should_run in functions.items():
        if should_run.lower() == "true" and hasattr(module, func_name):
            print(f"Uitvoeren van functie: {func_name} in module {module_name}")
            func = getattr(module, func_name)
            thread = start_function_in_thread(func)
            thread.start()
            threads.append(thread)
    
    return threads

def start_function_in_thread(func):
    thread = threading.Thread(target=func)
    return thread

def get_file_hash(file_path):
    with open(file_path, "rb") as f:
        return hashlib.md5(f.read()).hexdigest()

def restart_script():
    print("config.json is gewijzigd. Herstarten van script")
    os.execv(sys.executable, ['python'] + sys.argv)

def push_data_to_github(repo):
    commit_message = "Update data directory"

    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            file_path = os.path.join(root, file)
            relative_path = os.path.relpath(file_path, DATA_PATH)

            with open(file_path, "rb") as f:
                content = f.read()

            try:
                repo.create_file(
                    f"data/{relative_path}",
                    commit_message,
                    content,
                )
                print(f"Bestand toegevoegd: {relative_path}")
            except:
                repo.update_file(
                    f"data/{relative_path}",
                    commit_message,
                    content,
                    repo.get_contents(f"data/{relative_path}").sha,
                )
                print(f"Bestand bijgewerkt: {relative_path}")


def check_config_changes(repo, initial_config_hash):
    print("Check voor config.json wijzigingen")
    download_file_from_github(repo, CONFIG_FILE_PATH, "config.json")
    new_config_hash = get_file_hash("config.json")

    if new_config_hash != initial_config_hash:
        print("config.json is gewijzigd, data map pushen naar GitHub...")
        initial_config_hash = new_config_hash
        push_data_to_github(repo)
        print("Herstarten van het script na config wijziging...")
        restart_script()

    interval = random.randint(10, 60)  # wacht random interval
    print(f"Wachten voor {interval} seconden voordat config opnieuw wordt gecontroleerd")
    time.sleep(interval)



def main():
    g = Github(GITHUB_TOKEN)
    repo = g.get_repo(REPO_NAME)

    if not os.path.exists(MODULES_PATH):
        os.makedirs(MODULES_PATH)

    if not os.path.exists(DATA_PATH):
        os.makedirs(DATA_PATH)

    uuid_file_path = "uuid.txt"
    if not os.path.exists(uuid_file_path):
        unique_uuid = generate_uuid()

        with open(uuid_file_path, "w") as f:
            f.write(unique_uuid)
        print(f"UUID gegenereerd en opgeslagen: {unique_uuid}")
    else:
        with open(uuid_file_path, "r") as f:
            unique_uuid = f.read().strip()
        print(f"UUID uit bestand gelezen: {unique_uuid}")

    uuid_path = os.path.join(DATA_PATH, unique_uuid)
    if not os.path.exists(uuid_path):
        os.makedirs(uuid_path)
    print(f"UUID-directory aangemaakt: {uuid_path}")

    print("Download config.json van GitHub...")
    download_file_from_github(repo, CONFIG_FILE_PATH, "config.json")

    with open("config.json", "r") as file:
        config = json.load(file)

    initial_config_hash = get_file_hash("config.json")

    while True:
        print("Download modules en voer uit...")
        for module in config["modules"]:
            module_name = module["name"]
            print(f"Module downloaden: {module_name}")
            download_modules(repo, module_name)
            load_and_execute_module(module_name, module["config"], module["functions"])

        check_config_changes(repo, initial_config_hash)


if __name__ == "__main__":
    main()
