import os
from typing import Generator
from fastapi.testclient import TestClient
from moto import mock_aws
import pytest

from main import app
from tests.utils.database import create_test_table

@pytest.fixture(scope="module")
def test_client() -> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="function")
def aws_credentials():
    """Mocked AWS Credentials for moto."""
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def aws(aws_credentials):
    with mock_aws():
        yield

@pytest.fixture(scope="function")
def dynamodb_client(aws):
    create_test_table('codefeedback')