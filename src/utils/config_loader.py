import os
import json
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

try:
    import yaml
    YAML_AVAILABLE = True
except ImportError:
    YAML_AVAILABLE = False

# Load environment variables from .env (if present)
load_dotenv()


def load_json_config(path: str) -> Dict[str, Any]:
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)


def load_yaml_config(path: str) -> Dict[str, Any]:
    if not YAML_AVAILABLE:
        raise ImportError("PyYAML is not installed. Run `pip install pyyaml`.")
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def load_config(config_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads configuration from .env, JSON, or YAML file.
    Returns a merged dictionary with env variables taking precedence.
    """
    config: Dict[str, Any] = {}

    # Detect config file
    if config_path:
        config_file = Path(config_path)
    else:
        config_file = Path("config.json")
        if not config_file.exists():
            config_file = Path("config.yaml") if Path("config.yaml").exists() else None

    # Load file-based config
    if config_file:
        if config_file.suffix == ".json":
            config.update(load_json_config(str(config_file)))
        elif config_file.suffix in [".yml", ".yaml"]:
            config.update(load_yaml_config(str(config_file)))
        else:
            raise ValueError(f"Unsupported config file format: {config_file}")

    # Override with environment variables
    for key, value in os.environ.items():
        if key.startswith("APP_"):  # Only pull prefixed envs
            config_key = key.replace("APP_", "")
            config[config_key] = value

    return config


def get_config_value(key: str, default: Any = None) -> Any:
    """
    Convenience accessor for single config value with fallback.
    """
    return os.getenv(f"APP_{key}") or load_config().get(key, default)

