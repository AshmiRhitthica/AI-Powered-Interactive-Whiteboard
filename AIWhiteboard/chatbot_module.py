import requests
import re

WIKIPEDIA_API = "https://en.wikipedia.org/w/api.php"

EDU_HINTS = {
    "mathematics", "geometry", "physics", "chemistry",
    "biology", "education", "science"
}

BLOCK_HINTS = {
    "song", "music", "album", "film", "television",
    "video games", "novels", "band", "single"
}


def _clean_html(text):
    """Remove HTML tags from Wikipedia snippets."""
    return re.sub(r"<[^>]+>", "", text)


def _search_wikipedia(query):
    """Search Wikipedia using its REST/API endpoint."""

    params = {
        "action": "query",
        "format": "json",
        "list": "search",
        "srsearch": query,
        "srlimit": 10,
    }

    headers = {
        "User-Agent": "AI-Interactive-Whiteboard/1.0"
    }

    response = requests.get(
        WIKIPEDIA_API,
        params=params,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    return data.get("query", {}).get("search", [])


def _get_page_summary(title):
    """Get the summary of a specific Wikipedia page."""

    params = {
        "action": "query",
        "format": "json",
        "prop": "extracts",
        "exintro": True,
        "explaintext": True,
        "redirects": 1,
        "titles": title,
    }

    headers = {
        "User-Agent": "AI-Interactive-Whiteboard/1.0"
    }

    response = requests.get(
        WIKIPEDIA_API,
        params=params,
        headers=headers,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()

    pages = data.get("query", {}).get("pages", {})

    for page in pages.values():
        extract = page.get("extract", "")

        if extract:
            return extract

    return ""


def _pick_best_page(query):
    """Choose the most relevant Wikipedia result."""

    results = _search_wikipedia(query)

    if not results:
        return None

    query_clean = query.strip().lower()

    # First preference: exact title match
    for result in results:
        title = result.get("title", "")

        if title.lower() == query_clean:
            return title

    # Avoid obvious entertainment results
    for result in results:
        title = result.get("title", "").lower()

        if any(block in title for block in BLOCK_HINTS):
            continue

        return result.get("title")

    return results[0].get("title")


def get_definition_wikipedia(query: str, sentences: int = 3) -> str:

    if not query or not query.strip():
        return ""

    query = query.strip()

    try:

        title = _pick_best_page(query)

        if not title:
            return f"No encyclopedia entry found for '{query}'."

        summary = _get_page_summary(title)

        if not summary:
            return f"No definition available for '{title}'."

        # Keep approximately the requested number of sentences
        sentences_found = re.split(
            r"(?<=[.!?])\s+",
            summary.strip()
        )

        definition = " ".join(
            sentences_found[:sentences]
        )

        return definition

    except requests.exceptions.Timeout:
        return (
            "Wikipedia took too long to respond. "
            "Please try again."
        )

    except requests.exceptions.RequestException as e:
        return (
            f"Unable to connect to Wikipedia right now. "
            f"Please try again. ({e})"
        )

    except Exception as e:
        return f"[Definition error] {e}"