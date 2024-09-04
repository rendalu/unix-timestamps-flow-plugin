import sys
import json
from datetime import datetime, timedelta
from time import time_ns

def parse_input(user_input):
    user_input = user_input.strip().lower()
    
    # Check for date math expressions
    if user_input.startswith("now"):
        return evaluate_date_math(user_input)
    
    # Try to parse the input as a date
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            dt = datetime.strptime(user_input, fmt)
            return dt.timestamp() * 1000, dt.timestamp() * 1_000_000_000
        except ValueError:
            continue
    
    return None

def evaluate_date_math(expression):
    # Simple date math: e.g., "now + 1 day", "now - 2 hours"
    now = datetime.now()
    parts = expression.split()
    
    if len(parts) < 4 or parts[0] != "now":
        return None

    operator = parts[1]
    amount = int(parts[2])
    unit = parts[3]

    delta = timedelta()
    if "day" in unit:
        delta = timedelta(days=amount)
    elif "hour" in unit:
        delta = timedelta(hours=amount)
    elif "minute" in unit:
        delta = timedelta(minutes=amount)
    elif "second" in unit:
        delta = timedelta(seconds=amount)
    else:
        return None

    result_time = now + delta if operator == "+" else now - delta
    return result_time.timestamp() * 1000, result_time.timestamp() * 1_000_000_000

def generate_timestamps(user_input):
    timestamps = parse_input(user_input)
    if timestamps is None:
        return []

    ms_timestamp, ns_timestamp = timestamps
    return [
        {
            "Title": f"Millisecond Timestamp: {int(ms_timestamp)}",
            "SubTitle": "Press Enter to copy to clipboard",
            "IcoPath": "icon.png",
            "JsonRPCAction": {
                "method": "copy_to_clipboard",
                "parameters": [str(int(ms_timestamp))],
            }
        },
        {
            "Title": f"Nanosecond Timestamp: {int(ns_timestamp)}",
            "SubTitle": "Press Enter to copy to clipboard",
            "IcoPath": "icon.png",
            "JsonRPCAction": {
                "method": "copy_to_clipboard",
                "parameters": [str(int(ns_timestamp))],
            }
        }
    ]

def copy_to_clipboard(text):
    return {
        "method": "set_clipboard",
        "parameters": [text]
    }

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(json.dumps([]))  # No input provided
    else:
        user_input = " ".join(sys.argv[1:])  # Join all arguments as a single input
        results = generate_timestamps(user_input)
        print(json.dumps(results))