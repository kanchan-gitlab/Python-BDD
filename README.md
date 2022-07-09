# python-bdd
# BDD framework using Pytest-BDD
Used Python and GitHub API to implement a typical GitHub workflow.


Implemented the following BDD scenario:
  Given user logs in GitHub using basic authentication
  When user creates repository with name "git_flow_task" + suffix current time
  And user creates branch "feature/git_flow_feature"
  And user commits auto generated file
  Then user creates pull request to master branch
                

Library used: 
  Pytest
  Pytest-BDD
  Requests
  Pytest-html
  aenum


- used Python virtual environment

- used requests, pytest, pytest_bdd

- Followed rest API documentation on https://docs.github.com/en/rest

- integrated html report


 
