from Invokes import invoke_http
########################################## Telebot Initalization Below ##########################################
from telebot import telebot, types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv("config/.env")

# Now you can access the TELEGRAM_TOKEN environment variable
TOKEN = os.getenv("TELEGRAM_TOKEN")

# TOKEN = "6718909166:AAGJ8SFglA4R4cKydXUX0hJkkPGM7vl3jdg"
bot = telebot.TeleBot(TOKEN)
########################################## Telebot Initalization Above ##########################################

########################################## Menu Settings Below ##########################################
def main_menu(username):
    outgoing_message =  f"Hello {username}! I am Jarvis, Educatum's assistant!\n\nWhat do you need help with today?"
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Rescheduling", callback_data="reschedule"))
    markup.add(types.InlineKeyboardButton("Talk To Tutor", callback_data="goto_talktotutor"))
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
    
    if navigation == "goto_talktotutor":
        outgoing_message,markup = talktotutor_menu()

    elif navigation == "goto_main":
        outgoing_message,markup = main_menu(username)
        
    bot.edit_message_text(outgoing_message, call.message.chat.id,call.message.message_id, reply_markup=markup)

########################################## Chat Basics Above ##########################################
    
########################################## Reschedule Below ##########################################
# Upcoming 1: Fetches 4 Upcoming Lessons & Prompts Upcoming Lessons
@bot.callback_query_handler(func=lambda call: call.data.startswith("reschedule"))
def prepare_upcoming_lessons(call):
    telegram_username = call.from_user.username
    outgoing_message = "Which upcoming lesson would you reschedule?"
    markup = types.InlineKeyboardMarkup()
    url = "http://127.0.0.1:5000/communication/prepare_upcoming_lessons"

    payload = {
        "telegram_username": telegram_username,
    }
    
    response = invoke_http(url, method = "POST", json = payload)
    if response.get("code", 200) == 200:
        upcoming_lessons = response.get("upcoming_lessons_formatted", [])

        for lesson in upcoming_lessons:
            eventID = lesson[1]
            day_time = lesson[0]
            markup.row(types.InlineKeyboardButton(day_time, callback_data=f'upcominglesson_{eventID}'))

        markup.row(types.InlineKeyboardButton("🔙 Back", callback_data="goto_reschedule"))

    else:
        print("Error: prepare_upcoming_lessons", response.get("message"))

    bot.edit_message_text(outgoing_message, call.message.chat.id, call.message.message_id, reply_markup=markup)

# Upcoming 2: Fetches Avail Dates From Upcoming Lesson Date & Prompts Available Dates
@bot.callback_query_handler(func=lambda call: call.data.startswith('upcominglesson_'))
def upcoming_lesson_selection(call):
    outgoing_message = "Select an available date!"
    markup = types.InlineKeyboardMarkup()
    url = "http://127.0.0.1:5000/communication/get_weekly_available_timeslots"
    selected_lesson_eventID = call.data.split('_')[1]

    payload = {'selected_lesson_eventID': selected_lesson_eventID}
    
    response = invoke_http(url, method="POST", json=payload)

    if response.get("code", 200) == 200:  # Check for HTTP success status
        available_slots_week = response.get("available_timeslots_week_formatted", [])
        
        # Number of columns for dates
        columns = 2
        row_buttons = []

        for index, date in enumerate(available_slots_week, start=1):
            # Include both the new date and the original eventID in callback_data
            callback_data = f'newdate_{selected_lesson_eventID}_{date}'
            row_buttons.append(types.InlineKeyboardButton(date, callback_data=callback_data))
            
            if index % columns == 0 or index == len(available_slots_week):
                markup.row(*row_buttons)
                row_buttons = []  # Reset row_buttons for the next row

        markup.row(types.InlineKeyboardButton("🔙 Back", callback_data="goto_reschedule"))
    else:
        print("Error: handle_upcominglesson_selection", response.get("message"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=outgoing_message, reply_markup=markup)


# Upcoming Helper 3: Acknowledges Change & Updates Backend     
@bot.callback_query_handler(func=lambda call: call.data.startswith('newdate_'))
def handle_newdate_selection(call):
    
    url = "http://127.0.0.1:5000/communication/update_reschedule"

    username = call.from_user.username
    eventID = call.data.split('_')[1]  # Extract the eventID
    new_lesson = call.data.split('_')[2]  # Extract the new lesson date
    outgoing_message = "Your lesson has been rescheduled to" + "\n" + new_lesson
    payload = {
        'eventID': eventID,
        'new_lesson': new_lesson,
        'username': username
    }

    response = invoke_http(url,method="POST",json=payload)

    if response.get("code",200) == 200:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=outgoing_message)
    else:
        print("Error: newdate_selection")

########################################## Reschedule Above ##########################################

bot.infinity_polling()