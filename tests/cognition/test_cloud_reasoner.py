"""Tests for the offline-safe cloud reasoning entry point."""

from unittest.mock import Mock

from pytest import MonkeyPatch

from mitsu.cognition.cloud_reasoner import DisabledReasoner, OpenAIReasoner
from mitsu.cognition.tool_registry import ToolRegistry
from mitsu.config import CloudSettings


def test_disabled_configuration_never_creates_a_cloud_reasoner(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "not-a-real-key")

    reasoner = OpenAIReasoner.from_environment(
        settings=CloudSettings(enabled=False),
        tool_registry=Mock(spec=ToolRegistry),
    )

    assert isinstance(reasoner, DisabledReasoner)

    result = reasoner.resolve("put Discord on the left")

    assert not result.available
    assert not result.used_cloud
    assert result.message == "Cloud reasoning is unavailable. Use a supported command."
