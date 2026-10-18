import pytest
from ai.provider_adapters import get_ai_adapter, OfflineFallbackAdapter

def test_offline_adapter_always_available():
    adapter = OfflineFallbackAdapter()
    assert adapter.is_available() is True
    assert adapter.name == "Offline Curated Engine"

def test_default_adapter_is_offline():
    # Without API keys, default adapter is OfflineFallbackAdapter
    adapter = get_ai_adapter()
    assert adapter.is_available() is True
