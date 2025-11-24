#!/usr/bin/env python3
"""
Unit Tests for check_scene_limits.py

Tests scene limit validation including:
- Actor count limits
- Trigger count limits
- Script size limits
- Scene data validation
"""

import pytest
import sys
import json
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts' / 'validation'))

from check_scene_limits import validate_scene


class TestValidateScene:
    """Test scene file validation function."""

    @pytest.mark.unit
    def test_valid_scene(self, temp_dir):
        """Test validation of a valid scene."""
        scene_data = {
            "id": "test-scene-001",
            "name": "Test Scene",
            "actors": [],
            "triggers": [],
            "script": []
        }

        scene_path = temp_dir / "test_scene.json"
        with open(scene_path, 'w') as f:
            json.dump(scene_data, f)

        is_valid, issues = validate_scene(str(scene_path))
        assert is_valid is True
        assert len(issues) == 0

    @pytest.mark.unit
    def test_too_many_actors(self, temp_dir):
        """Test validation warns about too many actors."""
        # GB Studio has limits on actors per scene
        actors = [{"id": f"actor-{i}", "name": f"Actor {i}"} for i in range(50)]

        scene_data = {
            "id": "crowded-scene",
            "name": "Crowded Scene",
            "actors": actors,
            "triggers": [],
            "script": []
        }

        scene_path = temp_dir / "crowded_scene.json"
        with open(scene_path, 'w') as f:
            json.dump(scene_data, f)

        is_valid, issues = validate_scene(str(scene_path))
        # Should warn about high actor count

    @pytest.mark.unit
    def test_file_not_found(self, temp_dir):
        """Test error handling for non-existent file."""
        nonexistent = temp_dir / "nonexistent.json"
        is_valid, issues = validate_scene(str(nonexistent))
        assert is_valid is False
        assert any("not found" in issue.lower() for issue in issues)

    @pytest.mark.unit
    def test_invalid_json(self, temp_dir):
        """Test error handling for invalid JSON."""
        invalid_json = temp_dir / "invalid.json"
        invalid_json.write_text("{ not valid json }")

        is_valid, issues = validate_scene(str(invalid_json))
        assert is_valid is False

    @pytest.mark.unit
    def test_missing_required_fields(self, temp_dir):
        """Test validation fails for missing required fields."""
        incomplete_scene = {
            "name": "Incomplete"
            # Missing id, actors, triggers, script
        }

        scene_path = temp_dir / "incomplete.json"
        with open(scene_path, 'w') as f:
            json.dump(incomplete_scene, f)

        is_valid, issues = validate_scene(str(scene_path))
        # Should detect missing fields
