#!/usr/bin/env python3
"""
Tests for the enhanced Hello World app.
"""

import pytest
from click.testing import CliRunner
from main import hello, get_random_fact


def test_hello_simple():
    """Test simple greeting without fact."""
    runner = CliRunner()
    result = runner.invoke(hello, ["--style", "simple"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output


def test_hello_with_name():
    """Test greeting with custom name."""
    runner = CliRunner()
    result = runner.invoke(hello, ["--name", "DevContainer", "--style", "simple"])
    assert result.exit_code == 0
    assert "Hello, DevContainer!" in result.output


def test_hello_with_fact():
    """Test greeting with random fact."""
    runner = CliRunner()
    result = runner.invoke(hello, ["--fact", "--style", "simple"])
    assert result.exit_code == 0
    assert "Hello, World!" in result.output
    assert "Fun fact:" in result.output


def test_get_random_fact():
    """Test that get_random_fact returns a string."""
    fact = get_random_fact()
    assert isinstance(fact, str)
    assert len(fact) > 0


def test_fancy_output():
    """Test fancy output mode runs without error."""
    runner = CliRunner()
    result = runner.invoke(hello, ["--style", "fancy"])
    assert result.exit_code == 0