import random, string, re

class PasswordChecker:
    def __init__(self):
        pass

    def display_menu(self):
        print("\n=== Password Checker Program ===")
        print("1. Check password strength.")
        print("2. Generate a random strong password.")
        print("3. Exit.")
        return input("Select an option (1-3): ").strip()

    def check_password_strength(self, password):
        if not password:
            print("No password entered. ")
            return
        issues = []
        score = 0

        # Length >= 8
        if len(password) >= 8:
            score += 1
        else:
            issues.append("Password must be at least 8 characters long.")

        # Atleast one uppercase
        if re.search(r"[A-Z]", password):
            score += 1
        else:
            issues.append("Missing atleast one uppercase letter (A-Z).")

        # Atleast one lowercase
        if re.search(r"[a-z]", password):
            score += 1
        else:
            issues.append("Missing atleast one lowercase letter (a-z).")

        # Atleast one digit
        if re.search(r"\d", password):
            score += 1
        else:
            issues.append("Missing at least one digit (0-9).")

        # Atleast one special character
        if re.search(r"[!@#$%^&*()_+\-=\[\]{};':\"\\|,.<>\/?~]", password):
            score += 1
        else:
            issues.append("Missing at least one special character (!@#$%^&* etc.).")

        # No simple sequences (abc, 123, etc.)
        bad_sequences = [
            "abc", "bcd", "cde", "def", "efg", "fgh", "ghi", "hij", "ijk", "jkl",
            "klm", "lmn", "mno", "nop", "opq", "pqr", "qrs", "rst", "stu", "tuv",
            "uvw", "vwx", "wxy", "xyz",
            "123", "234", "345", "456", "567", "678", "789", "890"
        ]

        lowered = password.lower()
        for seq in bad_sequences:
            if seq in lowered:
                issues.append(f"Avoid sequential characters like '{seq}'.")
                break

        # No repeating characters like aaa or 111
        if re.search(r"(.)\1{2,}", password):
            issues.append("Avoid repeating the same character multiple times (e.g., 'aaa' or '111').")

        # Temporary strength
        if score == 5 and len(issues) == 0:
            strength = "Strong"
        elif score >= 3:
            strength = "Moderate"
        else:
            strength = "Weak"

        print(f"\nPassword strength: {strength}")
        if issues:
            print("Suggestions to improve: ")
            for issue in issues:
                print(" - " + issue)

    def generate_random_password(self, length=12):
        if length < 8:
            print("Minimum length is 8. Setting to 8.")
            length = 8

        # Include one of each type
        lower = random.choice(string.ascii_lowercase)
        upper = random.choice(string.ascii_uppercase)
        digit = random.choice(string.digits)
        special = random.choice("!@#$%^&*()_+-=[]{}|;':,.<>?")

        # Fill the rest with random mix
        all_chars = string.ascii_letters + string.digits + "!@#$%^&*()-=_+[]{};':,.<>?"
        remaining = length - 4
        rest = ''.join(random.choice(all_chars) for _ in range(remaining))

        # Combine and shuffle to randomize positions
        password = lower + upper + digit + special + rest
        password_list = list(password)
        random.shuffle(password_list)
        new_password = ''.join(password_list)

        # Basic check to avoid obvious repeats/sequences
        while re.search(r"(.)\1{2,}", new_password) or any(seq in new_password.lower() for seq in ["abc", "123"]):
            random.shuffle(password_list)
            new_password = ''.join(password_list)

        print(f"\nGenerated strong password ({length} characters): {new_password}")
        return new_password

    def run(self):
        print("Welcome to the Password Checker!")
        while True:
            choice = self.display_menu()
            if choice == "1":
                pwd = input("\nEnter the password to check: ").strip()
                self.check_password_strength(pwd)
            elif choice == "2":
                try:
                    len_input = input(f"Enter desired length (minimum 8, default 12): ").strip()
                    pwd_length = int(len_input) if len_input else 12
                except ValueError:
                    pwd_length = 12
                self.generate_random_password(pwd_length)
            elif choice == "3":
                print("Thank you for using the Password Checker. Goodbye!")
                break
            else:
                print("Invalid option. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    password_checker = PasswordChecker()
    password_checker.run()
