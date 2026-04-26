import pytest

from modules.model_loader import MODEL_PATHS, model_exists, load_digit_model
from modules.model_loader import get_available_models


def test_known_models_exist_in_mapping():
    assert "mnist" in MODEL_PATHS
    assert "custom" in MODEL_PATHS


def test_unknown_model_does_not_exist():
    assert model_exists("does_not_exist") is False


def test_loading_unknown_model_raises_value_error():
    with pytest.raises(ValueError):
        load_digit_model("does_not_exist")
        
        
def test_get_available_models_returns_list():
    result = get_available_models()
    
    assert isinstance(result, list)
