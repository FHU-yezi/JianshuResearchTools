from typing import Dict, List, Union, Optional

from httpx import get as httpx_get
from httpx import post as httpx_post
from lxml import etree
from lxml.etree import _Element

from .headers import (BeikeIsland_request_header, PC_header,
                      api_request_header, mobile_header)

try:
    from ujson import loads as json_loads
except ImportError:
    from json import loads as json_loads

__all__ = [
    "GetArticleJsonDataApi", "GetArticleHtmlJsonDataApi",
    "GetArticleCommentsJsonDataApi", "GetBeikeIslandTradeRankListJsonDataApi",
    "GetBeikeIslandTradeListJsonDataApi", "GetCollectionJsonDataApi",
    "GetCollectionEditorsJsonDataApi",
    "GetCollectionRecommendedWritersJsonDataApi",
    "GetCollectionSubscribersJsonDataApi", "GetCollectionArticlesJsonDataApi",
    "GetIslandJsonDataApi", "GetIslandPostsJsonDataApi",
    "GetNotebookJsonDataApi", "GetDailyArticleRankListJsonDataApi",
    "GetArticlesFPRankListJsonDataApi", "GetUserJsonDataApi",
    "GetUserPCHtmlDataApi", "GetUserCollectionsAndNotebooksJsonDataApi",
    "GetUserArticlesListJsonDataApi", "GetUserFollowingListHtmlDataApi",
    "GetUserFollowersListHtmlDataApi", "GetUserNextAnniversaryDayHtmlDataApi",
    "GetIslandPostJsonDataApi", "GetUserTimelineHtmlDataApi"
]


def GetArticleJsonDataApi(article_url: str) -> Dict:
    request_url = article_url.replace("https://www.jianshu.com/",
                                      "https://www.jianshu.com/asimov/")
    source = httpx_get(request_url, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetArticleHtmlJsonDataApi(article_url: str) -> _Element:
    source = httpx_get(article_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    json_obj = json_loads(html_obj.xpath("//script[@id='__NEXT_DATA__']/text()")[0])
    return json_obj


def GetArticleCommentsJsonDataApi(article_id: int, page: int, count: int,
                                  author_only: bool, order_by: str) -> Dict:
    params = {
        "page": page,
        "count": count,
        "author_only": author_only,
        "order_by": order_by
    }
    request_url = f"https://www.jianshu.com/shakespeare/notes/{article_id}/comments"
    source = httpx_get(request_url, params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetBeikeIslandTradeRankListJsonDataApi(ranktype: Union[int, None], pageIndex: Union[int, None]) -> Dict:
    params = {
        "ranktype": ranktype,
        "pageIndex": pageIndex
    }
    source = httpx_post("https://www.beikeisland.com/api/Trade/getTradeRankList",
                        headers=BeikeIsland_request_header, json=params).content
    json_obj = json_loads(source)
    return json_obj


def GetBeikeIslandTradeListJsonDataApi(pageIndex: int, retype: int):
    params = {
        "pageIndex": pageIndex,
        "retype": retype
    }
    source = httpx_post("https://www.beikeisland.com/api/Trade/getTradeList",
                        headers=BeikeIsland_request_header, json=params).content
    json_obj = json_loads(source)
    return json_obj


def GetCollectionJsonDataApi(collection_url: str) -> Dict:
    request_url = collection_url.replace("https://www.jianshu.com/c/", "https://www.jianshu.com/asimov/collections/slug/")
    source = httpx_get(request_url, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetCollectionEditorsJsonDataApi(collection_id: int, page: int) -> Dict:
    request_url = f"https://www.jianshu.com/collections/{collection_id}/editors"
    params = {
        "page": page
    }
    source = httpx_get(request_url, params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetCollectionRecommendedWritersJsonDataApi(collection_id: int, page: int, count: int) -> Dict:
    params = {
        "collection_id": collection_id,
        "page": page,
        "count": count
    }
    source = httpx_get("https://www.jianshu.com/collections/recommended_users",
                       params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetCollectionSubscribersJsonDataApi(collection_id: int, max_sort_id: int) -> Dict:
    request_url = f"https://www.jianshu.com/collection/{collection_id}/subscribers"
    params = {
        "max_sort_id": max_sort_id
    }
    source = httpx_get(request_url, params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetCollectionArticlesJsonDataApi(collection_slug: str, page: int, count: int, order_by: str) -> Dict:
    request_url = f"https://www.jianshu.com/asimov/collections/slug/{collection_slug}/public_notes"
    params = {
        "page": page,
        "count": count,
        "order_by": order_by
    }
    source = httpx_get(request_url, params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetIslandJsonDataApi(island_url: str) -> Dict:
    request_url = island_url.replace("https://www.jianshu.com/g/", "https://www.jianshu.com/asimov/groups/")
    source = httpx_get(request_url, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetIslandPostsJsonDataApi(group_slug: str, max_id: int,
                              count: int, topic_id: int, order_by: str):
    params = {
        "group_slug": group_slug,
        "order_by": order_by,
        "max_id": max_id,
        "count": count,
        "topic_id": topic_id
    }
    source = httpx_get("https://www.jianshu.com/asimov/posts",
                       params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetNotebookJsonDataApi(notebook_url: str) -> Dict:
    request_url = notebook_url.replace("https://www.jianshu.com/", "https://www.jianshu.com/asimov/")
    source = httpx_get(request_url, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetNotebookArticlesJsonDataApi(notebook_url: str, page: int,
                                   count: int, order_by: str) -> Dict:
    request_url = notebook_url.replace("https://www.jianshu.com/nb/",
                                       "https://www.jianshu.com/asimov/notebooks/") + "/public_notes/"
    params = {
        "page": page,
        "count": count,
        "order_by": order_by
    }
    source = httpx_get(request_url, params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetAssetsRankJsonDataApi(max_id: int, since_id: int) -> Dict:
    params = {
        "max_id": max_id,
        "since_id": since_id
    }
    source = httpx_get("https://www.jianshu.com/asimov/fp_rankings", params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetDailyArticleRankListJsonDataApi() -> Dict:
    source = httpx_get("https://www.jianshu.com/asimov/daily_activity_participants/rank", headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetArticlesFPRankListJsonDataApi(date: str, type_: Optional[str]) -> Dict:  # ????????????????????????
    params = {
        "date": date,
        "type": type_
    }
    source = httpx_get("https://www.jianshu.com/asimov/fp_rankings/voter_notes", params=params, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetUserJsonDataApi(user_url: str) -> Dict:
    request_url = user_url.replace("https://www.jianshu.com/u/", "https://www.jianshu.com/asimov/users/slug/")
    source = httpx_get(request_url, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetUserPCHtmlDataApi(user_url: str) -> _Element:
    source = httpx_get(user_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    return html_obj


def GetUserCollectionsAndNotebooksJsonDataApi(user_url: str, user_slug: str) -> Dict:
    request_url = user_url.replace("/u/", "/users/") + "/collections_and_notebooks"
    params = {
        "slug": user_slug
    }
    source = httpx_get(request_url, headers=api_request_header, params=params).content
    json_obj = json_loads(source)
    return json_obj


def GetUserArticlesListJsonDataApi(user_url: str, page: int,
                                   count: int, order_by: str) -> Dict:
    request_url = user_url.replace("/u/", "/asimov/users/slug/") + "/public_notes"
    params = {
        "page": page,
        "count": count,
        "order_by": order_by
    }
    source = httpx_get(request_url, headers=api_request_header, params=params).content
    json_obj = json_loads(source)
    return json_obj


def GetUserFollowingListHtmlDataApi(user_url: str, page: int) -> _Element:
    request_url = user_url.replace("/u/", "/users/") + "/following"
    params = {
        "page": page
    }
    source = httpx_get(request_url, headers=PC_header, params=params).content
    html_obj = etree.HTML(source)
    return html_obj


def GetUserFollowersListHtmlDataApi(user_url: str, page: int) -> _Element:
    request_url = user_url.replace("/u/", "/users/") + "/followers"
    params = {
        "page": page
    }
    source = httpx_get(request_url, headers=PC_header, params=params).content
    html_obj = etree.HTML(source)
    return html_obj


def GetUserNextAnniversaryDayHtmlDataApi(user_slug: str) -> _Element:
    request_url = f"https://www.jianshu.com/mobile/u/{user_slug}/anniversary"
    source = httpx_get(request_url, headers=mobile_header).content
    html_obj = etree.HTML(source)
    return html_obj


def GetIslandPostJsonDataApi(post_slug: str) -> List[Dict]:
    request_url = f"https://www.jianshu.com/asimov/posts/{post_slug}"
    source = httpx_get(request_url, headers=api_request_header).content
    json_obj = json_loads(source)
    return json_obj


def GetUserTimelineHtmlDataApi(uslug: str, max_id: int) -> _Element:
    request_url = f"https://www.jianshu.com/users/{uslug}/timeline"
    params = {
        "max_id": max_id
    }
    source = httpx_get(request_url, headers=PC_header, params=params).content
    html_obj = etree.HTML(source)
    return html_obj
