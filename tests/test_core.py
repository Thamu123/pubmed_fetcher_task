from pubmed_fetcher_task.core import get_pubmed_ids, fetch_details, parse_articles

# Test 2: get pubmed ids
def test_get_pubmed_ids():
    ids = get_pubmed_ids("cancer")
    assert isinstance(ids, list)
    assert len(ids) > 0

# Test 2: fetch_details
def test_fetch_details():
    ids = get_pubmed_ids("covid")
    xml_data = fetch_details(ids)
    assert isinstance(xml_data, str)
    assert "<PubmedArticle>" in xml_data

# Test 3: parse_articles
def test_parse_articles():
    ids = get_pubmed_ids("covid")
    xml_data = fetch_details(ids)
    articles = parse_articles(xml_data)
    assert isinstance(articles, list)
    assert "PubmedID" in articles[0]
    assert "Title" in articles[0]
