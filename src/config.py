from pathlib import Path
from typing import Dict, Any, Optional
import yaml
from pydantic import BaseModel, Field

class InputConfig(BaseModel):
    source_type: str = Field(..., pattern="^(csv|json|api)$")
    file_path: Optional[str] = None
    api_url: Optional[str] = None

class CleaningConfig(BaseModel):
    drop_duplicates: bool = True
    type_conversions: Dict[str, str] = Field(default_factory=dict)
    missing_value_strategies: Dict[str, Any] = Field(default_factory=dict)
    fill_values: Dict[str, Any] = Field(default_factory=dict)
    fill_string_values: Dict[str, str] = Field(default_factory=dict)

class OutputConfig(BaseModel):
    file_path: str
    format: str = Field("csv", pattern="^(csv|json)$")

class PipelineConfig(BaseModel):
    name: str
    input: InputConfig
    cleaning: CleaningConfig
    output: OutputConfig

def load_config(config_path: str = "config/pipeline_config.yaml") -> PipelineConfig:
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found at: {config_path}")
    
    with open(path, "r", encoding="utf-8") as f:
        raw_config = yaml.safe_load(f)
        
    p_config = raw_config.get("pipeline", {})
    return PipelineConfig(
        name=p_config.get("name", "Data Pipeline"),
        input=InputConfig(**raw_config.get("input", {})),
        cleaning=CleaningConfig(**raw_config.get("cleaning", {})),
        output=OutputConfig(**raw_config.get("output", {}))
    )