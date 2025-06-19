import os
from dotenv import load_dotenv

# Muat file .env (berfungsi di lokal atau development)
load_dotenv()

# Ambil BOT_TOKEN dari .env
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Validasi agar bot tidak jalan tanpa token
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN belum diatur di file .env")
