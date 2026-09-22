from youtubesearchpython import VideosSearch

BAD_TITLE_WORDS = [
    "official video", "official audio", "music", "song", "lyrics",
    "mv", "feat.", "remix", "dance", "parody"
]
EDU_TITLE_HINTS = ["lecture", "class", "tutorial", "lesson", "explained", "for kids", "introduction", "crash course"]
EDU_CHANNEL_HINTS = ["academy", "university", "edu", "khan academy", "ted-ed", "veritasium", "mit opencourseware",
                     "numberphile", "minutephysics", "national geographic", "nptel", "byju", "iit"]

def _looks_educational(result: dict) -> bool:
    title = (result.get("title") or "").lower()
    channel = (result.get("channel") or {}).get("name", "")
    channel = channel.lower() if isinstance(channel, str) else str(channel).lower()
    if any(b in title for b in BAD_TITLE_WORDS):
        return False
    if any(h in title for h in EDU_TITLE_HINTS):
        return True
    if any(h in channel for h in EDU_CHANNEL_HINTS):
        return True
    # Prefer if the description includes learning cues
    desc = " ".join([d.get("text","") for d in result.get("descriptionSnippet") or []]).lower()
    if any(h in desc for h in ["learn", "explain", "lecture", "class", "tutorial"]):
        return True
    return False

def get_youtube_video_link(query: str) -> str | None:
    # Bias the search toward educational content
    q = f"{query} explanation tutorial lecture"
    vs = VideosSearch(q, limit=8)
    results = vs.result().get("result", [])
    # Pick the first educational-looking result
    for r in results:
        if _looks_educational(r):
            return r.get("link")
    # Fallback to first result if nothing matches
    return results[0].get("link") if results else None

def to_embed_url(link: str | None) -> str | None:
    if not link:
        return None
    # streamlit accepts the raw link; but return the same for simplicity
    return link
