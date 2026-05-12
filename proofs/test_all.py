#!/usr/bin/env python3
"""
Run all Galois Unification Principle proofs.
"""

import subprocess
import sys

PROOFS = [
    ("Part 1: XOR Conversion", "part1_xor.py"),
    ("Part 2: INT8 Soundness", "part2_int8.py"),
    ("Part 3: Bloom Filter (Heyting)", "part3_bloom.py"),
    ("Part 4: Precision Quantization", "part4_quantize.py"),
    ("Part 5: Intent Alignment", "part5_intent.py"),
    ("Part 6: Holonomy Consensus", "part6_holonomy.py"),
]

def run_proof(name, script):
    print(f"\n{'='*70}")
    print(f"Running: {name}")
    print('='*70)
    result = subprocess.run(
        [sys.executable, script],
        capture_output=True, text=True, timeout=60
    )
    print(result.stdout)
    if result.stderr:
        print(f"STDERR: {result.stderr}")
    
    passed = "ALL TESTS PASSED" in result.stdout
    return passed

def main():
    import os
    proof_dir = os.path.dirname(os.path.abspath(__file__))
    
    results = {}
    for name, script in PROOFS:
        path = os.path.join(proof_dir, script)
        try:
            passed = run_proof(name, path)
            results[name] = "PASS" if passed else "FAIL"
        except subprocess.TimeoutExpired:
            results[name] = "TIMEOUT"
        except Exception as e:
            results[name] = f"ERROR: {e}"
    
    print(f"\n{'='*70}")
    print("GALOIS UNIFICATION PRINCIPLE — SUMMARY")
    print('='*70)
    
    all_pass = True
    for name, status in results.items():
        symbol = "✓" if status == "PASS" else "✗"
        print(f"  {symbol} {name}: {status}")
        if status != "PASS":
            all_pass = False
    
    print('='*70)
    if all_pass:
        print("ALL 6 PARTS PROVEN — GALOIS UNIFICATION PRINCIPLE VERIFIED")
    else:
        print("SOME PROOFS FAILED — REVIEW NEEDED")
    print('='*70)

if __name__ == "__main__":
    main()
