import pytest
from helix_hamiltonian.authority import ratify_velocity

def test_ratify_velocity_quebec():
    assert ratify_velocity("EXECUTE", "CUSTODIAN_QC", "CA-QC") == "EXECUTE"
    assert ratify_velocity("STOP", "POLICY_QC", "CA-QC") == "PAUSE"
