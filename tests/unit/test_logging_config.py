#!/usr/bin/env python3
"""
Unit Tests for logging_config.py

Tests centralized logging configuration including:
- Logger setup
- Log level configuration
- File logging
- Verbose mode
"""

import pytest
import sys
import logging
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'scripts'))

from logging_config import setup_logging, set_verbose


class TestSetupLogging:
    """Test logging setup function."""

    @pytest.mark.unit
    def test_basic_setup(self, temp_dir):
        """Test basic logger setup."""
        logger = setup_logging(
            "test_logger",
            log_level="INFO",
            log_to_file=True,
            log_dir=temp_dir
        )

        assert logger is not None
        assert logger.name == "test_logger"
        assert logger.level == logging.INFO

    @pytest.mark.unit
    def test_log_level_from_env(self, temp_dir, monkeypatch):
        """Test log level from environment variable."""
        monkeypatch.setenv('LOG_LEVEL', 'DEBUG')

        logger = setup_logging(
            "test_logger",
            log_to_file=True,
            log_dir=temp_dir
        )

        assert logger.level == logging.DEBUG

    @pytest.mark.unit
    def test_log_level_default(self, temp_dir, monkeypatch):
        """Test default log level when not specified."""
        monkeypatch.delenv('LOG_LEVEL', raising=False)

        logger = setup_logging(
            "test_logger",
            log_to_file=True,
            log_dir=temp_dir
        )

        assert logger.level == logging.INFO

    @pytest.mark.unit
    def test_file_logging_enabled(self, temp_dir):
        """Test that file logging creates log file."""
        logger = setup_logging(
            "test_file_logger",
            log_to_file=True,
            log_dir=temp_dir
        )

        logger.info("Test message")

        # Check that log file was created
        log_files = list(temp_dir.glob("*.log"))
        assert len(log_files) > 0

    @pytest.mark.unit
    def test_file_logging_disabled(self, temp_dir):
        """Test that file logging can be disabled."""
        logger = setup_logging(
            "test_no_file_logger",
            log_to_file=False,
            log_dir=temp_dir
        )

        logger.info("Test message")

        # Check that no log file was created
        log_files = list(temp_dir.glob("*.log"))
        assert len(log_files) == 0

    @pytest.mark.unit
    def test_console_handler_present(self, temp_dir):
        """Test that console handler is added."""
        logger = setup_logging(
            "test_console",
            log_to_file=False
        )

        # Check that at least one handler is a StreamHandler
        has_console = any(isinstance(h, logging.StreamHandler) and
                          not isinstance(h, logging.FileHandler)
                          for h in logger.handlers)
        assert has_console

    @pytest.mark.unit
    def test_no_propagation(self, temp_dir):
        """Test that logger doesn't propagate to root."""
        logger = setup_logging(
            "test_no_propagate",
            log_to_file=False
        )

        assert logger.propagate is False

    @pytest.mark.unit
    def test_multiple_setup_calls(self, temp_dir):
        """Test that calling setup multiple times doesn't duplicate handlers."""
        logger1 = setup_logging("test_multi", log_to_file=False)
        handler_count1 = len(logger1.handlers)

        logger2 = setup_logging("test_multi", log_to_file=False)
        handler_count2 = len(logger2.handlers)

        # Should have same number of handlers (old ones removed)
        assert handler_count1 == handler_count2


class TestSetVerbose:
    """Test verbose mode function."""

    @pytest.mark.unit
    def test_set_verbose_true(self, temp_dir):
        """Test enabling verbose mode."""
        logger = setup_logging("test_verbose", log_level="INFO", log_to_file=False)

        assert logger.level == logging.INFO

        set_verbose(logger, verbose=True)

        assert logger.level == logging.DEBUG

    @pytest.mark.unit
    def test_set_verbose_false(self, temp_dir):
        """Test that verbose=False doesn't change level."""
        logger = setup_logging("test_not_verbose", log_level="INFO", log_to_file=False)

        original_level = logger.level
        set_verbose(logger, verbose=False)

        assert logger.level == original_level

    @pytest.mark.unit
    def test_verbose_affects_handlers(self, temp_dir):
        """Test that verbose mode affects handler levels."""
        logger = setup_logging("test_handler_verbose", log_to_file=False)

        set_verbose(logger, verbose=True)

        # Check that StreamHandler was set to DEBUG
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                assert handler.level == logging.DEBUG
