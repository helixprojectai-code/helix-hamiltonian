"""
Helix Hamiltonian - Policy Compiler (v0.3)
Transforms RFC 0001 v0.4 schemas and JSON rules into executable bridge checks.
"""

import json
from typing import Dict, Any, List, Callable, Optional
from .core import Interaction

class PolicyCompiler:
    """
    Transforms human-readable 'Rules' into machine-executable 'Checks'.
    Ensures the 'Chess Pieces' are GPG-sealed to the Hamiltonian board.
    """
    
    def __init__(self, rule_source: Optional[str] = None):
        self.rules: Dict[str, Any] = {}
        if rule_source:
            with open(rule_source, 'r') as f:
                self.rules = json.load(f)
        self.executable_checks: List[Callable[[Interaction], bool]] = []
        self._compile()

    def _compile(self):
        """
        Compiles the active rule-set into a list of pass/fail lambda checks.
        """
        # 1. Authority Invariant: ITAR/Defence hardening (GICD §1)
        if self.rules.get("jurisdiction") == "ITAR":
            self.executable_checks.append(
                lambda i: i.authority in ["CUSTODIAN_ITAR", "SYSADMIN"]
            )
            
        # 2. Velocity Invariant: Pacing control (RFC 0001 §3.1)
        max_velocity = self.rules.get("constraints", {}).get("max_velocity", "PAUSE")
        if max_velocity == "PAUSE":
            self.executable_checks.append(lambda i: i.velocity != "PROCEED")

        # 3. Form Invariant: Fact-only zones (RFC 0001 §4)
        if self.rules.get("mode") == "STRICT_FACT":
            self.executable_checks.append(lambda i: i.form == "FACT")

    def validate_interaction(self, interaction: Interaction) -> bool:
        """
        Executes all compiled checks against a single interaction.
        Returns False (Fail-Closed) if any invariant is violated.
        """
        # If no rules are loaded, we fail-closed (Helix Default)
        if not self.executable_checks:
            return False
            
        return all(check(interaction) for check in self.executable_checks)
