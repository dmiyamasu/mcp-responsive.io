#!/usr/bin/env python3
#
# MCP Server to search the Responsive Content Library using fastmcp
#
import os
import httpx
from typing import Any, Dict, List
from mcp.server.fastmcp import FastMCP
import json

mcp = FastMCP("responsive_content")
base_url = "https://app.rfpio.com"
api_token = os.environ.get('RESPONSIVE_API_TOKEN')

async def make_responsive_request(data: Dict[str, Any]) -> dict[str, Any] | None:
    """Make a request to the Responsive API with error handling."""

    if not api_token:
        raise Exception("RESPONSIVE_API_TOKEN environment variable not set")

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    url = f"{base_url}/rfpserver/ext/v1/answer-lib/search"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, headers=headers, json=data, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except httpx.RequestError as e:
            print(f"Error during request: {e}")
            return {"error": f"Error communicating with Responsive API: {str(e)}"}
        except httpx.HTTPStatusError as e:
            print(f"HTTP Error: {e.response.status_code}, {e.response.text}")
            return {"error": f"HTTP Error: {e.response.status_code}"}
        except json.JSONDecodeError as e:
            print(f"JSON Decode Error: {e}")
            return {"error": "Invalid JSON response from server"}
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return {"error": f"An unexpected error occurred: {str(e)}"}


@mcp.tool()
async def search_content(keyword: str, approvers: List[str] = [], businessUnits: List[str] = [],
                   collectionList: List[str] = [], cursor: str = "*", customFields: Dict[str, Any] = {},
                   facetFields: List[str] = [], flagFilter: str = "ALL", hasAlertText: bool = False,
                   hasAttachment: bool = False, hasImage: bool = False, hasOpenComment: bool = False,
                   idsList: List[str] = [], languageSearch: List[str] = [], lastUpdatedBy: List[str] = [],
                   limit: int = 25, metadata: bool = False, owners: List[str] = [],
                   projectSearch: List[str] = [], sectionSearch: List[str] = [], starRating: int = 0,
                   tagSearch: List[str] = []) -> dict[str, Any]:
    """
    Search the Responsive Content Library for matching Q/A pairs using keywords
    and additional filters.

    Args:
        keyword: Keyword to search for
        approvers: List of approvers
        businessUnits: List of business units
        collectionList: List of collections
        cursor: Cursor for pagination
        customFields: JSON object for custom fields
        facetFields: List of facet fields
        flagFilter: Flag filter (ALL, STARRED, UNSTARRED)
        hasAlertText: Filter for items with alert text
        hasAttachment: Filter for items with attachments
        hasImage: Filter for items with images
        hasOpenComment: Filter for items with open comments
        idsList: List of IDs
        languageSearch: List of languages
        lastUpdatedBy: List of last updated by users
        limit: Maximum number of results
        metadata: Include metadata in results
        owners: List of owners
        projectSearch: List of projects
        sectionSearch: List of sections
        starRating: Minimum star rating
        tagSearch: List of tags

    Returns:
        The JSON response from the Responsive API.
    """

    data = {
        "keyword": keyword,
        "approvers": approvers,
        "businessUnits": businessUnits,
        "collectionList": collectionList,
        "cursor": cursor,
        "customFields": customFields,
        "facetFields": facetFields,
        "flagFilter": flagFilter,
        "hasAlertText": hasAlertText,
        "hasAttachment": hasAttachment,
        "hasImage": hasImage,
        "hasOpenComment": hasOpenComment,
        "idsList": idsList,
        "languageSearch": languageSearch,
        "lastUpdatedBy": lastUpdatedBy,
        "limit": limit,
        "metadata": metadata,
        "owners": owners,
        "projectSearch": projectSearch,
        "sectionSearch": sectionSearch,
        "starRating": starRating,
        "tagSearch": tagSearch
    }

    print(f"Search data: {json.dumps(data, indent=2)}")  # Log the request
    return await make_responsive_request(data)


if __name__ == "__main__":
    mcp.run(transport='stdio')
