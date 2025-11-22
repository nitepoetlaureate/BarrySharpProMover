"""Unit tests for validation scripts."""

import json
import sys
from pathlib import Path

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "scripts" / "validation"))

from check_scene_limits import MAX_ACTORS, MAX_SPRITE_TILES, MAX_TRIGGERS, check_scene


class TestSceneLimitsValidation:
    """Test suite for scene limits validation."""

    def test_scene_within_limits(self, temp_project_dir, capsys):
        """Test scene that meets all limits."""
        scene_data = {
            "actors": [{"id": str(i)} for i in range(10)],  # 10 actors (limit: 20)
            "triggers": [{"id": str(i)} for i in range(15)],  # 15 triggers (limit: 30)
            "spriteTilesUsed": 50  # 50 tiles (limit: 96)
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "All limits OK" in captured.out

    def test_too_many_actors(self, temp_project_dir, capsys):
        """Test scene with too many actors."""
        scene_data = {
            "actors": [{"id": str(i)} for i in range(25)],  # 25 > MAX_ACTORS (20)
            "triggers": [],
            "spriteTilesUsed": 0
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "25 actors" in captured.out
        assert f"limit: {MAX_ACTORS}" in captured.out

    def test_too_many_triggers(self, temp_project_dir, capsys):
        """Test scene with too many triggers."""
        scene_data = {
            "actors": [],
            "triggers": [{"id": str(i)} for i in range(35)],  # 35 > MAX_TRIGGERS (30)
            "spriteTilesUsed": 0
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "35 triggers" in captured.out
        assert f"limit: {MAX_TRIGGERS}" in captured.out

    def test_too_many_sprite_tiles(self, temp_project_dir, capsys):
        """Test scene with too many sprite tiles."""
        scene_data = {
            "actors": [],
            "triggers": [],
            "spriteTilesUsed": 100  # 100 > MAX_SPRITE_TILES (96)
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "100 sprite tiles" in captured.out
        assert f"limit: {MAX_SPRITE_TILES}" in captured.out

    def test_multiple_violations(self, temp_project_dir, capsys):
        """Test scene with multiple limit violations."""
        scene_data = {
            "actors": [{"id": str(i)} for i in range(25)],  # Too many
            "triggers": [{"id": str(i)} for i in range(35)],  # Too many
            "spriteTilesUsed": 100  # Too many
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert "25 actors" in captured.out
        assert "35 triggers" in captured.out
        assert "100 sprite tiles" in captured.out

    def test_missing_fields_use_defaults(self, temp_project_dir, capsys):
        """Test that missing fields default to empty/zero."""
        scene_data = {}  # No actors, triggers, or spriteTilesUsed

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "All limits OK" in captured.out

    def test_at_exact_limits(self, temp_project_dir, capsys):
        """Test scene at exactly the limits (should pass)."""
        scene_data = {
            "actors": [{"id": str(i)} for i in range(MAX_ACTORS)],  # Exactly 20
            "triggers": [{"id": str(i)} for i in range(MAX_TRIGGERS)],  # Exactly 30
            "spriteTilesUsed": MAX_SPRITE_TILES  # Exactly 96
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "✅" in captured.out
        assert "All limits OK" in captured.out

    def test_one_over_limit(self, temp_project_dir, capsys):
        """Test scene one over the limit (should fail)."""
        scene_data = {
            "actors": [{"id": str(i)} for i in range(MAX_ACTORS + 1)],  # 21 actors
            "triggers": [],
            "spriteTilesUsed": 0
        }

        scene_file = temp_project_dir / "test_scene.json"
        scene_file.write_text(json.dumps(scene_data))

        check_scene(str(scene_file))

        captured = capsys.readouterr()
        assert "⚠️" in captured.out
        assert f"{MAX_ACTORS + 1} actors" in captured.out

    def test_invalid_json_handling(self, temp_project_dir):
        """Test error handling for invalid JSON."""
        scene_file = temp_project_dir / "invalid.json"
        scene_file.write_text("{invalid json")

        with pytest.raises(json.JSONDecodeError):
            check_scene(str(scene_file))

    def test_nonexistent_file_handling(self):
        """Test error handling for non-existent file."""
        with pytest.raises(FileNotFoundError):
            check_scene("/nonexistent/scene.json")
