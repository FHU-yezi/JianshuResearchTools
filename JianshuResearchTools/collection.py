import json
import re

import requests
from lxml import etree

from assert_funcs import AssertCollectionUrl
from basic import PC_header, jianshu_request_header
from datetime import datetime
from convert import CollectionUrlToCollectionSlug


def GetCollectionName(collection_url: str) -> str:
    """该函数接收专题 Url，并返回该链接对应专题的名称

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 链接对应专题的名称
    """
    AssertCollectionUrl(collection_url)
    source = requests.get(collection_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//a[@class='name']")[0].text
    print(result)
    return result

def GetCollectionIntroduction(collection_url: str) -> str:
    """该函数接收专题 Url，并返回该链接对应专题的简介

    Args:
        collection_url (str): 专题 Url

    Returns:
        str: 链接对应专题的简介
    """
    AssertCollectionUrl(collection_url)
    source = requests.get(collection_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='description js-description']/p/text()")
    result = "".join(result)
    return result

def GetCollectionArticlesCount(collection_url: str) -> int:
    """该函数接收专题 Url，并返回该链接对应专题的收录文章数量

    Args:
        collection_url (str): 专题 Url

    Returns:
        int: 链接对应专题的收录文章数量
    """
    AssertCollectionUrl(collection_url)
    source = requests.get(collection_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']")[0].text
    result = re.findall(r"\d+", result)[0]
    return result

def GetCollectionFansCount(collection_url: str) -> int:
    """该函数接收专题 Url，并返回该链接对应专题的关注者数量

    Args:
        collection_url (str): 专题 Url

    Returns:
        int: 链接对应专题的关注者数量
    """
    AssertCollectionUrl(collection_url)
    source = requests.get(collection_url, headers=PC_header).content
    html_obj = etree.HTML(source)
    result = html_obj.xpath("//div[@class='info']")[0].text
    result = re.findall(r"\d+", result)[1]
    return result

def GetCollectionEditorsInfo(collection_id: int, page: int =1) -> list:
    """该函数接收专题 ID，并返回 ID 对应专题的编辑信息

    Args:
        collection_id (int): 专题 ID
        page (int, optional): 页码. Defaults to 1.

    Returns:
        list: ID 对应专题的编辑信息
    """
    request_url = "https://www.jianshu.com/collections/" + str(collection_id) + "/editors"
    params = {
        "page": page
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["editors"]:
        item_info = {
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar_source"]
        }
        result.append(item_info)
    return result

def GetCollectionRecommendedWritersInfo(collection_id: int, page: int =1, count: int =20) -> list:
    """该函数接收一个专题 ID，并返回该 ID 对应专题的推荐作者信息

    Args:
        collection_id (int): 专题 ID
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的数量. Defaults to 20.

    Returns:
        list: 推荐作者信息
    """
    params = {
        "collection_ids": collection_id, 
        "page": page, 
        "count": count
    }
    source = requests.get("https://www.jianshu.com/collections/recommended_users", 
                            params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj["users"]:
        item_info = {
            "uid": item["id"], 
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar_source"], 
            "collection_name": item["collection_name"], 
            "likes_count": item["total_likes_count"], 
            "words_count": item["total_wordage"]
        }
        result.append(item_info)
    return result

def GetCollectionFansInfo(collection_id: int, start_sort_id: int) -> list:
    """该函数接收一个专题 ID，并返回该 ID 对应专题的关注者信息

    Args:
        collection_id (int): 专题 ID
        start_sort_id (int): 起始序号，等于上一条数据的序号

    Returns:
        list: 关注者信息
    """
    request_url = "https://www.jianshu.com/collection/" + str(collection_id) + "/subscribers"
    params = {
        "max_sort_id": start_sort_id
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj:
        item_info = {
            "uslug": item["slug"], 
            "name": item["nickname"], 
            "avatar": item["avatar_source"], 
            "sort_id": item["like_id"], 
            "subscribe_time": datetime.fromisoformat(item["subscribed_at"])
        }
        result.append(item_info)
    return result

def GetCollectionArticlesInfo(collection_url: str, page: int =1, 
                                count: int =10, sorting_method: str ="time") -> list:
    """该函数接收专题 Url ，并返回该 Url 对应专题的文章信息

    Args:
        collection_url (str): 专题 Url
        page (int, optional): 页码. Defaults to 1.
        count (int, optional): 每次返回的数据数量. Defaults to 10.
        sorting_method (str, optional): 排序方法，time 为按照发布时间排序，
        comment_time 为按照最近评论时间排序，hot 为按照热度排序. Defaults to "time".

    Returns:
        list: 文章信息
    """
    AssertCollectionUrl(collection_url)
    request_url = "https://www.jianshu.com/asimov/collections/slug/" + \
        CollectionUrlToCollectionSlug(collection_url) + "/public_notes"
    params = {
        "page": page, 
        "count": count, 
        "order_by": {
            "time": "added_at", 
            "comment_time": "commented_at", 
            "hot": "top"  # 是不是太直白了点
        }[sorting_method]
    }
    source = requests.get(request_url, params=params, headers=jianshu_request_header).content
    json_obj = json.loads(source)
    result = []
    for item in json_obj:
        item_info  = {
            "aid": item["object"]["data"]["id"], 
            "title": item["object"]["data"]["title"], 
            "aslug": item["object"]["data"]["slug"], 
            "release_time": datetime.fromisoformat(item["object"]["data"]["first_shared_at"]), 
            "image_url": item["object"]["data"]["list_image_url"],   # TODO: 名字不太贴切
            "summary": item["object"]["data"]["public_abbr"], 
            "views_count": item["object"]["data"]["views_count"], 
            "likes_count": item["object"]["data"]["likes_count"], 
            "paid": item["object"]["data"]["paid"], 
            "commentable": item["object"]["data"]["commentable"], 
            "user": {
                "uid": item["object"]["data"]["user"]["id"], 
                "name": item["object"]["data"]["user"]["nickname"], 
                "uslug": item["object"]["data"]["user"]["slug"], 
                "avatar": item["object"]["data"]["user"]["avatar"]
            }, 
            "total_fp_amount": item["object"]["data"]["total_fp_amount"] / 1000, 
            "comments_count": item["object"]["data"]["public_comments_count"], 
            "rewards_count": item["object"]["data"]["total_rewards_count"]
        }
        result.append(item_info)
    return result