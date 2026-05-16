# Importing necessary tools for the program
import base64    # For making the scrambled text look clean
import json      # For saving data into structured files
import os        # For checking if files exist on the computer
import hashlib   # For creating secure math-based keys from passwords
from datetime import datetime  # For recording the exact time of encryption


#  LAYER 1: Simple shift cipher logic
def caesar_encrypt(text: str, shift: int) -> str:
    result = []
    for ch in text:
        code = ord(ch)
        # Only change characters that we can actually see and print
        if 32 <= code <= 126:
            result.append(chr((code - 32 + shift) % 95 + 32))
        else:
            result.append(ch)
    return "".join(result)

# Reversing the shift to get the original text back
def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)

#  LAYER 2: Substitution Cipher (Swapping letters)

ORIGINAL  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
SUBSTITUTED = "QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm9876543210"

ENCRYPT_TABLE = str.maketrans(ORIGINAL, SUBSTITUTED)
DECRYPT_TABLE = str.maketrans(SUBSTITUTED, ORIGINAL)

# Swapping letters using the custom table above
def substitution_encrypt(text: str) -> str:
    return text.translate(ENCRYPT_TABLE)

# Swapping them back to their normal positions
def substitution_decrypt(text: str) -> str:
    return text.translate(DECRYPT_TABLE)


#  LAYER 3: Mixing and Flipping text

# Turn the password into a number we can use for math
def get_key_hash(password: str) -> int:
    return int(hashlib.sha256(password.encode()).hexdigest(), 16) % 256

# Mix up the text using the password and then flip it backwards
def xor_encrypt(text: str, password: str) -> str:
    key = get_key_hash(password)
    result = []
    for ch in text:
        xored = ord(ch) ^ key
        result.append(f"{xored:03d}")
    joined = "".join(result)
    return joined[::-1]

# Un-flip the text and reverse the mixing math
def xor_decrypt(text: str, password: str) -> str:
    key = get_key_hash(password)
    unrev = text[::-1]
    result = []
    for i in range(0, len(unrev), 3):
        chunk = unrev[i:i+3]
        if len(chunk) == 3:
            xored = int(chunk)
            original = xored ^ key
            result.append(chr(original))
    return "".join(result)

#  LAYER 4: Final formatting
# Make the scrambled text look like a clean string
def b64_encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()

# Turn the clean string back into our scrambled format
def b64_decode(text: str) -> str:
    return base64.b64decode(text.encode()).decode()


#  MASTER ENCRYPT / DECRYPT (Combining everything)

# Run all 4 layers of security one after another
def encrypt(plaintext: str, password: str) -> str:
    shift = get_key_hash(password) % 47 + 1
    step1 = caesar_encrypt(plaintext, shift)
    step2 = substitution_encrypt(step1)
    step3 = xor_encrypt(step2, password)
    step4 = b64_encode(step3)
    return step4

# Undo all 4 layers in the exact opposite order
def decrypt(ciphertext: str, password: str) -> str:
    shift = get_key_hash(password) % 47 + 1
    step1 = b64_decode(ciphertext)
    step2 = xor_decrypt(step1, password)
    step3 = substitution_decrypt(step2)
    step4 = caesar_decrypt(step3, shift)
    return step4

#  FILE HANDLING (Saving and Loading)

# Save the secret data into a JSON file so we can use it later
def save_to_file(encrypted_text: str, filename: str, original_hint: str = ""):
    data = {
        "tool": "The Maryam Protocol v1.0",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "hint": original_hint,
        "encrypted_data": encrypted_text
    }
    filepath = filename if filename.endswith(".json") else filename + ".json"
    with open(filepath, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\n  ✅ Data saved to '{filepath}'")
    return filepath

# Open and read the encrypted file we saved
def load_from_file(filename: str) -> dict:
    filepath = filename if filename.endswith(".json") else filename + ".json"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found!")
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


#  USER INTERFACE (Menu and Prompts)

# Show the main title on the screen
def print_banner():
    print("\n  🔐  Custom Encryption & Decryption Tool\n HK — Task 3")

# Show the options user can choose from
def print_menu():
    print("\n  1. Encrypt Data\n  2. Decrypt Data\n  3. Save Encrypted Data to File\n  4. Load & Decrypt from File\n  5. Exit")

# Ask the user for their secret password
def get_password(confirm: bool = False) -> str:
    password = input("\n  🔑 Enter password/key: ").strip()
    if not password:
        raise ValueError("Password cannot be empty!")
    if confirm:
        confirm_pass = input("  🔑 Confirm password: ").strip()
        if password != confirm_pass:
            raise ValueError("Passwords do not match!")
    return password

# Handle the encryption menu logic
def menu_encrypt():
    print("\n  ── ENCRYPT DATA ──")
    plaintext = input("  📝 Enter text to encrypt: ").strip()
    if not plaintext:
        print("  ⚠️  No text entered.")
        return None, None

    password = get_password(confirm=True)
    encrypted = encrypt(plaintext, password)

    print(f"\n✅ Encrypted Successfully!\n🔒 Encrypted Text: {encrypted}\n")
    return encrypted, plaintext

# Handle the decryption menu logic
def menu_decrypt():
    print("\n  ── DECRYPT DATA ──")
    ciphertext = input("🔒Enter encrypted text: ").strip()
    if not ciphertext:
        print("⚠️No text entered.")
        return

    password = get_password()
    try:
        decrypted = decrypt(ciphertext, password)
        print(f"\n  ✅ Decrypted Successfully!\n  📝 Original Text: {decrypted}\n")
    except Exception:
        print("\n❌ Decryption failed! Check your password.")

# Encrypt the text and then save it directly to a file
def menu_save():
    print("\n  ── SAVE ENCRYPTED DATA ──")
    plaintext = input("  📝 Enter text to encrypt & save: ").strip()
    if not plaintext:
        return

    password = get_password(confirm=True)
    hint = input("💡 Enter a hint: ").strip()
    filename = input("💾 Enter filename: ").strip() or "encrypted_data"

    encrypted = encrypt(plaintext, password)
    save_to_file(encrypted, filename, hint)

# Load an existing file and try to unlock it
def menu_load():
    print("\n  ── LOAD & DECRYPT FROM FILE ──")
    filename = input("📂 Enter filename: ").strip()
    if not filename:
        return

    try:
        data = load_from_file(filename)
        if data.get("hint"):
            print(f"Hint: {data['hint']}")

        password = get_password()
        decrypted = decrypt(data["encrypted_data"], password)
        print(f"\n  ✅ Decrypted Successfully!\n  📝 Original Text: {decrypted}\n")

    except Exception as e:
        print(f"\n  ❌ Could not load or decrypt file: {e}")

#  MAIN PROGRAM LOOP
def main():
    print_banner()

    while True:
        print_menu()
        choice = input("\n👉 Choose option (1-5): ").strip()

        if choice == "1":
            try: menu_encrypt()
            except ValueError as e: print(f"❌ {e}")

        elif choice == "2":
            try: menu_decrypt()
            except ValueError as e: print(f"❌ {e}")

        elif choice == "3":
            try: menu_save()
            except Exception as e: print(f"❌ {e}")

        elif choice == "4":
            try: menu_load()
            except Exception as e: print(f"sa❌ {e}")

        elif choice == "5":
            print("\n  👋 Goodbye!Stay Secure.\n")
            break

        else:
            print("\n  ⚠️  Please enter a valid choice (1–5).")

        # Wait for user to press enter before showing the menu again
        input("\n  Press Enter to continue...")

# This line tells Python to start the program here
if __name__ == "__main__":
    main()