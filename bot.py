import os
import telebot
from notion.client import NotionClient
from notion.block import TextBlock
from to_notion import append_text_to_notion_page


#tokens 
TOKEN = os.environ['BOT_TOKEN']
token_notion = os.environ['NOTION_TOKEN']


#create bot
bot = telebot.TeleBot(TOKEN)


#global for page address
page_address = ''


@bot.message_handler(commands=['start', 'go', 'activate'])
def start_handler(message):
    bot.send_message(message.chat.id, 
        '''Hey there! 
        I\'m a deadpan simple bot for appending text to Notion page. 
        Set page address with /setpage. 
        Then just send me text you want to appear in said Notion page.''')



@bot.message_handler(commands=['setpage'])
def start_handler(message):
    bot.send_message(message.chat.id, 'please send me an address of a page from your Notion')
    # TODO: получить адрес из текста
    bot.register_next_step_handler(message, get_page_address)
    
    bot.send_message(message.chat.id, f'page set to {page_address}!')


def get_page_address(message):
    page_address = message.text


@bot.message_handler(content_types=['text'])
def text_handler(message):
    text = message.text
    append_text_to_notion_page(token_notion, page_address, text)
    bot.send_message(message.chat.id, f'sent text to {page_address}!')


bot.polling(none_stop=True, timeout=300)