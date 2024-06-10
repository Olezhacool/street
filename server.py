import logging
from telegram.ext import Application, MessageHandler, filters, CommandHandler
from telegram.ext import ConversationHandler
from telegram import ReplyKeyboardMarkup

TOKEN = "7458642626:AAEvyHHYWqTO-yfPpnjmjFk-iniGP-gqrwM"
TIMER = 5

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s'

)

logger = logging.getLogger(__name__)

reply_keyboard = [['/start'], ['/help']]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=False)


def remove_job(name, context):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


async def set_timer(update, context):
    chat_id = update.effective_message.chat_id
    job_removed = remove_job(str(chat_id), context)
    context.job_queue.run_once(echo2, TIMER, chat_id, name=str(chat_id), data=TIMER)
    text = 'Ща метнусь'
    if job_removed:
        text += 'ss'
        await update.effective_message.reply_text(text)


async def echo2(update, context):
    await context.bot.send_message(context.job.chat_id, text='5 cek')


async def echo(update, context):
    await update.message.reply_text(update.message.text)
    return 2


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Привет, {user.mention_html()}! Я повторюн, могу повторять за тобой, да я Илья Сизов!",
        reply_markup=markup)


async def help(update, context):
    user = update.effective_user
    await update.message.reply_html(rf"Привет, {user.mention_html()}! Я повторюн! Больше помогать не буду!")

async def stop(update, context):
    await update.message.reply_text('Bye, snitch!')
    return ConversationHandler.END



def main():
    application = Application.builder().token(TOKEN).build()
    text_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start), CommandHandler('help', help)],
        states={
            1: [MessageHandler(filters.TEXT & ~filters.COMMAND, echo)],
            2: [MessageHandler(filters.TEXT & ~filters.COMMAND, stop)]

        },
        fallbacks=[CommandHandler("stop", stop)]
    )
    application.add_handler(conv_handler)
    application.add_handler(text_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
