import hmac
import hashlib
import base64
import json
import math
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os

# Secrets should be loaded from env vars
SECRET_KEY = os.getenv("SECRET_KEY", "my_super_secret_key_32_bytes_len")
AES_KEY = os.getenv("AES_KEY", "my_aes_secret_key_32_bytes_lengt")
AES_IV = os.getenv("AES_IV", "my_aes_16bytes_i")

def verify_signature(payload: str, signature: str) -> bool:
    """Verify HMAC-SHA256 signature"""
    expected_mac = hmac.new(
        SECRET_KEY.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    return hmac.compare_digest(expected_mac, signature)

def decrypt_payload(encrypted_payload_b64: str) -> dict:
    """Decrypt AES-256-CBC payload"""
    try:
        encrypted_data = base64.b64decode(encrypted_payload_b64)
        cipher = AES.new(AES_KEY.encode('utf-8'), AES.MODE_CBC, AES_IV.encode('utf-8'))
        decrypted_data = unpad(cipher.decrypt(encrypted_data), AES.block_size)
        return json.loads(decrypted_data.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance in meters between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371000 # Radius of earth in meters
    return c * r
