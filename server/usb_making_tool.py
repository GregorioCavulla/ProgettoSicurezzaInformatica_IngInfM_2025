import json
import os

KEY_GEN_PATH = "genera_chiavi.py"  # Path to key generation script
RNG_DB = "rng.json"  # Path to RNG token file
SERVER_KEY_PATH = "rsa_keys/server_public.pem"  # Path to server public key

"""prendo la chiave pubblica del server e la copio nella chiavetta usb"""

def copy_server_public_key_to_usb():
    if not os.path.exists("rsa_keys/server_public.pem"):
        raise FileNotFoundError("Server public key not found in rsa_keys.")
    
    with open("rsa_keys/server_public.pem", "rb") as f:
        server_public_key = f.read()
    
    usb_device_path = "../usb_device/server_public.pem"
    with open(usb_device_path, "wb") as f:
        f.write(server_public_key)
    
    print(f"Server public key copied to {usb_device_path}")
copy_server_public_key_to_usb()

"""prendo rng token da rng.json e lo copio nella chiavetta usb"""
def copy_rng_token_to_usb():
    if not os.path.exists("rng.json"):
        raise FileNotFoundError("RNG token file not found in rng.json.")
    
    with open("rng.json", "r") as f:
        rng_data = json.load(f)
    
    if not rng_data:
        raise ValueError("No RNG tokens found in rng.json.")
    
    # Prendi il primo token
    first_token = next(iter(rng_data.keys()))

    
    usb_device_path = "../usb_device/rng_token.txt"
    with open(usb_device_path, "w") as f:
        f.write(first_token)
    
    print(f"RNG token copied to {usb_device_path}")
copy_rng_token_to_usb()

"""Wipe the USB device"""
def wipe_usb_device():
    usb_device_path = "../usb_device"
    if os.path.exists(usb_device_path):
        for filename in os.listdir(usb_device_path):
            file_path = os.path.join(usb_device_path, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    os.rmdir(file_path)
            except Exception as e:
                print(f"Failed to delete {file_path}. Reason: {e}")
    else:
        print(f"USB device path {usb_device_path} does not exist.")
wipe_usb_device()

# Main function to execute the USB making tool
def main():
    print("Starting USB making tool...")
    wipe_usb_device()
    copy_server_public_key_to_usb()
    copy_rng_token_to_usb()
    print("USB device setup completed successfully.")
main()