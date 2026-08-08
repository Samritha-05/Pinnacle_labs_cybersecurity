import re
import math

COMMON_PASSWORDS = {
    "password", "123456", "12345678", "qwerty", "admin", 
    "welcome", "password123", "letmein", "iloveyou"
}

def print_banner(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50 + "\n")

def analyze_password(password: str):
    print_banner("*** PASSWORD ANALYZER ***")

    # 1. Check common breach list
    if password.lower() in COMMON_PASSWORDS:
        print("-" * 50)
        print("RESULT: CRITICAL RISK")
        print("REASON: Found in common leaked password list.")
        print("-" * 50 + "\n")
        return

    # 2. Analyze length and character sets
    length = len(password)
    has_lower = bool(re.search(r'[a-z]', password))
    has_upper = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'[0-9]', password))
    has_special = bool(re.search(r'[^a-zA-Z0-9]', password))

    pool_size = 0
    if has_lower: pool_size += 26
    if has_upper: pool_size += 26
    if has_digit: pool_size += 10
    if has_special: pool_size += 32

    # 3. Calculate Shannon Entropy (bits)
    entropy = length * math.log2(pool_size) if pool_size > 0 else 0

    # 4. Determine Strength Rating
    if entropy < 30 or length < 8:
        rating = "WEAK"
    elif entropy < 60 or length < 12:
        rating = "MODERATE"
    elif entropy < 80:
        rating = "STRONG"
    else:
        rating = "VERY STRONG"

    # 5. Output Metrics
    print("-" * 50)
    print(f"PASSWORD LENGTH:    {length} characters")
    print(f"CHARACTER POOL:     {pool_size} possible characters")
    print(f"CALCULATED ENTROPY: {entropy:.2f} bits")
    print(f"STRENGTH RATING:    {rating}")
    print("-" * 50)

    # 6. Detailed Feedback
    print("\n[ANALYZER FEEDBACK]")
    if length < 12:
        print("- Increase length to at least 12–16 characters.")
    if not has_upper:
        print("- Add uppercase letters (A-Z).")
    if not has_lower:
        print("- Add lowercase letters (a-z).")
    if not has_digit:
        print("- Add numeric digits (0-9).")
    if not has_special:
        print("- Add special symbols (e.g., !@#$%^&*).")
    if rating in ["STRONG", "VERY STRONG"]:
        print("- Password meets high complexity standards!")
    print("-" * 50 + "\n")

if __name__ == "__main__":
    pwd = input("ENTER PASSWORD TO ANALYZE: ")
    analyze_password(pwd)