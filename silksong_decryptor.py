import argparse
import base64
import json
import os
import sys
from pathlib import Path

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


KEY = b"UKu52ePUBwetZ9wNX88o54dnfKRu0T1l" # 32-byte key for AES-256


def encrypt(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_ECB)
    return cipher.encrypt(pad(data, AES.block_size))


def decrypt(data: bytes) -> bytes:
    cipher = AES.new(KEY, AES.MODE_ECB)
    return unpad(cipher.decrypt(data), AES.block_size)


def encrypt_string(text: str) -> str:
    encrypted_bytes = encrypt(text.encode("utf-8"))
    return base64.b64encode(encrypted_bytes).decode("utf-8")


def decrypt_string(b64: str) -> str:
    encrypted_bytes = base64.b64decode(b64)
    decrypted_bytes = decrypt(encrypted_bytes)
    return decrypted_bytes.decode("utf-8")


def decrypt_folder(input_folder: str):
    input_path = Path(input_folder)
    if not input_path.is_dir():
        print(f"Error: Folder '{input_folder}' does not exist.")
        sys.exit(1)

    output_path = input_path.parent / (input_path.name + "_Decrypted")
    output_path.mkdir(exist_ok=True)

    for json_file in input_path.rglob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            name = data["m_Name"]
            encrypted_script = data["m_Script"]

            decrypted_text = decrypt_string(encrypted_script)

            output_content = name + "\n" + decrypted_text

            rel_path = json_file.relative_to(input_path)
            output_file = output_path / rel_path.with_suffix(".txt")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)

            print(f"Decrypted {name}")

        except Exception as e:
            print(f"Failed to process {json_file}: {e}")


def encrypt_folder(input_folder: str):
    input_path = Path(input_folder)
    if not input_path.is_dir():
        print(f"Error: Folder '{input_folder}' does not exist.")
        sys.exit(1)

    output_path = input_path.parent / (input_path.name + "_Encrypted")
    output_path.mkdir(exist_ok=True)

    for txt_file in input_path.rglob("*.txt"):
        try:
            lines = txt_file.read_text(encoding="utf-8").splitlines()
            if len(lines) < 1:
                continue

            name = lines[0]
            script = "\n".join(lines[1:])

            encrypted_script = encrypt_string(script)

            asset = {
                "m_Name": name,
                "m_Script": encrypted_script
            }

            rel_path = txt_file.relative_to(input_path)
            output_file = output_path / rel_path.with_suffix(".json")
            output_file.parent.mkdir(parents=True, exist_ok=True)

            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(asset, f, indent=4, ensure_ascii=False)

            print(f"Encrypted {name}")

        except Exception as e:
            print(f"Failed to process {txt_file}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Silksong text encryptor/decryptor (Python version)"
    )
    parser.add_argument(
        "mode",
        choices=["-decrypt", "-encrypt"],
        help="Operation mode"
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing .json (for decrypt) or .txt (for encrypt) files"
    )

    args = parser.parse_args()

    if args.mode == "-decrypt":
        decrypt_folder(args.folder)
    else:  # -encrypt
        encrypt_folder(args.folder)


if __name__ == "__main__":
    main()
