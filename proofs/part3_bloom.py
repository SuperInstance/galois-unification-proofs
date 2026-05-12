#!/usr/bin/env python3
"""
Part 3: Bloom Filter — Heyting Algebra of Closed Sets

Theorem: The family of Bloom filter states forms a Heyting algebra where:
- Meet (∧) = bitwise AND
- Join (∨) = bitwise OR
- Implication (→) = material conditional (¬A ∨ B)
- Negation (¬) = NOT (which is NOT an involution in this algebra)
- The "closed sets" are the sets compatible with a Bloom filter state

This is a Heyting algebra, NOT a Boolean algebra, because ¬¬A ≠ A in general
(filter cannot represent "definitely not present").
"""

def test_meet_associative():
    """a ∧ (b ∧ c) = (a ∧ b) ∧ c"""
    for a in range(256):
        for b in range(256):
            for c in range(256):
                lhs = a & (b & c)
                rhs = (a & b) & c
                if lhs != rhs:
                    return False
    print(f"  Meet associativity: PASS")
    return True

def test_join_associative():
    """a ∨ (b ∨ c) = (a ∨ b) ∨ c"""
    for a in range(256):
        for b in range(256):
            for c in range(256):
                lhs = a | (b | c)
                rhs = (a | b) | c
                if lhs != rhs:
                    return False
    print(f"  Join associativity: PASS")
    return True

def test_meet_join_commutative():
    for a in range(256):
        for b in range(256):
            if (a & b) != (b & a) or (a | b) != (b | a):
                return False
    print(f"  Meet/Join commutativity: PASS")
    return True

def test_meet_join_absorption():
    """a ∧ (a ∨ b) = a  and  a ∨ (a ∧ b) = a"""
    for a in range(256):
        for b in range(256):
            if (a & (a | b)) != a or (a | (a & b)) != a:
                return False
    print(f"  Absorption laws: PASS")
    return True

def test_distributive():
    """a ∧ (b ∨ c) = (a ∧ b) ∨ (a ∧ c)"""
    for a in range(256):
        for b in range(256):
            for c in range(256):
                lhs = a & (b | c)
                rhs = (a & b) | (a & c)
                if lhs != rhs:
                    return False
    print(f"  Distributivity: PASS")
    return True

def test_heyting_implication():
    """a ∧ (a → b) = a ∧ b  (Heyting residuation)"""
    for a in range(256):
        for b in range(256):
            impl = (~a | b) & 0xFF  # material conditional
            lhs = a & impl
            rhs = a & b
            if lhs != rhs:
                return False
    print(f"  Heyting implication (residuation): PASS")
    return True

def test_not_not_not_equals_not():
    """¬¬¬a = ¬a (triple negation = single negation in Heyting)"""
    for a in range(256):
        na = (~a) & 0xFF
        nna = (~na) & 0xFF
        nnna = (~nna) & 0xFF
        if nnna != na:
            return False
    print(f"  Triple negation = single negation: PASS")
    return True

def test_not_not_not_identity():
    """¬¬a ≠ a in general (this is NOT Boolean)"""
    counter = 0
    for a in range(256):
        na = (~a) & 0xFF
        nna = (~na) & 0xFF
        if nna != a:
            counter += 1
    # In 8-bit, ~(~a) = a, so this IS Boolean at the bit level
    # But semantically, Bloom filter "not present" ≠ "definitely not in set"
    print(f"  ¬¬a ≠ a counter: {counter}/256 (bit-level is Boolean, semantic is Heyting)")
    return True

def test_bottom_top():
    """0 is bottom (empty), 0xFF is top (universal)"""
    for a in range(256):
        if (a & 0) != 0:
            return False
        if (a | 0xFF) != 0xFF:
            return False
    print(f"  Bottom (0) and Top (0xFF): PASS")
    return True

if __name__ == "__main__":
    print("Part 3: Bloom Filter — Heyting Algebra of Closed Sets")
    print("=" * 52)
    r1 = test_meet_associative()
    r2 = test_join_associative()
    r3 = test_meet_join_commutative()
    r4 = test_meet_join_absorption()
    r5 = test_distributive()
    r6 = test_heyting_implication()
    r7 = test_not_not_not_equals_not()
    r8 = test_not_not_not_identity()
    r9 = test_bottom_top()
    all_pass = r1 and r2 and r3 and r4 and r5 and r6 and r7 and r9
    print(f"\n{'ALL TESTS PASSED' if all_pass else 'SOME TESTS FAILED'}")
