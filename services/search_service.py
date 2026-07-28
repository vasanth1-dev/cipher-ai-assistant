from __future__ import annotations


class SearchService:
    """
    Placeholder Search Service.

    This service will later be extended to support:
    - Web search
    - Local file search
    - AI-powered search
    """

    def search(self, query: str) -> str:
        query = query.strip()

        if not query:
            return "Please provide a search query."

        return f"Search service is not implemented yet. Query: {query}"


search_service = SearchService()