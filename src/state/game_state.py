from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Tuple


@dataclass
class InitiativeState:
    side: Optional[str] = None  # "allies" or "enemies"
    sun_score: float = 0.0
    dagger_score: float = 0.0
    sun_off_score: float = 0.0
    dagger_off_score: float = 0.0
    profile: Optional[str] = None
    method: Optional[str] = None


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
class PipInventory:
    tokens: List[str] = field(default_factory=list)
    normal: int = 0
    power: int = 0
    school: int = 0

    @property
    def total(self) -> int:
        return self.normal + self.power + self.school

    @property
    def total(self) -> int:
        return self.normal + self.power + self.school


@dataclass
class ParticipantState:
    side: str = "unknown"  # "enemy" or "ally"
    index: int = -1
    rel_roi: Tuple[float, float, float, float] = (0.0, 0.0, 0.0, 0.0)
    sigil: Optional[str] = None
    sigil_score: Optional[float] = None
    name: Optional[str] = None
    name_raw: Optional[str] = None
    health_current: Optional[int] = None
    health_max: Optional[int] = None
    school: Optional[str] = None
    school_score: Optional[float] = None
    pips: PipInventory = field(default_factory=PipInventory)
    occupied: bool = False
    empty_reason: Optional[str] = None
    name_roi: Optional[Tuple[float, float, float, float]] = None
    health_roi: Optional[Tuple[float, float, float, float]] = None
    pips_roi: Optional[Tuple[float, float, float, float]] = None
    sigil_roi: Optional[Tuple[float, float, float, float]] = None
    school_roi: Optional[Tuple[float, float, float, float]] = None


@dataclass
class ParticipantsState:
    enemies: List[ParticipantState] = field(default_factory=list)
    allies: List[ParticipantState] = field(default_factory=list)
    profile: Optional[str] = None
    detected: bool = False
    timestamp: Optional[float] = None


@dataclass
class BattleState:
    in_card_select: bool = False
    initiative: InitiativeState = field(default_factory=InitiativeState)
    turn_order: TurnOrderState = field(default_factory=TurnOrderState)
    participants: ParticipantsState = field(default_factory=ParticipantsState)


@dataclass
class GameState:
    updated_at: float = 0.0
    battle: BattleState = field(default_factory=BattleState)
