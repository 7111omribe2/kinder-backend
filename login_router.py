import datetime as dt

from fastapi import APIRouter
from shapely.geometry import Point

users = [
    {
        'username': 'omri',
        'connection_type': 'brother',
        'decease': 'cancer1',
        'age': 23,
        'location': Point(31.93923698780856, 34.7952495596364),
        'for_how_long': dt.timedelta(days=90)
    },
    {
        'username': 'nitay',
        'connection_type': 'brother',
        'decease': 'cancer1',
        'age': 22,
        'location': Point(31.896207264989634, 34.79677389252961),
        'for_how_long': dt.timedelta(days=30)
    },
    {
        'username': 'daniel',
        'connection_type': 'mother',
        'decease': 'cancer2',
        'age': 23,
        'location': Point(31.87838047674572, 34.736044728911246),
        'for_how_long': dt.timedelta(days=765)
    },
    {
        'username': 'shira',
        'connection_type': 'sister',
        'decease': 'cancer2',
        'age': 26,
        'location': Point(32.086200713100055, 34.781161271332124),
        'for_how_long': dt.timedelta(days=12)
    },
    {
        'username': 'yonatan',
        'connection_type': 'mother',
        'decease': 'cancer2',
        'age': 23,
        'location': Point(32.07714016816094, 34.77096406145831),
        'for_how_long': dt.timedelta(days=765)
    },
]
communities = [
    {
        'decease': 'cancer1'
    },
    {
        'decease': 'cancer2'
    },
    {
        'decease': 'cancer3'
    }
]

auth_api_router = APIRouter()


@auth_api_router.post("/getUsers")
async def regular_login_for_access_token():
    return users
