import json

import httpx
from langchain_core.tools import tool


GITHUB_REPOSITORY_SEARCH_URL = "https://api.github.com/search/repositories"
REQUEST_TIMEOUT_SECONDS = 10.0
MAX_RESULTS = 10


@tool
def search_github_learning_repositories(query: str, limit: int = 5) -> str:
    """Search GitHub for candidate repositories containing learning materials.

    Returns repository metadata for discovery only. Results are not verified as
    official, free, complete, or pedagogically suitable resources.
    """
    normalized_query = " ".join(query.split())
    if not normalized_query:
        raise ValueError("query cannot be empty or whitespace-only")
    if not 1 <= limit <= MAX_RESULTS:
        raise ValueError(f"limit must be between 1 and {MAX_RESULTS}")

    try:
        response = httpx.get(
            GITHUB_REPOSITORY_SEARCH_URL,
            params={"q": normalized_query, "per_page": limit},
            headers={
                "Accept": "application/vnd.github+json",
                "X-GitHub-Api-Version": "2022-11-28",
            },
            timeout=REQUEST_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
        payload = response.json()
    except httpx.HTTPError as exc:
        raise RuntimeError("GitHub repository search request failed") from exc
    except ValueError as exc:
        raise RuntimeError("GitHub repository search returned invalid JSON") from exc

    items = payload.get("items") if isinstance(payload, dict) else None
    if not isinstance(items, list):
        raise RuntimeError("GitHub repository search returned an unexpected response")

    repositories = []
    for item in items[:limit]:
        if not isinstance(item, dict):
            continue
        full_name = item.get("full_name")
        html_url = item.get("html_url")
        if not isinstance(full_name, str) or not isinstance(html_url, str):
            continue
        repositories.append(
            {
                "full_name": full_name,
                "url": html_url,
                "description": item.get("description"),
                "stars": item.get("stargazers_count"),
                "language": item.get("language"),
            }
        )

    return json.dumps(repositories, ensure_ascii=False)
