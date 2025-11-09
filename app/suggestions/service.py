import requests


def query_openlibrary(query, limit=8, base_url='https://openlibrary.org'):
    if not query:
        return []
    params = {'q': query, 'limit': limit}
    url = f"{base_url}/search.json"
    resp = requests.get(url, params=params, timeout=5)
    resp.raise_for_status()
    data = resp.json()
    docs = data.get('docs', [])
    suggestions = []
    for d in docs[:limit]:
        title = d.get('title') or d.get('title_suggest')
        authors = ', '.join(d.get('author_name', [])) if d.get('author_name') else None
        year = d.get('first_publish_year')
        isbns = d.get('isbn', [])
        isbn = isbns[0] if isbns else None
        suggestions.append({'title': title, 'authors': authors, 'year': year, 'isbn': isbn})
    return suggestions
