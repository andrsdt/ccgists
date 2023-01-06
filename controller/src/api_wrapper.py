from utils import caesar_decrypt, caesar_encrypt
from dotenv import load_dotenv
import os
import requests
import steganography

"""Wrapper for GitHub API. Makes it easier to handle requests to gists."""

load_dotenv()
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")

base_url = "https://api.github.com/gists"

base_headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer " + GITHUB_TOKEN,
    "X-GitHub-Api-Version": "2022-11-28"
}


def create_gist(description, body, file_name=None):
    file_name = file_name if file_name != None else description.split(' ')[1].lower() + ".md"
    data = {
        "description": description,
        "public": False,
        "files": {
            file_name: {
                "content": body
            }
        }
    }

    response = requests.post(base_url, headers=base_headers, json=data)
    return response.status_code, response.reason


def create_comment(gist_id, comment, cipher=True):
    body = caesar_encrypt(
        comment, steganography.caesar_constant) if cipher else comment
    response = requests.post(base_url + "/" + str(gist_id) + "/comments",
                             headers=base_headers, json={"body": body})
    return response.status_code, response.reason


def get_gists():
    response = requests.get(base_url, headers=base_headers)
    return response.json()


def get_gist(gist_id):
    response = requests.get(base_url + "/" + gist_id, headers=base_headers)
    return response.json()


def get_gist_id_from_description(description):
    gists = get_gists()
    for gist in gists:
        if description in gist["description"]:
            return gist["id"]


def get_comments(gist_id, cipher=True):
    response = requests.get(base_url + "/" + gist_id +
                            "/comments", headers=base_headers)
    json = response.json()

    if cipher:
        for c in json:
            c['body'] = caesar_decrypt(
                c['body'], steganography.caesar_constant)

    return json


def delete_gist(gist_id):
    response = requests.delete(base_url + "/" + gist_id, headers=base_headers)
    return response.status_code, response.reason
