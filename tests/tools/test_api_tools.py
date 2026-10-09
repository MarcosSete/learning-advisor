import json

import httpx
import pytest

from app.tools import api_tools


class FakeResponse:
    def __init__(self, payload, status_error=None):
        self._payload = payload
        self._status_error = status_error

    def raise_for_status(self):
        if self._status_error is not None:
            raise self._status_error

    def json(self):
        return self._payload


def test_search_github_learning_repositories_returns_limited_metadata(monkeypatch):
    captured = {}

    def fake_get(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse(
            {
                "items": [
                    {
                        "full_name": "example/ml-notes",
                        "html_url": "https://github.com/example/ml-notes",
                        "description": "Machine learning course notes",
                        "stargazers_count": 42,
                        "language": "Python",
                    },
                    {
                        "full_name": "example/ai-course",
                        "html_url": "https://github.com/example/ai-course",
                        "description": None,
                        "stargazers_count": 8,
                        "language": None,
                    },
                ]
            }
        )

    monkeypatch.setattr(api_tools.httpx, "get", fake_get)

    result = api_tools.search_github_learning_repositories.invoke(
        {"query": "  machine learning   course notes ", "limit": 2}
    )

    assert json.loads(result) == [
        {
            "full_name": "example/ml-notes",
            "url": "https://github.com/example/ml-notes",
            "description": "Machine learning course notes",
            "stars": 42,
            "language": "Python",
        },
        {
            "full_name": "example/ai-course",
            "url": "https://github.com/example/ai-course",
            "description": None,
            "stars": 8,
            "language": None,
        },
    ]
    assert captured["url"] == api_tools.GITHUB_REPOSITORY_SEARCH_URL
    assert captured["params"] == {
        "q": "machine learning course notes",
        "per_page": 2,
    }
    assert captured["timeout"] == api_tools.REQUEST_TIMEOUT_SECONDS


@pytest.mark.parametrize(
    ("query", "limit", "message"),
    [
        ("  ", 5, "query cannot be empty"),
        ("machine learning", 0, "limit must be between 1 and 10"),
        ("machine learning", 11, "limit must be between 1 and 10"),
    ],
)
def test_search_github_learning_repositories_validates_inputs(
    query, limit, message
):
    with pytest.raises(ValueError, match=message):
        api_tools.search_github_learning_repositories.invoke(
            {"query": query, "limit": limit}
        )


def test_search_github_learning_repositories_handles_http_errors(monkeypatch):
    def fake_get(*args, **kwargs):
        return FakeResponse(
            {},
            status_error=httpx.HTTPStatusError(
                "rate limited",
                request=httpx.Request("GET", api_tools.GITHUB_REPOSITORY_SEARCH_URL),
                response=httpx.Response(403),
            ),
        )

    monkeypatch.setattr(api_tools.httpx, "get", fake_get)

    with pytest.raises(RuntimeError, match="request failed"):
        api_tools.search_github_learning_repositories.invoke(
            {"query": "graph machine learning", "limit": 3}
        )


def test_search_github_learning_repositories_rejects_unexpected_payload(
    monkeypatch,
):
    monkeypatch.setattr(api_tools.httpx, "get", lambda *args, **kwargs: FakeResponse({}))

    with pytest.raises(RuntimeError, match="unexpected response"):
        api_tools.search_github_learning_repositories.invoke(
            {"query": "graph machine learning", "limit": 3}
        )
