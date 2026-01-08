# Silksong Text Decryptor/Encryptor

A simple Python tool for decrypting and re-encrypting text assets from **Hollow Knight: Silksong**.

The game's text files are stored as JSON with an encrypted `m_Script` field. This script allows you to convert them into readable plain text files and back again.

## Features

- Decrypt all `.json` files in a folder (and subfolders) to `.txt` files
- Re-encrypt `.txt` files back to the original `.json` format
- Preserves folder structure
- Shows progress in the console
- Clean and safe file handling

## Requirements

- Python 3.7 or higher
- `pycryptodome` library

Install the required dependency:

```bash
git clone https://github.com/ReaIMoFraD/silksong-localization-tool.git
cd silksong-localization-tool
```

## Usage

```bash
# Decrypt: convert .json files to readable .txt
python silksong_decryptor.py -decrypt "path/to/Texts/folder"

# Encrypt: convert .txt files back to .json
python silksong_decryptor.py -encrypt "path/to/Texts_Decrypted/folder"
```

### Example

```bash
python silksong_decryptor.py -decrypt "E:\Games\Hollow Knight Silksong\Hollow Knight Silksong_Data\Texts"
```

Output will be created in a new folder named `Texts_Decrypted` next to the input folder.

### File Format

Each output `.txt` file contains:
- Line 1: The text name (`m_Name`)
- Remaining lines: The decrypted script content

The encrypt mode expects the same format when reading `.txt` files.

## Notes

- Only modify the content of decrypted `.txt` files if you understand the implications.
- This tool is intended for personal use and study of game files only.
- Always make backups before modifying game data.

## License
This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

Made with ❤️ for the localization community.
