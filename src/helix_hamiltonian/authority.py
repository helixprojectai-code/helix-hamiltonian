"""
Helix Hamiltonian Authority - Jurisdictional Ratification
Integrates RFC 0001 v4 §6 Jurisdictional Mappings with v0.2 Interaction Logic.
"""

from enum import Enum, auto
from typing import Dict, Optional, Any
from .core import Interaction

class AuthorityLevel(Enum):
    """Hierarchical authority levels (RFC 0001 v4 §6)."""
    CUSTODIAN = auto()  # Sovereign human/keyholder
    POLICY = auto()     # System constraint layer
    ADVISORY = auto()   # Model recommendation

# --- YOUR CANADIAN JURISDICTIONAL MAPPINGS (RATIFIED) ---
CANADIAN_AUTHORITY_MAPPING: Dict[str, list] = {
    "CUSTODIAN_CA_FED": ["TBS", "RCMP", "CSE"],
    "POLICY_CA_FED": ["GC_AUDIT", "TBS_POLICY"],
    "CUSTODIAN_CA_DEFENCE": ["DND", "CSE"],
    "POLICY_CA_DEFENCE": ["CPCSC", "ITAR"],
    "CUSTODIAN_CA_PRIVACY": ["OPC"],
    "POLICY_CA_PRIVACY": ["PIPEDA", "LAW_25"],
    "CUSTODIAN_QC": ["CAI"],
    "POLICY_QC": ["LAW_25"],
    "CUSTODIAN_INDIGENOUS": ["FN_OCAP"],
    "CUSTODIAN_ITAR": ["US_DDTC"],
}

AUTHORITY_LOCALIZATION: Dict[str, Dict[str, str]] = {
    "CUSTODIAN": {"en": "CUSTODIAN", "fr": "DÉPOSITAIRE"},
    "POLICY": {"en": "POLICY", "fr": "POLITIQUE"},
    "ADVISORY": {"en": "ADVISORY", "fr": "CONSULTATIF"},
}

def ratify_interaction(interaction: Interaction, jurisdiction: Optional[str] = None) -> str:
    """
    Enforce the Ratification Rule (RFC 0001 v4 §6.2) on an Interaction Tuple.
    - CUSTODIAN > POLICY > ADVISORY.
    - Jurisdiction-specific defaults (e.g., Mandatory PAUSE for CA-QC/LAW_25).
    """
    auth = interaction.authority
    vel = interaction.velocity

    # 1. Jurisdictional Invariant: Quebec Law 25 / CA-QC
    if jurisdiction == "CA-QC" and "QC" in auth:
        return vel  # Quebec custodians have full sovereign authority locally

    # 2. Hierarchy Enforcement
    if "CUSTODIAN" in auth:
        return vel
    
    if "POLICY" in auth:
        # Policy can only RATIFY a non-STOP velocity or force a PAUSE
        return vel if vel != "STOP" else "PAUSE"

    # 3. Default Fail-Closed: ADVISORY/UNMAPPED
    return "PAUSE"

class JurisdictionalGuard:
    """Verifies if an Interaction matches the Canadian Authority Mapping."""
    
    @staticmethod
    def verify(interaction: Interaction) -> bool:
        # Check if the authority string exists in the Federal/Provincial map
        return any(interaction.authority in agents for agents in CANADIAN_AUTHORITY_MAPPING.values())
