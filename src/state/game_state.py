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
    stable_side: Optional[str] = None
    stable_since: Optional[float] = None
    last_checked_at: Optional[float] = None


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
    name_time_ms: Optional[float] = None
    name_time_parts: Optional[Tuple[float, float, float, float]] = None
    name_roi_hash: Optional[int] = None
    name_ocr: bool = False
    details_checked_at: Optional[float] = None
    health_current: Optional[int] = None
    health_max: Optional[int] = None
    school: Optional[str] = None
    school_score: Optional[float] = None
    pips: PipInventory = field(default_factory=PipInventory)
    slot_active: bool = False
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
    occupancy_checked_at: Optional[float] = None


@dataclass
class PlayerWizardState:
    detected: bool = False
    matched: bool = False
    side: str = "ally"
    slot_index: Optional[int] = None
    slot_sigil: Optional[str] = None
    slot_confirm_streak: int = 0
    slot_locked: bool = False
    name: Optional[str] = None
    school: Optional[str] = None
    pips: PipInventory = field(default_factory=PipInventory)
    health_current: Optional[int] = None
    health_max: Optional[int] = None
    mana_current: Optional[int] = None
    mana_max: Optional[int] = None
    energy_current: Optional[int] = None
    energy_max: Optional[int] = None
    health_raw: Optional[str] = None
    mana_raw: Optional[str] = None
    energy_raw: Optional[str] = None
    health_roi: Optional[Tuple[float, float, float, float]] = None
    mana_roi: Optional[Tuple[float, float, float, float]] = None
    energy_roi: Optional[Tuple[float, float, float, float]] = None
    matched_by: Optional[str] = None  # e.g. "health"
    timestamp: Optional[float] = None


@dataclass
class PlayerHandState:
    detected: bool = False
    cards_in_hand: Optional[int] = None
    slot_score: float = 0.0
    slot_center_px: Optional[Tuple[int, int]] = None
    slot_center_rel: Optional[Tuple[float, float]] = None
    slot_roi: Optional[Tuple[float, float, float, float]] = None
    profile: Optional[str] = None
    timestamp: Optional[float] = None


@dataclass
class BattleState:
    active: bool = False
    in_card_select: bool = False
    card_select_started_at: Optional[float] = None
    initial_card_select_done: bool = False
    initiative: InitiativeState = field(default_factory=InitiativeState)
    turn_order: TurnOrderState = field(default_factory=TurnOrderState)
    participants: ParticipantsState = field(default_factory=ParticipantsState)
    player_wizard: PlayerWizardState = field(default_factory=PlayerWizardState)
    player_hand: PlayerHandState = field(default_factory=PlayerHandState)


@dataclass
class GameState:
    updated_at: float = 0.0
    state: str = "idle"
    battle: BattleState = field(default_factory=BattleState)
