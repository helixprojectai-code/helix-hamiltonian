# helix-hamiltonian/src/helix_hamiltonian/authority.py
from enum import Enum, auto
from typing import Dict, Optional


class AuthorityLevel(Enum):
    """Hierarchical authority levels (RFC 0001 v4 §6)."""

    CUSTODIAN = auto()  # Sovereign human/keyholder
    POLICY = auto()  # System constraint layer
    ADVISORY = auto()  # Model recommendation


# Canadian jurisdictional authority mappings
CANADIAN_AUTHORITY_MAPPING: Dict[str, list] = {
    # Federal
    "CUSTODIAN_CA_FED": ["TBS", "RCMP", "CSE"],
    "POLICY_CA_FED": ["GC_AUDIT", "TBS_POLICY"],
    # Defence
    "CUSTODIAN_CA_DEFENCE": ["DND", "CSE"],
    "POLICY_CA_DEFENCE": ["CPCSC", "ITAR"],
    # Privacy
    "CUSTODIAN_CA_PRIVACY": ["OPC"],
    "POLICY_CA_PRIVACY": ["PIPEDA", "LAW_25"],
    # Quebec
    "CUSTODIAN_QC": ["CAI"],
    "POLICY_QC": ["LAW_25"],
    # Indigenous
    "CUSTODIAN_INDIGENOUS": ["FN_OCAP"],
    # Cross-border
    "CUSTODIAN_ITAR": ["US_DDTC"],
}

# Bilingual localization (English/French)
AUTHORITY_LOCALIZATION: Dict[str, Dict[str, str]] = {
    "CUSTODIAN": {"en": "CUSTODIAN", "fr": "DÉPOSITAIRE"},
    "POLICY": {"en": "POLICY", "fr": "POLITIQUE"},
    "ADVISORY": {"en": "ADVISORY", "fr": "CONSULTATIF"},
    "CUSTODIAN_CA_DEFENCE": {
        "en": "CUSTODIAN (National Defence)",
        "fr": "DÉPOSITAIRE (Défense nationale)",
    },
    "CUSTODIAN_QC": {"en": "CUSTODIAN (Quebec)", "fr": "DÉPOSITAIRE (Québec)"},
}


def ratify_velocity(
    model_recommended_velocity: str, authority: str, jurisdiction: Optional[str] = None
) -> str:
    """
    Enforce the Ratification Rule (RFC 0001 v4 §6.2).
    - Model recommendations are advisory until ratified by CUSTODIAN or POLICY.
    - CUSTODIAN > POLICY > ADVISORY.
    - Jurisdiction-specific defaults (e.g., PAUSE for CA-QC).
    """
    if jurisdiction == "CA-QC" and authority.startswith("CUSTODIAN"):
        return model_recommended_velocity  # Quebec custodians have full authority

    if authority.startswith("CUSTODIAN"):
        return model_recommended_velocity
    elif authority.startswith("POLICY"):
        return (
            model_recommended_velocity
            if model_recommended_velocity != "STOP"
            else "PAUSE"
        )
    else:  # ADVISORY
        return "PAUSE"  # Default to PAUSE for advisory
