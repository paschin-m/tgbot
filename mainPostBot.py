from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import ReplyKeyboardRemove
from telegram.ext import Updater
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
import json

#глобальные настройки поведения и компонент бота-оповещения команды в Telegram
buttonSet='Проверить заполнение RN'
# rpStuffAutoIfobot - имя бота для телеграм в строке поиска

def logErrorMonitor(f):
    def inner(*args, **kwargs):
        try:
            return f(*args,**kwargs)
        except Exception as e:
            print(f'Ошибки были следующие: {e}')
            raise e
    return inner

def buttonSetHandler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text='Производится проверка заполнения RN, результаты проверки опубликуются здесь!',
        reply_markup=ReplyKeyboardRemove(),
    )

def message_handler(update: Update, context: CallbackContext):
    text=update.message.text
    reply_markup=ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=buttonSet)
            ],
        ],
        resize_keyboard=True,
    )
    if text==buttonSet:
        return buttonSetHandler(update=update,context=context)
    update.message.reply_text(
        text='ReleaseNotes.txt (далее RN) забери с репозитория. Команды установки вносятся между тегами #start и #end.'
             'Программисту, который заполняет RN необходимо после тега #start перейти на новую строку для ввода комад установки ПАТЧА'
             'Каждая команда вводится на одной строке команда заканчивается символом - ; Многоточие следует удалить из файла'
             'Завершается ввод команд отдельной строкой с #end',
        reply_markup=reply_markup,
    )
@logErrorMonitor
def main():
    with open("conf.json","r") as read_file:
        config=json.load(read_file)
    print('Start')
    updater=Updater(
        token=config["tg_token"],
        use_context=True,
    )
    updater.dispatcher.add_handler(MessageHandler(filters=Filters.all, callback=message_handler))

    updater.start_polling()
    updater.idle()

main()