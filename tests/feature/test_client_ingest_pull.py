from unittest.mock import Mock
from click.testing import CliRunner
from pytest import fixture
from pytest_bdd import scenario, given, when, then, parsers
from cli import cli


@fixture
def context():
    return {}


@scenario("test_client_ingest_pull.feature", "Successful download without local activities")
def test_successful_download_without_local_activities():
    pass


@scenario("test_client_ingest_pull.feature", "Successful download with local activities")
def test_successful_download_with_local_activities():
    pass


@scenario("test_client_ingest_pull.feature", "Download with missing activities")
def test_download_with_missing_activities():
    pass


@scenario("test_client_ingest_pull.feature", "Authentication fails")
def test_authentication_fails():
    pass


@given(parsers.parse("I have a Connect account with {num_activities:d} activities"))
def i_have_a_connect_account_with_num_activities_activities(num_activities, mocker, context):
    client = mocker.patch("trainalyzr.cli.ingest.ConnectClient").return_value.__enter__.return_value
    client.activities = set(range(num_activities))
    client.download_activity.return_value = "FiTdAtA"
    context["client"] = client


@given(parsers.parse("I have {num_activities:d} local activities"))
def i_have_num_activities_local_activities(num_activities, mocker, context):
    storage = mocker.patch("trainalyzr.cli.ingest.FitStorage").return_value
    storage.activities = set(range(num_activities))
    context["storage"] = storage


@given(parsers.parse("{num_missing:d} activities are missing in the download"))
def num_missing_activities_are_missing_in_the_download(num_missing, context):
    client = context["client"]
    successes = len(client.activities) - num_missing
    assert successes >= 0
    rv = ["FiTdAtA" for _ in range(successes)] + [None for _ in range(num_missing)]
    download = Mock()
    download.side_effect = rv
    client.download_activity = download


@given("I am using wrong credentials")
def i_am_using_wrong_credentials(mocker, context):
    mocker.patch("trainalyzr.cli.ingest.ConnectClient").return_value.__enter__.side_effect = ValueError("")


@when("I `cli ingest pull`")
def i_cli_ingest_pull(context):
    runner = CliRunner()
    result = runner.invoke(cli, ["ingest", "pull", "--account=test-account", "--password=test-password"])
    context["result"] = result


@then(parsers.parse("I receive {num_activities:d} activities"))
def i_receive_num_activities_activities(num_activities, context):
    assert context["storage"].save.call_count == num_activities


@then(parsers.parse("I have {num_missing:d} activities marked as missing"))
def i_have_num_missing_activities_marked_as_missing(num_missing, context):
    assert context["storage"].add_missing.call_count == num_missing


@then(parsers.parse("the exit code is {exit_code:d}"))
def the_exit_code_is(exit_code, context):
    assert context["result"].exit_code == exit_code
