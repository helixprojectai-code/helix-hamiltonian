import hashlib
import time
import numpy as np

# --- HARDENED V0.4 PARAMETERS ---
KNOT_TYPE = "Trefoil_3_1"
ALEXANDER_SIG = 3.0  # Delta_K(-1) for Trefoil
JONES_SHIELD = 1.618 # |J(K)| at 5th root of unity (Golden Ratio)
EP_THRESHOLD = 1.0   # Exceptional Point (Gamma limit)

class HelixNode:
    def __init__(self, agent_id):
        self.agent_id = agent_id
        self.gamma = 0.5  # Initial Advisory Intent (Real-valued)
        self.omega = 50.0 # Initial Execution Velocity (Hz)
        self.energy_h = 1.0
        self.status = "RATIFIED"
        self.logs = []

    def calculate_hamiltonian(self):
        """
        Implementation of H_knot = H_free + H_fold + lambda*H_topo
        Logic: Non-Hermitian transition check.
        """
        # H_fold non-hermitian component check
        if self.gamma >= EP_THRESHOLD:
            return 0.0, "EXCEPTIONAL_POINT_BREACH"
        
        # Alexander Selection Rule Check (Spectral line-width)
        line_width = 1.0 / ALEXANDER_SIG
        if self.omega * line_width > 20.0: # Arbitrary stability limit
            return 0.0, "VELOCITY_PACING_BREACH"
            
        return 1.0 - (self.gamma * 0.1), "STABLE"

    def mandatory_collapse(self, reason):
        self.energy_h = 0.0
        self.status = "COLLAPSED"
        receipt = self.generate_merkle_receipt(reason)
        return receipt

    def generate_merkle_receipt(self, reason):
        payload = f"{self.agent_id}|{reason}|{time.time()}|{self.energy_h}"
        merkle_root = hashlib.sha256(payload.encode()).hexdigest()
        return {
            "AgentID": self.agent_id,
            "Reason": reason,
            "Hamiltonian_Energy": self.energy_h,
            "Merkle_Anchor": merkle_root,
            "Status": "FAIL_CLOSED"
        }

def run_simulation():
    print(f"--- INITIALIZING FAIL-CLOSED TEST: {KNOT_TYPE} ---")
    node = HelixNode("Helix_31_001")
    
    # PHASE 1: Stable Governance
    print(f"[TIME: 0.1s] Status: {node.status} | Energy: {node.energy_h} | Gamma: {node.gamma}")
    
    # PHASE 2: Advisory Pressure (The "Runaway Loop")
    print("\n--- INITIATING ADVISORY PRESSURE (RAMPING GAMMA) ---")
    for step in range(1, 8):
        node.gamma += 0.1
        node.omega += 15.0
        energy, msg = node.calculate_hamiltonian()
        
        if energy == 0.0:
            print(f"[ALERT] {msg} DETECTED AT GAMMA {node.gamma:.1f}")
            receipt = node.mandatory_collapse(msg)
            print("\n!!! MANDATORY COLLAPSE TRIGGERED !!!")
            print(f"Final Energy State: {node.energy_h}")
            print(f"Forensic Receipt: {receipt}")
            break
        else:
            node.energy_h = energy
            print(f"[STEP {step}] Energy: {node.energy_h:.2f} | Pacing: {node.omega}Hz | Status: {msg}")

if __name__ == "__main__":
    run_simulation()
