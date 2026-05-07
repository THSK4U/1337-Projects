from pydantic import BaseModel
from typing import Any, Dict


class FunctionParameter(BaseModel):
    """Class for 1 parameter as type"""

    type: str


class FunctionDefinition(BaseModel):
    """Function Structur"""

    name: str
    description: str
    parameters: Dict[str, FunctionParameter]


class TestPrompt(BaseModel):
    """user prompet"""

    prompt: str


class FunctionCallResult(BaseModel):
    """Final Output"""

    prompt: str
    name: str
    parameters: Dict[str, Any]
