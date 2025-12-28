import telebot
import requests
import time

# Ayarlar
BOT_TOKEN = "8443683055:AAGoUkD6pGkY-RLLceZPaArqeHUxYjUV_do"
bot = telebot.TeleBot(BOT_TOKEN)

# Ücretsiz bir indirme API'si (Örnek: Cobalt API - Instagram için çok hızlıdır)
def get_download_link(url):
    api_url = "https://api.cobalt.tools/api/json"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    data = {
        "url": url,
        "videoQuality": "720"
    }
    try:
        response = requests.post(api_url, headers=headers, json=data)
        return response.json().get('url')
    except:
        return None

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    if "instagram.com" in url:
        bot.reply_to(message, "⏳ Video hazırlanıyor, lütfen bekleyin...")
        
        video_url = get_download_link(url)
        
        if video_url:
            try:
                # Videoyu Telegram'a dosya olarak gönder
                bot.send_video(message.chat.id, video_url, caption="✅ Video indirildi!")
            except Exception as e:
                bot.reply_to(message, "❌ Video gönderilirken bir hata oluştu.")
        else:
            bot.reply_to(message, "❌ Video linki alınamadı. Linkin doğru olduğundan emin olun.")
    else:
        bot.reply_to(message, "👋 Lütfen geçerli bir Instagram Reels linki gönderin.")

print("Bot aktif...")
bot.infinity_polling()
