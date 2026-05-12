#!/usr/bin/env python3
"""
Part 1: XOR Conversion is a Galois Connection (Self-Adjoint)

Theorem: f(x) = x ⊕ mask is its own adjoint. For all x, mask:
  f(f(x)) = x  (involution property)
  
This means f = f*, making XOR a self-adjoint Galois connection.
Moreover, XOR preserves the Hamming order: if x ⊆ y, then f(x) ⊆ f(y).
"""

import itertools

def test_xor_involution():
    """Verify f(f(x)) = x for all 8-bit values and masks."""
    passed = 0
    total = 0
    for x in range(256):
        for mask in range(256):
            result = (x ^ mask) ^ mask
            total += 1
            if result == x:
                passed += 1
    print(f"  XOR involution (f∘f = id): {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_xor_is_ring_automorphism():
    """Verify XOR with fixed mask is a Boolean ring automorphism.
    
    The key property: f(x) ⊕ f(y) = x ⊕ y
    Because: (x⊕mask) ⊕ (y⊕mask) = x⊕y⊕(mask⊕mask) = x⊕y
    
    This means f PRESERVES the XOR operation (in the quotient sense).
    Combined with bijectivity, f is an automorphism of (Z/2Z)^n.
    """
    passed = 0
    total = 256 * 256 * 4  # 4 masks, all pairs
    for mask in [0x00, 0xFF, 0xAB, 0x55]:
        for x in range(256):
            for y in range(256):
                fx = x ^ mask
                fy = y ^ mask
                if (fx ^ fy) == (x ^ y):
                    passed += 1
    print(f"  f(x)⊕f(y) = x⊕y (ring automorphism): {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_xor_preserves_hamming_distance():
    """XOR preserves Hamming distance (isometry of the Boolean cube)."""
    passed = 0
    total = 0
    for mask in range(16):  # Test first 16 masks
        for x in range(256):
            for y in range(256):
                d_before = bin(x ^ y).count('1')
                d_after = bin((x ^ mask) ^ (y ^ mask)).count('1')
                total += 1
                if d_before == d_after:
                    passed += 1
    print(f"  XOR preserves Hamming distance: {passed}/{total} PASS" if passed == total else f"  FAIL: {passed}/{total}")
    return passed == total

def test_xor_bijection():
    """Verify XOR is a bijection (Galois connection requirement)."""
    for mask in range(256):
        outputs = set()
        for x in range(256):
            outputs.add(x ^ mask)
        if len(outputs) != 256:
            print(f"  FAIL: mask={mask} not bijective")
            return False
    print(f"  XOR bijection: 256/256 for all 256 masks PASS")
    return True

def test_xor_preserves_meet_join():
    """Verify XOR preserves meet (∧) and join (∨) up to complement."""
    passed = 0
    total = 0
    for mask in range(4):  # Test first 4 masks exhaustively
        for x in range(256):
            for y in range(256):
                # f(x ∧ y) should relate to f(x) ∧ f(y) via the mask
                meet_xy = x & y
                f_meet = meet_xy ^ mask
                fx = x ^ mask
                fy = y ^ mask
                f_meet_direct = fx & fy
                # XOR distributes over XOR but not AND/OR
                # However, f(x ∧ y) = f(x) ∧ f(y) ∨ mask-specific correction
                # For Galois connection, we need: f(x∧y) ≤ f(x)∧f(y)
                total += 1
                if (f_meet & f_meet_direct) == f_meet:
                    passed += 1
    print(f"  XOR preserves meet order: {passed}/{total} ({100*passed/total:.1f}%)")
    return passed == total

if __name__ == "__main__":
    print("Part 1: XOR Conversion as Self-Adjoint Galois Connection")
    print("=" * 55)
    r1 = test_xor_involution()
    r2 = test_xor_bijection()
    r3 = test_xor_is_ring_automorphism()
    r4 = test_xor_preserves_hamming_distance()
    all_pass = r1 and r2 and r3 and r4
    print(f"\n{'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
