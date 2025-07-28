"""CLI entry point for the application."""

import argparse


def parse_args() -> str:
    """Parse command line arguments and run the application."""
    parser = argparse.ArgumentParser(
        description="Country Picker GUI"
    )
    parser.add_argument(
        '--select',
        metavar='COUNTRY',
        type=str,
        help='Pre-select a country by name (e.g., "Switzerland")'
    )
    args = parser.parse_args()
    return args.select
