import datetime
import argparse
import json
import os
from flask import Flask, jsonify
from waitress import serve

def isBinDay(start_week=1, frequency=2, days=None):
    if days is None:
        days = [2, 3]  # Tuesday and Wednesday by default
    
    Date = datetime.datetime.now()
    Year, WeekNum, DOW = Date.isocalendar()

    # Check if current week matches the pattern: (current - start) % frequency == 0
    week_check = (WeekNum - start_week) % frequency == 0
    
    isBinday = week_check and DOW in days
    return isBinday

def main():
    # Try to load Home Assistant addon options
    options_file = '/data/options.json'
    if os.path.exists(options_file):
        with open(options_file, 'r') as f:
            options = json.load(f)
        start_week = options.get('start_week', 1)
        frequency = options.get('frequency', 2)
        days = options.get('days', [2, 3])
        
        # Run as HTTP service for Home Assistant
        app = Flask(__name__)
        
        @app.route('/status')
        def status():
            is_bin_day = isBinDay(start_week=start_week, frequency=frequency, days=days)
            return jsonify({
                'bin_day': is_bin_day,
                'start_week': start_week,
                'frequency': frequency,
                'days': days,
                'message': 'Today is a bin day.' if is_bin_day else 'Today is not a bin day.'
            })
        
        @app.route('/')
        def home():
            is_bin_day = isBinDay(start_week=start_week, frequency=frequency, days=days)
            return jsonify({
                'bin_day': is_bin_day,
                'message': 'Today is a bin day.' if is_bin_day else 'Today is not a bin day.'
            })
        
        print(f"Starting Bin Day Checker service (start_week={start_week}, frequency={frequency}, days={days})")
        print("Listening on http://0.0.0.0:8099")
        serve(app, host='0.0.0.0', port=8099)
    else:
        # Run as CLI tool
        parser = argparse.ArgumentParser(description='Check if today is a bin day.')
        parser.add_argument('--start-week', '-s', 
                           type=int,
                           default=1,
                           help='Starting week number for the pattern (default: 1)')
        parser.add_argument('--frequency', '-f',
                           type=int,
                           default=2,
                           help='Frequency in weeks (default: 2 for fortnightly)')
        parser.add_argument('--days', '-d',
                           type=int,
                           nargs='+',
                           default=[2, 3],
                           help='Days of week for bin day (1=Mon, 2=Tue, ..., 7=Sun). Default: 2 3 (Tue Wed)')
        
        args = parser.parse_args()
        
        if isBinDay(start_week=args.start_week, frequency=args.frequency, days=args.days):
            print("Today is a bin day.")
        else:
            print("Today is not a bin day.")

if __name__ == "__main__":
    main()