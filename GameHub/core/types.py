from __future__ import annotations
from typing import Any, Dict, Hashable, Mapping

PlayerID = Hashable


Action = Any


JointAction = Mapping[PlayerID,Action]


Reward = float


Result = Mapping[PlayerID,Reward]


State = Any








