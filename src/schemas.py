from pydantic import BaseModel
from typing import Dict, Any


class ParameterDetail(BaseModel):
    type: str


class FunctionsDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, ParameterDetail]
    returns: Dict[str, str]


class FunctionCallingTests(BaseModel):
    prompt: str


class FunctionCallingResults(BaseModel):
    prompt: str
    name: str
    parameters: Dict[str, Any]
