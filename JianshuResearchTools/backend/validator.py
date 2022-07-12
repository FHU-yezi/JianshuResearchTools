from re import compile as re_compile
from typing import Any, Dict, Pattern

_VERIFICATION: Dict[str, Pattern[str]] = {
    "jianshu_url": re_compile(r"^https://www\.jianshu\.com/"
                              r"\w{1,2}/\w{6,16}/?$"),
    "user_url": re_compile(r"^https://www\.jianshu\.com/u/\w{6,12}/?$"),
    "article_url": re_compile(r"^https://www\.jianshu\.com/p/\w{12}/?$"),
    "notebook_url": re_compile(r"^https://www\.jianshu\.com/nb/\d{7,8}/?$"),
    "collection_url": re_compile(r"^https://www\.jianshu\.com/c/\w{6,12}/?$"),
    "island_url": re_compile(r"^https://www\.jianshu\.com/g/\w{16}/?$"),
    "island_post_url": re_compile(r"^https://www\.jianshu\.com/gp/\w{16}/?$")
}


def IsTargetType(obj: Any, target: Any) -> bool:
    """判断 obj 是否是 target 类型

    Args:
        obj (Any): 待判断对象
        target (Any): 目标类型

    Returns:
        bool: 类型是否正确
    """
    if isinstance(obj, target):
        return True
    return False


def IsJianshuURL(string: str) -> bool:
    """判断是否是简书 URL

    # ! 并非所有以 https://www.jianshu.com/ 开头的都是简书 URL
    # ! 本库中的“简书 URL”指所有简书资源 URL 的并集

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["jianshu_url"].fullmatch(string))


def IsUserURL(string: str) -> bool:
    """判断是否是用户 URL

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["user_url"].fullmatch(string))


def IsArticleURL(string: str) -> bool:
    """判断是否是文章 URL

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["article_url"].fullmatch(string))


def IsNotebookURL(string: str) -> bool:
    """判断是否是文集 URL

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["notebook_url"].fullmatch(string))


def IsCollectionURL(string: str) -> bool:
    """判断是否是文集 URL

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["collection_url"].fullmatch(string))


def IsIslandURL(string: str) -> bool:
    """判断是否是小岛 URL

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["island_url"].fullmatch(string))


def IsIslandPostURL(string: str) -> bool:
    """判断是否是小岛帖子 URL

    Args:
        string (str): 待判断的字符串

    Returns:
        bool: 判断结果
    """
    return bool(_VERIFICATION["island_post_url"].fullmatch(string))
