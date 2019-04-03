Feature: CLI ingest pull command
  Scenario: Successful download without local activities
    Given I have a Connect account with 3 activities
    And I have 0 local activities
    When I `cli ingest pull`
    Then I receive 3 activities
    And the exit code is 0

  Scenario: Successful download with local activities
    Given I have a Connect account with 3 activities
    And I have 2 local activities
    When I `cli ingest pull`
    Then I receive 1 activities
    And the exit code is 0

  Scenario: Download with missing activities
    Given I have a Connect account with 3 activities
    And I have 0 local activities
    And 1 activities are missing in the download
    When I `cli ingest pull`
    Then I receive 2 activities
    And I have 1 activities marked as missing
    And the exit code is 128

  Scenario: Authentication fails
    Given I am using wrong credentials
    When I `cli ingest pull`
    Then the exit code is 1
