from telebot import telebot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

# Now you can access the TELEGRAM_TOKEN environment variable
TOKEN = os.getenv("TELEGRAM_TOKEN")

# TOKEN = "6718909166:AAGJ8SFglA4R4cKydXUX0hJkkPGM7vl3jdg"
bot = telebot.TeleBot(TOKEN)
COMMUNICATION_URL = "http://127.0.0.1:5000/process_message"

########################################## Menu Settings Below ##########################################
def main_menu(username):
    outgoing_message =  f"Hello {username}! I am Jarvis, Educatum's assistant!\n\nWhat do you need help with today?"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Rescheduling", callback_data="goto_reschedule"))
    markup.add(types.InlineKeyboardButton("Talk To Tutor", callback_data="goto_talktotutor"))
    return outgoing_message,markup

def reschedule_menu():
    outgoing_message = "Would you like to reschedule:"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Upcoming Lesson", callback_data="reschedule_upcoming"))
    markup.row(types.InlineKeyboardButton("All Future Lessons", callback_data="reschedule_all"))
    markup.row(types.InlineKeyboardButton("🔙 Back", callback_data="goto_main"))
    return outgoing_message,markup

def talktotutor_menu():
    outgoing_message = "What is your enquiring regarding?"
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton("Urgent Help", callback_data="item_1"))
    markup.row(types.InlineKeyboardButton("Hehe Haha", callback_data="item_2"))
    markup.row(types.InlineKeyboardButton("🔙 Back", callback_data="goto_main"))
    return outgoing_message,markup
########################################## Menu Settings Above ##########################################

########################################## Chat Basics Below ##########################################

@bot.message_handler(commands=['help', 'start']) # Start Chat
def start_chat(incoming_message):
    username = incoming_message.from_user.username
    outgoing_message, markup = main_menu(username) 
    bot.send_message(incoming_message.chat.id, outgoing_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("goto"))
def menu_navigation(call): # Handles Navigation
    user = call.from_user # We have username here just for main_menu(username)
    username = user.username
    navigation = call.data # Navigation always starts with "goto"

    if navigation == "goto_reschedule":
        outgoing_message,markup = reschedule_menu()
    
    elif navigation == "goto_talktotutor":
        outgoing_message,markup = talktotutor_menu()

    elif navigation == "goto_main":
        outgoing_message,markup = main_menu(username)
        
    bot.edit_message_text(outgoing_message, call.message.chat.id,call.message.message_id, reply_markup=markup)

########################################## Chat Basics Above ##########################################
    

########################################## Main Reschedule Function Above ##########################################
@bot.callback_query_handler(func=lambda call: call.data.startswith("reschedule"))
def reschedule_navigation(call):
    user = call.from_user
    username = user.username
    reschedule_type = call.data.split("_")[-1] # Either "upcoming" or "all"

    # Dispatch to Upcoming/All rescheduling functions
    if reschedule_type == "upcoming":
        outgoing_message, markup = prepare_upcoming_lessons(username)

    elif reschedule_type == "all":
        pass

    bot.edit_message_text(outgoing_message, call.message.chat.id,call.message.message_id, reply_markup=markup)
########################################## Main Reschedule Function Above ##########################################
    
########################################## Reschedule Upcoming Helpers Below ##########################################
# Upcoming Helper 1: Fetches Upcoming Lessons & Prompts Upcoming Lessons
def prepare_upcoming_lessons(username):
    outgoing_message = "Which upcoming lesson would you reschedule?"
    markup = types.InlineKeyboardMarkup()

    payload = {
        "request": "fetch_upcoming_lessons",
        "username": username,
    }

    response = requests.post(COMMUNICATION_URL, json = payload)
    
    if response.ok:
        upcoming_lessons = response.json()["data"]

        for lesson in upcoming_lessons:
            markup.row(types.InlineKeyboardButton(lesson, callback_data=f'upcominglesson_{lesson}'))

        markup.row(types.InlineKeyboardButton("None", callback_data="none"))
        markup.row(types.InlineKeyboardButton("🔙 Back", callback_data="goto_reschedule"))

    else:
        print("Error: prepare_upcoming_lessons")

    return outgoing_message, markup

# Upcoming Helper 2: Fetches Avail Dates From Upcoming Lesson Date & Prompts Available Dates
@bot.callback_query_handler(func=lambda call: call.data.startswith('upcominglesson_'))
def handle_upcominglesson_selection(call):
    outgoing_message = "Select an available date!"
    markup = types.InlineKeyboardMarkup()
    selected_lesson = call.data.split('_')[1]

    payload = {
        'request': "fetch_available_timeslot_week",
        'date': selected_lesson
    }

    response = requests.post(COMMUNICATION_URL, json = payload)
    
    if response.ok:
        available_date_week = response.json()['data']

        for date in available_date_week:
            markup.add(types.InlineKeyboardButton(date, callback_data=f'newdate_{date}'))

        markup.row(types.InlineKeyboardButton("None", callback_data="none"))
        markup.row(types.InlineKeyboardButton("🔙 Back", callback_data="goto_reschedule"))
        
    else:
        print("Error: handle_upcominglesson_selection")

    
    bot.edit_message_text(outgoing_message, call.message.chat.id,call.message.message_id, reply_markup=markup)

# Upcoming Helper 3: Acknowledges Change & Updates Backend     
@bot.callback_query_handler(func=lambda call: call.data.startswith('newdate_'))
def handle_newdate_selection(call):
    outgoing_message = "Your Lesson On\n" + "\n" + upcoming_lesson + "\n" + "Has been rescheduled to" + "\n" + new_lesson

    user = call.from_user
    username = user.username
    upcoming_lesson = "WE NEED TO FIX THIS"
    new_lesson = call.data.split('_')[-1]

    payload = {
        'request': "change_request_single",
        'username': username,
        'upcoming_lesson': upcoming_lesson,
        'new_lesson': new_lesson
    }

    response = requests.post(COMMUNICATION_URL, json = payload)
    if response.ok:
        bot.edit_message_text(outgoing_message, call.message.chat.id,call.message.message_id)
    else:
        print("Error: handle_newdate_selection")
    
########################################## Reschedule Upcoming Helpers Above ##########################################

########################################## Reschedule All Helpers Below ##########################################

########################################## Reschedule All Helpers Above ##########################################
bot.infinity_polling()