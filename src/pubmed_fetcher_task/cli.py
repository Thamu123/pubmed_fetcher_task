import argparse
import pandas as pd
from pubmed_fetcher_task.core import get_pubmed_ids, fetch_details, parse_articles, write_to_csv
import sys


def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers related to pharma/biotech companies.")
    parser.add_argument("query", help="Search query for PubMed")
    parser.add_argument("-f", "--file", help="Output CSV filename (if not given, prints to console)")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging")

    args = parser.parse_args()

    try:
        pmids = get_pubmed_ids(args.query, debug=args.debug)
        xml = fetch_details(pmids, debug=args.debug)
        records = parse_articles(xml, debug=args.debug)

        if not records:
            print("No company-affiliated articles found.")
            return

        if args.file:
            write_to_csv(records, args.file, debug=args.debug)
        else:
            df = pd.DataFrame(records)
            print(df.to_string(index=False))

    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
