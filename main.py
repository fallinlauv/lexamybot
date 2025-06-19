from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram import Update
from config import BOT_TOKEN
from supabase_client import insert_user, get_user  # Tambahkan get_user
from datetime import datetime

# ✅ Fungsi saat user mengetik /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    joined_at = datetime.utcnow().isoformat()

    # Simpan data user ke Supabase
    status_code, response = await insert_user(
        user_id=user.id,
        username=user.username or "anonymous",
        joined_at=joined_at
    )

    if status_code in [200, 201]:
        await update.message.reply_text("✅ Kamu sudah terdaftar di sistem bot.")
    else:
        await update.message.reply_text("⚠️ Gagal menyimpan ke database.")
        print("Insert error:", response)

# ✅ Fungsi untuk command /check
async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    status_code, data = await get_user(user.id)

    if status_code == 200 and data:
        user_data = data[0]
        await update.message.reply_text(
            f"👤 Data kamu:\n"
            f"ID: {user_data['user_id']}\n"
            f"Username: {user_data['username']}\n"
            f"Joined at: {user_data['joined_at']}"
        )
    else:
        await update.message.reply_text("❌ Data kamu belum terdaftar.")

# ✅ Fungsi untuk command /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📋 Perintah yang tersedia:\n/start - Daftar ke bot\n/check - Lihat datamu\n/help - Bantuan")

# ✅ Fungsi utama menjalankan bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Daftarkan semua command handler
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("check", check))
    app.add_handler(CommandHandler("help", help_command))

    # Jalankan bot
    app.run_polling()

if __name__ == "__main__":
    main()
