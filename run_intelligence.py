import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.intelligence.scanner import MorningScanner
from backend.intelligence.validator import EveningValidator

def run_intelligence():
    print("--- Running Morning Scanner ---")
    scanner = MorningScanner()
    report = scanner.scan_market()
    print("\nMorning Report Generated:")
    print(report[:500] + "...\n")

    print("--- Running Evening Validator ---")
    validator = EveningValidator()
    validation = validator.validate_predictions()
    print("\nValidation Report Generated:")
    print(validation[:500] + "...\n")

if __name__ == "__main__":
    run_intelligence()
