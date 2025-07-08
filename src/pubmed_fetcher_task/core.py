import requests
import xml.etree.ElementTree as ET
import pandas as pd
import re

COMPANY_KEYWORDS = ["pharma", "biotech", "therapeutics", "inc", "ltd", "llc", "gmbh", "pfizer", "roche", "novartis", "astrazeneca"]

def get_pubmed_ids(query, retmax=50, debug=False):
    if debug:
        print(f"[DEBUG] Searching PubMed for: {query}")
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": retmax}
    response = requests.get(url, params=params)
    response.raise_for_status()
    ids = response.json()['esearchresult']['idlist']
    if debug:
        print(f"[DEBUG] Found PMIDs: {ids}")
    return ids

def fetch_details(pmids, debug=False):
    if debug:
        print(f"[DEBUG] Fetching details for PMIDs: {pmids}")
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {"db": "pubmed", "retmode": "xml", "id": ",".join(pmids)}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.text

def parse_articles(xml_text, debug=False):
    root = ET.fromstring(xml_text)
    records = []

    for article in root.findall(".//PubmedArticle"):
        pmid = article.findtext(".//PMID")
        title = article.findtext(".//ArticleTitle")
        pub_date_node = article.find(".//PubDate")
        pub_date = ""

        if pub_date_node is not None:
            year = pub_date_node.findtext("Year") or ""
            month = pub_date_node.findtext("Month") or ""
            day = pub_date_node.findtext("Day") or ""
            pub_date = f"{year}-{month}-{day}".strip("-")

        authors = article.findall(".//Author")
        non_academic_authors = []
        company_affiliations = set()
        corresponding_email = ""

        for author in authors:
            affils = author.findall("AffiliationInfo")
            fullname = f"{author.findtext('ForeName', '')} {author.findtext('LastName', '')}".strip()

            for affil in affils:
                affil_text = affil.findtext("Affiliation", "")
                if not affil_text:
                    continue

                # Email detection
                emails = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", affil_text)
                if emails and not corresponding_email:
                    corresponding_email = emails[0]

                if any(keyword in affil_text.lower() for keyword in COMPANY_KEYWORDS):
                    company_affiliations.add(affil_text)
                    non_academic_authors.append(fullname)

        if company_affiliations:
            record = {
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academic Author(s)": "; ".join(set(non_academic_authors)),
                "Company Affiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            }
            if debug:
                print(f"[DEBUG] Record: {record}")
            records.append(record)

    return records

def write_to_csv(records, file_path, debug=False):
    df = pd.DataFrame(records)
    df.to_csv(file_path, index=False)
    if debug:
        print(f"[DEBUG] Saved {len(df)} records to {file_path}")