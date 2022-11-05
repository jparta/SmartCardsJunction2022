import json
import random
from copy import copy
from datetime import date, timedelta
from pprint import pprint


n = 100

def days_to_seconds(days):
    delta = timedelta(days=days)
    seconds = (delta.days * 24 * 60 * 60) + delta.seconds
    return seconds

def random_recent_date():
    start_years_ago = 5
    end = date.today()
    start = copy(end)
    start = date(year=start.year - start_years_ago, month=start.month, day=start.day)
    delta = end - start
    delta_seconds = days_to_seconds(delta.days)
    random_seconds = random.randrange(delta_seconds)
    return start + timedelta(seconds=random_seconds)

def increment_date_random(date):
    delta_range = (0, 14)
    min_seconds = days_to_seconds(delta_range[0])
    max_seconds = days_to_seconds(delta_range[1])
    random_seconds = random.randrange(min_seconds, max_seconds)
    return date + timedelta(seconds=random_seconds)

def event_happens(chance):
    return random.random() < chance

def transaction_counts(n):
    """"Returns (total count, since online, date) pairs"""
    online_chance = 0.9
    offline_anomaly_chance = 0.005
    offline_anomaly_size_range = (2, 5)
    txs_start_range = (0, 5)
    txs_delta_range = (0, 10)
    cur_total = random.randint(*txs_start_range)
    cur_since_online = 0
    cur_date = random_recent_date()
    data = {
        "totals": [],
        "txs_since_online": [],
        "date": [],
    }
    for _ in range(n):
        data["totals"].append(cur_total)
        data["txs_since_online"].append(cur_since_online)
        data["date"].append(cur_date)
        count_delta = random.randint(*txs_delta_range)
        cur_total += count_delta
        cur_date = increment_date_random(cur_date)
        for _ in range(count_delta):
            cur_since_online += 1
            if event_happens(online_chance):
                cur_since_online = 0
        if event_happens(offline_anomaly_chance):
            cur_since_online += random.randint(*offline_anomaly_size_range)
    return data


if __name__ == "__main__":
    pprint(transaction_counts(n))