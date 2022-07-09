Feature: git workflow
  git workflow to add new repo, create a branch and push a file


  Scenario: push a file to new repo
    Given user has authentication Token
    When user creates a repo with name "git_flow_task"
    And user creates a branch "feature/git_flow_feature"
    And user adds a commit
    Then user creates a pull request to main branch
