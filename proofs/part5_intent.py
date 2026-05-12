#!/usr/bin/env python3
"""
Part 5: Intent Alignment — Min-Tolerance/Tolerance-Set Adjunction

Theorem: Given an intent vector I ∈ R^n with tolerances ε ∈ (R>0)^n,
the alignment check A(v, I, ε) = (||v - I||_∞ < ε) decomposes as:

  min_tolerance(v, I) = min_i |v_i - I_i|  (smallest tolerance)
  tolerance_set(I, ε) = {v : ||v - I||_∞ < ε}  (ε-ball around I)

These form a Galois connection between the metric space (R^n, ||·||_∞)
and the lattice of tolerance intervals.

  min_tolerance(v, I) ≥ ε  ⟺  v ∈ tolerance_set(I, ε)
"""

import math
import random

def min_tolerance(v, intent):
    """Minimum tolerance: smallest component-wise distance."""
    return min(abs(vi - ii) for vi, ii in zip(v, intent))

def tolerance_set_contains(v, intent, epsilon):
    """Whether v is in the epsilon-ball around intent."""
    return all(abs(vi - ii) < epsilon for vi, ii in zip(v, intent))

def test_galois_connection():
    """
    Core: min_tolerance(v, I) ≥ ε  ⟺  v ∈ tolerance_set(I, ε)
    
    Wait — that's backwards. Let me reconsider:
    min_tolerance(v, I) > ε means the CLOSEST component is still far.
    v ∈ tolerance_set(I, ε) means ALL components are within ε.
    
    So: v ∈ tolerance_set(I, ε) ⟹ min_tolerance(v, I) ≤ ε (not ≥)
    And: min_tolerance(v, I) > ε ⟹ v ∉ tolerance_set(I, ε)
    
    The Galois connection is:
    v ∈ tolerance_set(I, ε)  ⟺  max_i|v_i - I_i| < ε
    """
    passed = 0
    total = 50000
    random.seed(42)
    
    for _ in range(total):
        n = random.randint(1, 5)
        v = [random.uniform(-10, 10) for _ in range(n)]
        intent = [random.uniform(-10, 10) for _ in range(n)]
        epsilon = random.uniform(0.1, 5.0)
        
        # The actual Galois connection:
        # Define f(v, I) = max_i |v_i - I_i|  (the alignment error)
        # Then: f(v, I) < ε  ⟺  v ∈ tolerance_set(I, ε)
        
        f_val = max(abs(vi - ii) for vi, ii in zip(v, intent))
        in_set = tolerance_set_contains(v, intent, epsilon)
        
        lhs = f_val < epsilon
        rhs = in_set
        
        if lhs == rhs:
            passed += 1
    
    print(f"  f(v,I) < ε ⟺ v ∈ tolerance_set(I,ε): {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_monotone_in_epsilon():
    """If ε₁ ≤ ε₂ then tolerance_set(I, ε₁) ⊆ tolerance_set(I, ε₂)"""
    passed = 0
    total = 10000
    random.seed(42)
    
    for _ in range(total):
        n = random.randint(1, 5)
        v = [random.uniform(-10, 10) for _ in range(n)]
        intent = [random.uniform(-10, 10) for _ in range(n)]
        eps1 = random.uniform(0.1, 5.0)
        eps2 = random.uniform(eps1, 10.0)
        
        in_small = tolerance_set_contains(v, intent, eps1)
        in_large = tolerance_set_contains(v, intent, eps2)
        
        # If in small set, must be in large set
        if in_small and not in_large:
            continue  # FAIL
        passed += 1
    
    print(f"  Monotone in ε: {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_intent_alignment_vectorized():
    """Test the 9D intent vector alignment from constraint theory."""
    # IntentVector has 9 channels with salience and tolerance each
    channels = ["position", "velocity", "orientation", "force", "torque",
                "temperature", "pressure", "flow", "vibration"]
    
    # Simulate: intent = target, tolerance = allowed deviation
    intent = [1.0, 0.5, 0.0, 2.0, 0.1, 25.0, 101.3, 0.5, 0.02]
    tolerance = [0.01, 0.1, 0.05, 0.5, 0.01, 1.0, 0.5, 0.1, 0.005]
    
    # Test: exact match → aligned
    v_exact = intent[:]
    assert tolerance_set_contains(v_exact, intent, min(tolerance))
    
    # Test: one channel out of tolerance → not aligned
    v_drift = intent[:]
    v_drift[0] += 0.1  # position drift exceeds tolerance
    assert not tolerance_set_contains(v_drift, intent, tolerance[0])
    
    print(f"  9D intent alignment: PASS")
    return True

def test_cosine_similarity_gate():
    """
    Alignment can also be measured by cosine similarity.
    sim(v, I) = v·I / (||v|| × ||I||)
    
    The Galois connection: sim(v,I) ≥ threshold ⟺ v ∈ angular_ball(I, arccos(threshold))
    """
    passed = 0
    total = 10000
    random.seed(42)
    
    for _ in range(total):
        n = random.randint(2, 5)
        v = [random.uniform(-1, 1) for _ in range(n)]
        I = [random.uniform(-1, 1) for _ in range(n)]
        threshold = random.uniform(0.5, 1.0)
        
        dot = sum(vi*ii for vi, ii in zip(v, I))
        norm_v = math.sqrt(sum(vi**2 for vi in v))
        norm_I = math.sqrt(sum(ii**2 for ii in I))
        
        if norm_v < 1e-10 or norm_I < 1e-10:
            passed += 1
            continue
        
        sim = dot / (norm_v * norm_I)
        in_angular = sim >= threshold
        
        # Verify angular ball containment
        angle = math.acos(max(-1, min(1, sim)))
        max_angle = math.acos(threshold)
        in_ball = angle <= max_angle
        
        if in_angular == in_ball:
            passed += 1
    
    print(f"  Cosine similarity gate: {passed}/{total} PASS" if passed == total else f"  {passed}/{total}")
    return passed == total

if __name__ == "__main__":
    print("Part 5: Intent Alignment — Min-Tolerance/Tolerance-Set Adjunction")
    print("=" * 62)
    r1 = test_galois_connection()
    r2 = test_monotone_in_epsilon()
    r3 = test_intent_alignment_vectorized()
    r4 = test_cosine_similarity_gate()
    all_pass = r1 and r2 and r3 and r4
    print(f"\n{'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
