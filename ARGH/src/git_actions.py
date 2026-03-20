import os
import subprocess


def get_repo_path(entry, directory):
    return os.path.join(directory, f"{entry['First Name']}-{entry['Last Name']}")

def clone_repositories(entries, directory):
    to_download = []

    for entry in entries:
        name = f"{entry['First Name']}-{entry['Last Name']}"
        repo_url = entry['git Link']
        if repo_url == "NA":
            continue
        expected_dir = get_repo_path(entry, directory)
        if os.path.exists(expected_dir):
            continue
        to_download.append((name, repo_url))

    for name, repo_url in to_download:
        expected_dir = os.path.join(directory, name)
        subprocess.run(["git", "clone", repo_url, expected_dir], check=True)

    return
