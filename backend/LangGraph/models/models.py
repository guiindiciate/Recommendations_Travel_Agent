from typing_extensions import TypedDict
from typing import Annotated
import operator

class AgentState(TypedDict):
    query: dict
    recc: Annotated[list, operator.add]