from pathlib import Path

from pytest_bdd import scenario, when, parsers, given, then

from pages.api_requests import *

feature_file_dir = '../features'
feature_file = 'git_workflow.feature'
base_dir = Path(__file__).resolve().parent
feature_file_path = str(base_dir.joinpath(feature_file_dir).joinpath(feature_file))


@scenario(feature_file_path, "push a file to new repo")
def test_commit_a_file():
    pass


@given('user has authentication Token')
def get_auth_token():
    get_basic_auth('JavaPractice')
    # delete_repo()


@when(parsers.parse('user creates a repo with name "{repo}"'))
def step_create_a_new_repo(context, repo):
    context['repo'] = create_new_repo(repo)


@when(parsers.parse('user creates a branch "{new_branch}"'))
def step_add_a_new_branch(context, new_branch):
    context['branch'] = create_new_branch(new_branch_name=new_branch, repo_name=context['repo'])


@when('user adds a commit')
def step_add_a_commit(context):
    push_commits_to_github("readme", repo=context['repo'], branch=context['branch'])


@then('user creates a pull request to main branch')
def step_create_a_pull_request(context):
    create_a_pull_request(repo=context['repo'], branch_to_merge=context['branch'])
