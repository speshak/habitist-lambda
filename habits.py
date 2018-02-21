import os
import re
import logging
import json
from datetime import datetime, timedelta
from todoist.api import TodoistAPI

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


def get_token():
    token = os.getenv('TODOIST_APIKEY')
    return token


def is_habit(text):
    return re.search(r'\[day\s(\d+)\]', text)


def is_today(text):
    today = (datetime.utcnow() + timedelta(1)).strftime("%a %d %b")
    return text[:10] == today


def is_due(text):
    yesterday = datetime.utcnow().strftime("%a %d %b")
    return text[:10] == yesterday


def update_streak(item, streak):
    days = '[day {}]'.format(streak)
    text = re.sub(r'\[day\s(\d+)\]', days, item['content'])
    item.update(content=text)


def main(event, context):
    body = { "tasksUpdated": 0 }

    API_TOKEN = get_token()
    if not API_TOKEN:
        logging.warn('Please set the API token in environment variable.')
        exit()

    today = datetime.utcnow().replace(tzinfo=None)
    api = TodoistAPI(token=API_TOKEN, cache="/tmp/todoist")
    api.sync()
    tasks = api.state['items']
    for task in tasks:
        if task['due_date_utc'] and is_habit(task['content']):
            if is_today(task['due_date_utc']):
                habit = is_habit(task['content'])
                streak = int(habit.group(1)) + 1
                update_streak(task, streak)
                body["tasksUpdated"] += 1
            elif is_due(task['due_date_utc']):
                update_streak(task, 0)
                task.update(date_string='ev day starting tod')
    api.commit()


    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

