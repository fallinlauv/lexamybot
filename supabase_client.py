import os
import httpx
from dotenv import load_dotenv

# Load .env (aktif saat development lokal, di hosting bisa otomatis lewat environment)
load_dotenv()

# Ambil data dari environment
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_TABLE = "user"  # GANTI ke "user" jika memang nama tabel kamu "user", bukan "users"

# Cek validitas environment
if not SUPABASE_URL or not SUPABASE_KEY:
    raise ValueError("❌ SUPABASE_URL dan SUPABASE_KEY wajib diatur di .env")

# Header wajib untuk akses Supabase REST API
HEADERS = {
    "apikey": SUPABASE_KEY,
    "Authorization": f"Bearer {SUPABASE_KEY}",
    "Content-Type": "application/json",
}

# ✅ Fungsi untuk menyimpan user baru
async def insert_user(user_id: int, username: str, joined_at: str):
    payload = {
        "user_id": user_id,
        "username": username,
        "joined_at": joined_at
    }

    async with httpx.AsyncClient() as client:
        res = await client.post(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}",
            json=payload,
            headers=HEADERS
        )
        try:
            return res.status_code, res.json()
        except Exception:
            return res.status_code, res.text

# ✅ Fungsi untuk mengambil data user berdasarkan ID Telegram
async def get_user(user_id: int):
    async with httpx.AsyncClient() as client:
        res = await client.get(
            f"{SUPABASE_URL}/rest/v1/{SUPABASE_TABLE}?user_id=eq.{user_id}",
            headers=HEADERS
        )
        try:
            return res.status_code, res.json()
        except Exception:
            return res.status_code, res.text
