import datetime
import time
import sqlite3

async def add_activity(db_connection, update):
    db = db_connection.cursor()
    full_command = update['text'].split(' ')

    # Testing input length
    if(len(full_command) < 2):
        return "Usage: /act <i>activity_name</i> [<i>notes</i>]"

    # Getting new entry data
    user_id = update['from']['id']
    activity_name = str(full_command[1])
    notes = str(" ".join(full_command[2:]))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # Writing data to db
    try:
        db.execute(
            """
            INSERT INTO Activities (User, ActivityName, Timestamp, Notes)
            VALUES(?, ?, ?, ?);
            """, (user_id, activity_name, timestamp, notes)
        )
        db_connection.commit()
    except:
        return 'Insertion failed. :('
    return 'Insetion compelted.'

async def add_mood(db_connection, update):
    db = db_connection.cursor()
    full_command = update['text'].split(' ')

    # Testing input length
    if(len(full_command) < 2):
        return "Usage: /mood <i>mood_value</i> [<i>notes</i>]"

    # Getting new entry data
    user_id = update['from']['id']
    mood_value = str(full_command[1])
    notes = str(" ".join(full_command[2:]))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')

    # Writing data to db
    try:
        db.execute(
            """
            INSERT INTO Moods (User, MoodValue, Timestamp, Notes)
            VALUES(?, ?, ?, ?);
            """, (user_id, mood_value, timestamp, notes)
        )
        db_connection.commit()
    except:
        return 'Insertion failed. :('
    return 'Insetion compelted.'

async def get_db(update, bot):
    try:
        with open("data/maranc-bot.db", 'rb') as db:
            await bot.sendDocument(
                chat_id = update['from']['id'],
                document = db
            )
    except Exception as e:
        return dict(text=str("Error:\n\n<code>{}</code>".format(e))[:5000], parse_mode="HTML")
    return "Here it is!"
