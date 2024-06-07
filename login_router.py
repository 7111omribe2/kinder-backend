import datetime as dt
import json
import deepl

import requests
from fastapi import APIRouter
from pydantic import BaseModel
from shapely.geometry import Point

users = [
    {
        'username': 'omri',
        'connection_type': 'brother',
        'decease': 'cancer',
        'age': 23,
        'location': Point(31.93923698780856, 34.7952495596364),
        'for_how_long': dt.timedelta(days=90)
    },
    {
        'username': 'nitay',
        'connection_type': 'brother',
        'decease': 'cancer',
        'age': 22,
        'location': Point(31.896207264989634, 34.79677389252961),
        'for_how_long': dt.timedelta(days=30)
    },
    {
        'username': 'daniel',
        'connection_type': 'mother',
        'decease': 'cancer',
        'age': 23,
        'location': Point(31.87838047674572, 34.736044728911246),
        'for_how_long': dt.timedelta(days=765)
    },
    {
        'username': 'shira',
        'connection_type': 'sister',
        'decease': 'cancer',
        'age': 26,
        'location': Point(32.086200713100055, 34.781161271332124),
        'for_how_long': dt.timedelta(days=12)
    },
    {
        'username': 'yonatan',
        'connection_type': 'mother',
        'decease': 'cancer',
        'age': 23,
        'location': Point(32.07714016816094, 34.77096406145831),
        'for_how_long': dt.timedelta(days=765)
    },
]

communities = [
    {
        'decease': 'cancer'
    }
]

auth_api_router = APIRouter()


@auth_api_router.get("/getUsers")
async def regular_login_for_access_token():
    return users


def sort_users(user):
    return user['age_diff'], user['location_dist']


def get_user(opt):
    user = opt['user_data']
    user['location'] = user['location'].wkt
    return user


@auth_api_router.get("/findMatch/{user_name}")
async def regular_login_for_access_token(user_name: str):
    user = [u for u in users if u['username'] == user_name][0]
    optional_users = []
    for other_user in users:
        if user['username'] == other_user['username']:
            continue
        if user['decease'] != other_user['decease']:
            continue
        if user['connection_type'] != other_user['connection_type']:
            continue
        age_diff = int(abs(user['age'] - other_user['age']) / 2) * 2
        location_dist = user['location'].distance(other_user['location'])
        for_how_long_diff = abs(user['for_how_long'] - other_user['for_how_long'])
        optional_users.append({
            'user_data': other_user,
            'age_diff': age_diff,
            'location_dist': location_dist,
            'for_how_long_diff': for_how_long_diff
        })
    optional_users.sort(key=sort_users)
    optional_users = [get_user(opt) for opt in optional_users]
    return optional_users[:5]


class RightsBot(BaseModel):
    text: str


# Print the translated text


@auth_api_router.get("/rightsBot")
async def get_answer(modal: RightsBot):
    text = modal.text
    chat_answer = await get_chat_answer(text)
    hebrew_text = await translate_text(chat_answer)
    return {'chat_answer': hebrew_text}


async def translate_text(chat_answer):
    return """
    אני כל כך מצטער לשמוע על האבחנה שלך.

כבן משפחה של חולה סרטן, ייתכן שתרצה לשקול לנקוט בצעדים כדי להבטיח שזכויות החולה מוגנות. בדרך כלל מומלץ להתחיל את התהליך במוקדם ולא במאוחר, שכן לחלק מהיתרונות והשירותים עשויים להיות מגבלות זמן או לדרוש תכנון מוקדם.

בישראל קיימים מספר ארגונים ומשאבים לתמיכה בחולי סרטן ובני משפחתם. כמה דוגמאות כוללות:

* האגודה הישראלית למלחמה בסרטן (ICA): מציעה תמיכה רגשית, סיוע כלכלי והכוונה בניווט במערכת הבריאות.
* משרד הבריאות: מספק מידע על תוכניות במימון ממשלתי, כגון כיסוי תרופות ושירותי טיפול ביתי.
* המוסד לביטוח לאומי (ביטוח לאומי): מעניק תמיכה כספית לחולי סרטן ובני משפחותיהם.

זה רעיון טוב לפנות לארגונים אלה או לצוות הבריאות של המטופל שלך כדי לקבל הבנה טובה יותר של הזכויות והמשאבים הספציפיים הזמינים.
    """
    auth_key = "61958d07-900f-406f-b135-9fd60ca75c10:fx"  # Replace with your key
    translator = deepl.Translator(auth_key)
    result = translator.translate_text(chat_answer, target_lang="he")
    hebrew_text = result.text
    return hebrew_text


async def get_chat_answer(text):
    url = "http://localhost:11434/api/chat"
    modal_name = "example"
    payload = {
        "model": modal_name,
        "messages": [
            {"role": "user", "content": text}
        ]
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response_lines = [json.loads(line.strip()) for line in response.text.split('\n') if line.strip()]
    chat_answer = ""
    for word_dict in response_lines:
        if word_dict['done'] is True:
            break
        chat_answer += word_dict['message']['content']
    return chat_answer
