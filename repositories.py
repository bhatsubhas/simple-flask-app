import urllib.request
import json

base_url = "https://api.github.com/users/{}/repos"

def get_data_from_web(username):
    user_repo_url = base_url.format(username)
    with urllib.request.urlopen((user_repo_url)) as url:
        return json.loads(url.read().decode())

def get_repo_list(username):
    data = get_data_from_web(username)
    repo_names = [x['full_name'].split('/')[1] for x in data if x['full_name']]
    return repo_names