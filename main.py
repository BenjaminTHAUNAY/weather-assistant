#!/usr/bin/env python3
"""
Weather Analysis Assistant - Command Line Interface
Entry point for the Weather Agent system.
"""

import sys
import argparse
from agent import WeatherAgent


def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description='Weather Analysis Assistant - Get current weather and forecasts',
        epilog='Examples:\n'
               '  python main.py --query "weather in Paris"\n'
               '  python main.py --query "forecast for London for 3 days"\n'
               '  python main.py --city "Riga"\n'
               '  python main.py --city "Tokyo" --forecast --days 5'
    )
    
    parser.add_argument(
        '--query', '-q',
        type=str,
        help='Natural language query (e.g., "weather in Paris", "forecast for London tomorrow")'
    )
    
    parser.add_argument(
        '--city', '-c',
        type=str,
        help='City name for simple weather lookup'
    )
    
    parser.add_argument(
        '--forecast', '-f',
        action='store_true',
        help='Get forecast instead of current weather'
    )
    
    parser.add_argument(
        '--days', '-d',
        type=int,
        default=3,
        help='Number of days for forecast (default: 3, max: 5)'
    )
    
    args = parser.parse_args()
    
    # Build query from arguments
    if args.query:
        query = args.query
    elif args.city:
        if args.forecast:
            query = f"forecast for {args.city} for {args.days} days"
        else:
            query = f"weather in {args.city}"
    else:
        parser.print_help()
        sys.exit(1)
    
    # Create agent and process query
    agent = WeatherAgent()
    print(f"\n Processing: {query}\n")
    print("-" * 50)
    
    result = agent.process_query(query)
    print(result)
    
    if "Error" in result:
        sys.exit(1)


if __name__ == "__main__":
    main()