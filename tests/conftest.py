"""Pytest configuration and shared fixtures for all tests."""

import pytest
from pathlib import Path
from unittest.mock import Mock, MagicMock
import tempfile
import shutil


@pytest.fixture
def temp_project_dir():
    """Create a temporary project directory for testing."""
    temp_dir = tempfile.mkdtemp()
    yield Path(temp_dir)
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def mock_subprocess():
    """Mock subprocess.run for testing CLI interactions."""
    mock = Mock()
    mock.return_value = Mock(
        returncode=0,
        stdout="",
        stderr="",
        args=[]
    )
    return mock


@pytest.fixture
def sample_gbsproj_path(temp_project_dir):
    """Create a sample GB Studio project file."""
    project_file = temp_project_dir / "test-project.gbsproj"
    project_file.write_text('{"name": "test-project", "author": "test"}')
    return project_file


@pytest.fixture
def mock_langflow_component():
    """Mock LangFlow Component base class."""
    mock = MagicMock()
    mock.display_name = "TestComponent"
    mock.description = "A test component"
    return mock


@pytest.fixture
def sample_approval_queue():
    """Sample approval queue data structure."""
    return {
        "queue": [
            {
                "timestamp": "2025-11-21T10:00:00",
                "file": "assets/sprites/test.png",
                "change_type": "modified",
                "approved": False
            }
        ]
    }


@pytest.fixture
def sample_ledger_entries():
    """Sample ledger entries for testing."""
    return [
        {
            "timestamp": "2025-11-21T10:00:00",
            "event": "build_started",
            "agent": "ci_cd_pipeline",
            "task_id": "build-001",
            "details": {"target": "rom"}
        },
        {
            "timestamp": "2025-11-21T10:05:00",
            "event": "build_completed",
            "agent": "ci_cd_pipeline",
            "task_id": "build-001",
            "details": {"success": True}
        }
    ]
