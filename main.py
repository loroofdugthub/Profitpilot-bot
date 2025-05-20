import os
import openai
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
ALPHA_VANTAGE_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
openai.api_key = OPENAI_API_KEY

def get_price(symbol):
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={ALPHA_VANTAGE_API_KEY}'
    r = requests.get(url)
    data = r.json()
    try:
        price = data['Global Quote']['05. price']
        return f"{symbol.upper()} price is ${price}"
    except:
        return "Price not found. Check symbol."

async def insight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = " ".join(context.args) or "crypto and stock profit strategies"
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Give expert tips to increase profit in {user_msg}."}]
    )
    answer = response['choices'][0]['message']['content']
    await update.message.reply_text(answer)

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        symbol = context.args[0].upper()
        result = get_price(symbol)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Use /price SYMBOL (e.g., /price BTC)")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to ProfitPilot! Use /price or /insight to begin.")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("price", price))
app.add_handler(CommandHandler("insight", insight))
app.run_polling()
