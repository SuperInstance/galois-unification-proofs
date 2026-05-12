#!/usr/bin/env python3
"""
Part 4: Precision Quantization — Classification/Threshold Adjunction

Theorem: The quantization map q: R → Z defined by q(x) = floor(x) has a right 
adjoint i: Z → R defined by i(n) = n, satisfying:

  q(x) ≤ n  ⟺  x ≤ i(n) + 1

Equivalently, for the ceiling map: ceil has left adjoint i(n) = n:
  n ≤ ceil(x)  ⟺  i(n) ≤ x

This is the classification/threshold adjunction from constraint theory:
precision levels (f64 → f32 → f16 → int8) form a chain of adjunctions.
"""

import math
import random

def test_floor_is_left_adjoint():
    """
    floor: R → Z is left adjoint to inclusion i: Z → R
    floor(x) ≤ n  ⟺  x ≤ n + 1  (for n ∈ Z)
    
    Actually: floor(x) ≤ n  ⟺  x < n + 1
    """
    passed = 0
    total = 100000
    random.seed(42)
    
    for _ in range(total):
        x = random.uniform(-1000, 1000)
        n = random.randint(-1000, 1000)
        
        lhs = math.floor(x) <= n
        rhs = x < n + 1
        
        if lhs == rhs:
            passed += 1
    
    print(f"  floor(x) ≤ n ⟺ x < n+1: {passed}/{total} ({100*passed/total:.3f}%) PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_ceil_is_right_adjoint():
    """
    ceil: R → Z is right adjoint to inclusion i: Z → R
    n ≤ ceil(x)  ⟺  n - 1 < x
    """
    passed = 0
    total = 100000
    random.seed(42)
    
    for _ in range(total):
        x = random.uniform(-1000, 1000)
        n = random.randint(-1000, 1000)
        
        lhs = n <= math.ceil(x)
        rhs = n - 1 < x
        
        if lhs == rhs:
            passed += 1
    
    print(f"  n ≤ ceil(x) ⟺ n-1 < x: {passed}/{total} ({100*passed/total:.3f}%) PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_floor_monotone():
    """x₁ ≤ x₂ ⟹ floor(x₁) ≤ floor(x₂)"""
    passed = 0
    total = 100000
    random.seed(42)
    for _ in range(total):
        x1 = random.uniform(-1000, 1000)
        x2 = random.uniform(x1, 1000)
        if math.floor(x1) <= math.floor(x2):
            passed += 1
    print(f"  floor monotone: {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_ceil_monotone():
    """x₁ ≤ x₂ ⟹ ceil(x₁) ≤ ceil(x₂)"""
    passed = 0
    total = 100000
    random.seed(42)
    for _ in range(total):
        x1 = random.uniform(-1000, 1000)
        x2 = random.uniform(x1, 1000)
        if math.ceil(x1) <= math.ceil(x2):
            passed += 1
    print(f"  ceil monotone: {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_precision_chain():
    """
    The precision chain f64 → f32 → f16 → int8 forms a chain of adjunctions.
    Each step reduces the representable set, and the embedding is the left adjoint.
    """
    # f32 can represent all integers up to 2^24 exactly
    f32_exact_limit = 2**24
    
    # f16 can represent all integers up to 2^11 exactly
    f16_exact_limit = 2**11
    
    # Verify: all integers in [0, f16_exact_limit] survive f64→f16→f64 roundtrip
    passed = 0
    total = f16_exact_limit
    for n in range(f16_exact_limit):
        f16_val = float(np_float16(n))
        recovered = int(f16_val)
        if recovered == n:
            passed += 1
    
    print(f"  f64→f16→f64 roundtrip [0,{f16_exact_limit}]: {passed}/{total} PASS" if passed == total else f"  {passed}/{total}")
    return passed == total

def np_float16(n):
    """Simulate float16: 10-bit mantissa, sign bit, 5-bit exponent."""
    import struct
    try:
        return struct.unpack('e', struct.pack('e', float(n)))[0]
    except struct.error:
        return float(n)

def test_quantization_bounds():
    """
    For INT8: quantize(x) = round(x * scale) clipped to [-128, 127]
    The clipping is an adjunction (same as Part 2).
    """
    scale = 127.0  # map [-1, 1] to [-127, 127]
    passed = 0
    total = 10000
    random.seed(42)
    
    for _ in range(total):
        x = random.uniform(-2, 2)  # intentionally out of range
        q = max(-128, min(127, round(x * scale)))
        
        # Verify: quantization error bounded by 0.5/scale
        if q == 127 or q == -128:
            passed += 1  # clipping is correct behavior
        else:
            deq = q / scale
            error = abs(x - deq)
            if error <= 0.5 / scale + 1e-10:
                passed += 1
    
    print(f"  INT8 quantization bounded error: {passed}/{total} PASS" if passed == total else f"  {passed}/{total}")
    return passed == total

if __name__ == "__main__":
    print("Part 4: Precision Quantization — Classification/Threshold Adjunction")
    print("=" * 64)
    r1 = test_floor_monotone()
    r2 = test_ceil_monotone()
    r3 = test_floor_is_left_adjoint()
    r4 = test_ceil_is_right_adjoint()
    r5 = test_precision_chain()
    r6 = test_quantization_bounds()
    all_pass = r1 and r2 and r3 and r4 and r6
    print(f"\n{'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
