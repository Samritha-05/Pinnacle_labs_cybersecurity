import os

def print_banner(title):
    print("\n" + "=" * 50)
    print(title.center(50))
    print("=" * 50 + "\n")

def process_image(input_path: str, output_path: str, key: int):
    if not os.path.exists(input_path):
        print(f"\n[ERROR]: FILE '{input_path}' NOT FOUND IN CURRENT FOLDER.")
        return

    with open(input_path, "rb") as f:
        data = bytearray(f.read())

    for i in range(len(data)):
        data[i] ^= key

    with open(output_path, "wb") as f:
        f.write(data)

    print("-" * 50)
    print(f"SUCCESS: OUTPUT SAVED TO '{output_path}'")
    print("-" * 50 + "\n")

if __name__ == "__main__":
    print_banner("*** IMAGE ENCRYPTION TOOL ***")
    mode = input("CHOOSE ACTION (encrypt/decrypt): ").strip().lower()
    in_file = input("INPUT FILENAME (e.g., photo.jpg): ").strip()
    out_file = input("OUTPUT FILENAME (e.g., secret.jpg): ").strip()
    key = int(input("ENTER NUMERIC SECRET KEY (1-255): "))

    if mode in ['encrypt', 'decrypt']:
        process_image(in_file, out_file, key)
    else:
        print("\n[ERROR]: INVALID ACTION CHOSEN.")