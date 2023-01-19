from deta import Deta
from dotenv import load_dotenv
import os

load_dotenv()
key = os.getenv('project_key')

deta = Deta(key)

db = deta.Base('budget')

def save_data(date, period, incomes, expenses, comments):
    db.put({
        'date': date,
        'period': period,
        'incomes': incomes,
        'expenses': expenses,
        'comments': comments
    })

def fetch_period():
    periods = db.fetch()
    return periods.items

def get_period(p):
    p = db.fetch({'period':p})
    return p