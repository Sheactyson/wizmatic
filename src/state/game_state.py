from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class InitiativeState:
    side: Optional[str] = None  # "allies" or "enemies"
    sun_score: float = 0.0
    dagger_score: float = 0.0
    profile: Optional[str] = None


@dataclass
class TurnOrderSlot:
    index: int
    rel_roi: Tuple[float, float, float, float]
    active_score: Optional[float] = None
    is_active: Optional[bool] = None
    actor: str = "unknown"
    confidence: float = 0.0


@dataclass
class TurnOrderState:
    order: List[str] = field(default_factory=list)
    source: Optional[str] = None  # e.g. "initiative", "vision"
    detected: bool = False
    rel_roi: Optional[Tuple[float, float, float, float]] = None
    slots: List[TurnOrderSlot] = field(default_factory=list)
    active_index: Optional[int] = None
    active_confidence: float = 0.0
    timestamp: Optional[float] = None


@dataclass
class BattleState:
    in_card_select: bool = False
    initiative: InitiativeState = field(default_factory=InitiativeState)
    turn_order: TurnOrderState = field(default_factory=TurnOrderState)


@dataclass
class GameState:
    updated_at: float = 0.0
    battle: BattleState = field(default_factory=BattleState)
