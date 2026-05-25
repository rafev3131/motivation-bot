import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN не найден. Проверь файл .env")

motivational_messages = [
    "Ты справишься. Просто сделай один маленький шаг прямо сейчас.",
    "Сегодня отличный день, чтобы стать чуть сильнее, чем вчера.",
    "Не нужно идеально. Нужно начать.",
    "Твой прогресс уже идет, даже если он кажется маленьким.",
    "Сфокусируйся на одном деле. Один час, один шаг, один результат.",
    "Ты не обязан знать весь путь. Достаточно сделать следующий шаг.",
    "Дисциплина сегодня - свобода завтра.",
    "Маленькие действия каждый день создают большие перемены.",
    "Ты уже молодец, потому что не стоишь на месте.",
    "Сделай паузу, вдохни и продолжай. У тебя получится."
]

subscribed_chats = set()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribed_chats.add(chat_id)

    await update.message.reply_text(
        "Привет! Я буду каждый час присылать тебе мотивирующее сообщение."
    )


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    subscribed_chats.discard(chat_id)

    await update.message.reply_text(
        "Хорошо, я больше не буду присылать уведомления."
    )


async def send_motivation(context: ContextTypes.DEFAULT_TYPE):
    if not subscribed_chats:
        return

    message = random.choice(motivational_messages)

    for chat_id in subscribed_chats:
        try:
            await context.bot.send_message(chat_id=chat_id, text=message)
        except Exception as error:
            print(f"Не удалось отправить сообщение в chat_id={chat_id}: {error}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stop", stop))

    app.job_queue.run_repeating(
        send_motivation,
        interval=3600,
        first=10
    )

    print("Бот запущен...")
    app.run_polling()


if __name__ == "__main__":
    main()