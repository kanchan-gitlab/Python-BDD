"""
uses requests module and Git hub API endpoints to create compatible git actions
"""
import base64
import json

import requests

from testdata.constants import TestConstants
from utils.helper import get_current_time

user_name = TestConstants.USER_NAME.value
pat_token = TestConstants.ACCESS_TOKEN.value
base_url = TestConstants.DEFAULT_BASE_URL.value
timeout = TestConstants.DEFAULT_TIMEOUT.value
small_timeout = TestConstants.SMALL_TIMEOUT.value
headers = {"Accept": "application/vnd.github.v3+json",
           "Authorization": "token {}".format(pat_token)}


def get_basic_auth(repo):
    """
    curl -u your-username "https://api.github.com/repos/user/repo/issues?state=closed"
    curl -u username:token "https://api.github.com/repos/user/repo/issues?state=closed"
    curl -u username:token https://api.github.com/user
    :return:
    """
    url = f"{base_url}repos/{user_name}/{repo}/issues?state=closed"
    response = requests.get(url, headers=headers)
    if response.status_code > 200:
        raise Exception(f"An error occurred {response}")


def create_new_repo(repo_name=None):
    """
    https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user
    -X POST
    -H "Accept: application/vnd.github+json"
    -H "Authorization: token <TOKEN>
    https://api.github.com/user/repos
    :param repo_name: string/ desired repository name
    :return: string / created repository name
    """
    postfix = get_current_time().strftime("%Y%m%d%H%M%S").replace("/", "")
    if repo_name is None:
        repo = "git_flow_task_" + postfix
    else:
        repo = repo_name + "_" + postfix
    print(f"Creating repo: {repo}")
    url = base_url + "user/repos"
    payload = {"name": "{}".format(repo),
               "auto_init": True,
               "private": False}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code > 201:
        raise Exception(f"An error occurred {response}")
    else:
        return repo


def create_new_branch(new_branch_name, repo_name, from_branch='main'):
    """
    https://docs.github.com/en/rest/git/refs#create-a-reference

    1. get revision from https://api.github.com/repos/<AUTHOR>/<REPO>/git/refs/heads
    2. create new branch
    /repos/{owner}/{repo}/git/refs
    -X POST
     -H "Accept: application/vnd.github.v3+json"
     -H "Authorization: token <TOKEN>"
     https://api.github.com/repos/OWNER/REPO/git/refs
     -d '{"ref":"refs/heads/featureA","sha":"aa218f56b14c9653891f9e74264a383fa43fefbd"}'

    :param new_branch_name: string / desired new branch name
    :param repo_name: string / required repository name
    :param from_branch: string / from branch name, from which new branch will be cut
    :return: string / created branch name
    """
    # url1 = f"https://api.github.com/repos/{user_name}/{repo_name}/git/refs/heads"
    # sha = None
    # revision = requests.get(url=url1, headers=headers).json()
    # for rev in revision:
    #     if rev['ref'] == 'refs/heads/' + from_branch:
    #         sha = rev["object"]['sha']
    sha = get_last_commit_sha_from_branch(repo_name=repo_name, branch_name=from_branch)
    payload = {"ref": "refs/heads/{}".format(new_branch_name), "sha": sha}
    url = f"{base_url}repos/{user_name}/{repo_name}/git/refs"
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code > 201:
        raise Exception(f"An error occurred {response}")
    else:
        return new_branch_name


def push_commits_to_github(filename, repo, branch):
    """
    https://docs.github.com/en/rest/repos/contents#create-or-update-file-contents
    -X PUT \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: token <TOKEN>" \
      https://api.github.com/repos/OWNER/REPO/contents/PATH \
      -d '{"message":"my commit message","committer":{"name":"Monalisa Octocat","email":"octocat@github.com"},"content":"bXkgbmV3IGZpbGUgY29udGVudHM="}'
    :param filename: string / required file name
    :param repo:  string / required repository name
    :param branch: string / desired new branch name
    :return: `Response <Response>` object / response
    """
    sha = get_last_commit_sha_from_branch(repo_name=repo, branch_name=branch)

    contents_new = str(get_current_time()).encode('ascii')
    base64content = base64.b64encode(bytes(contents_new))
    url = f"{base_url}repos/{user_name}/{repo}/contents/{filename}"
    payload = {"message": "update",
               "branch": branch,
               "content": base64content.decode("utf-8"),
               "sha": sha
               }

    response = requests.put(url, data=json.dumps(payload), headers=headers)
    if response.status_code > 201:
        raise Exception(f"An error occurred {response}")
    else:
        return response


def create_a_pull_request(repo, branch_to_merge):
    """
    https://docs.github.com/en/rest/pulls/pulls#create-a-pull-request
     -X POST \
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: token <TOKEN>" \
      https://api.github.com/repos/OWNER/REPO/pulls \
      -d '{"title":"Amazing new feature","body":"Please pull these awesome changes in!","head":"octocat:new-feature","base":"master"}'
    :return: `Response <Response>` object / response
    """
    payload = {"title": "New feature update", "body": "Please review these news changes!",
               "head": branch_to_merge, "base": "main"}
    url = f"{base_url}repos/{user_name}/{repo}/pulls"

    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code > 201:
        raise Exception(f"An error occurred {response}")
    else:
        return response


def get_last_commit_sha_from_branch(repo_name, branch_name="main"):
    """
    https://docs.github.com/en/rest/branches/branches#get-a-branch
      -H "Accept: application/vnd.github+json"
      -H "Authorization: token <TOKEN>"
      https://api.github.com/repos/OWNER/REPO/branches/BRANCH
    :param repo_name:
    :param branch_name:
    :return: string / sha of last commit in the given branch
    """
    url = f'{base_url}repos/{user_name}/{repo_name}/branches/{branch_name}'
    response = requests.get(url=url)
    sha = response.json()['commit']['sha']
    return sha


# additional functions

def delete_repo(repo_name=None):
    """
    https://docs.github.com/en/rest/repos/repos#delete-a-repository
      -X DELETE \
      -H "Accept: application/vnd.github+json"
      -H "Authorization: token <TOKEN>"
      https://api.github.com/repos/OWNER/REPO
    :param repo_name:
    """
    if repo_name is None:
        repos = get_all_repos()
        print(f"Available repos: {repos}")
        for repo in repos:
            if repo.startswith("git_"):
                print(f"Deleting repo: {repo}")
                response = requests.delete(base_url + "repos/{}/{}".format(user_name, repo), headers=headers)
                if response.status_code > 204:
                    raise Exception(f"Couldn't delete repo: {repo}, error: {response}")
    else:
        response = requests.delete(base_url + "repos/{}/{}".format(user_name, repo_name), headers=headers)
        print(response)


def get_all_repos():
    """
    https://docs.github.com/en/rest/repos/repos#list-repositories-for-a-user
      -H "Accept: application/vnd.github+json"
      -H "Authorization: token <TOKEN>"
      https://api.github.com/users/USERNAME/repos
    :return: list
    """
    url = f"{base_url}users/{user_name}/repos"
    repo_data = requests.get(url)
    repo_data = json.loads(repo_data.text)
    repo_list = []
    for repo_name in repo_data:
        repo_list.append(repo_name['name'])
    return repo_list


def get_readme_file(repo):
    """
      -H "Accept: application/vnd.github+json" \
      -H "Authorization: token <TOKEN>" \
      https://api.github.com/repos/OWNER/REPO/readme
    :return: `Response <Response>` object / response
    """
    url = f"{base_url}repos/{user_name}/{repo}/readme"
    response = requests.get(url, headers)
    return response


if __name__ == "__main__":
    # get_basic_auth("git_flow_task_1656864303467092000")
    delete_repo()
