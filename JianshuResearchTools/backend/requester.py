from typing import Dict, Literal, Union

from httpx import (AsyncClient, Client, ConnectError, ConnectTimeout,
                   HTTPStatusError, UnsupportedProtocol)
from lxml import etree
from lxml.etree import _Element
from ujson import loads as usjon_loads

from .exceptions import NetWorkError, ParseError
from .settings import ENABLE_HTTP2, FOLLOW_REDIRECTS, TIMEOUT_SECONDS

_sync_client = Client(
    http2=ENABLE_HTTP2,
    follow_redirects=FOLLOW_REDIRECTS,
    timeout=TIMEOUT_SECONDS
)
_async_client = AsyncClient(
    http2=ENABLE_HTTP2,
    follow_redirects=FOLLOW_REDIRECTS,
    timeout=TIMEOUT_SECONDS
)


def SyncGet(url: str, *, params: Dict = None, headers: Dict = None,
            return_type: Literal["html", "json"]) -> Union[_Element, Dict]:
    """以同步方式发送 Get 请求

    Args:
        url (str): 目标 URL
        return_type (Literal["html", "json"]): 返回数据类型
        params (Dict, optional): 请求参数. Defaults to None.
        headers (Dict, optional): 请求头. Defaults to None.

    Raises:
        NetWorkError: httpx.ConnectError
        NetWorkError: httpx.UnsupportedProtocol
        NetWorkError: httpx.ConnectTimeout
        NetWorkError: httpx.HTTPStatusError
        ParseError: etree 库中的错误
        ParseError: ujson 库中的错误

    Returns:
        Union[_Element, Dict]: 返回数据
    """
    try:
        response = _sync_client.get(
            url,
            params=params,
            headers=headers,
        )
    except ConnectError:
        raise NetWorkError("来自 httpx 库的异常：ConnectError。"
                           "请检查网络状态和代理设置")
    except UnsupportedProtocol:
        raise NetWorkError("来自 httpx 库的异常：UnsupportedProtocol。"
                           "也许你忘了在链接前加上 https://？")
    except ConnectTimeout:
        raise NetWorkError("来自 httpx 库的异常：ConnectTimeout。"
                           "请检查网络状态和延时设置")

    try:
        response.raise_for_status()
    except HTTPStatusError:
        raise NetWorkError("来自 httpx 库的异常：HTTPStatusError。"
                           "可能是服务器问题，请稍后重试")

    if return_type == "html":
        try:
            return etree.HTML(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 lxml 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")
    elif return_type == "json":
        try:
            return usjon_loads(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 ujson 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")


def SyncPost(url: str, *, body: Dict = None, headers: Dict = None,
             return_type: Literal["html", "json"]) -> Union[_Element, Dict]:
    """以同步方式发送 Post 请求

    Args:
        url (str): 目标 URL
        return_type (Literal["html", "json"]): 返回数据类型
        data (Dict, optional): 请求体. Defaults to None.
        headers (Dict, optional): 请求头. Defaults to None.

    Raises:
        NetWorkError: httpx.ConnectError
        NetWorkError: httpx.UnsupportedProtocol
        NetWorkError: httpx.ConnectTimeout
        NetWorkError: httpx.HTTPStatusError
        ParseError: etree 库中的错误
        ParseError: ujson 库中的错误

    Returns:
        Union[_Element, Dict]: 返回数据
    """
    try:
        response = _sync_client.post(
            url,
            json=body,
            headers=headers,
        )
    except ConnectError:
        raise NetWorkError("来自 httpx 库的异常：ConnectError。"
                           "请检查网络状态和代理设置")
    except UnsupportedProtocol:
        raise NetWorkError("来自 httpx 库的异常：UnsupportedProtocol。"
                           "也许你忘了在链接前加上 https://？")
    except ConnectTimeout:
        raise NetWorkError("来自 httpx 库的异常：ConnectTimeout。"
                           "请检查网络状态和延时设置")

    try:
        response.raise_for_status()
    except HTTPStatusError:
        raise NetWorkError("来自 httpx 库的异常：HTTPStatusError。"
                           "可能是服务器问题，请稍后重试")

    if return_type == "html":
        try:
            return etree.HTML(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 lxml 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")
    elif return_type == "json":
        try:
            return usjon_loads(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 ujson 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")


async def AsyncGet(url: str, *, params: Dict = None, headers: Dict = None,
                   return_type: Literal["html", "json"]) \
        -> Union[_Element, Dict]:
    """以同步方式发送 Get 请求

    Args:
        url (str): 目标 URL
        return_type (Literal["html", "json"]): 返回数据类型
        params (Dict, optional): 请求参数. Defaults to None.
        headers (Dict, optional): 请求头. Defaults to None.

    Raises:
        NetWorkError: httpx.ConnectError
        NetWorkError: httpx.UnsupportedProtocol
        NetWorkError: httpx.ConnectTimeout
        NetWorkError: httpx.HTTPStatusError
        ParseError: etree 库中的错误
        ParseError: ujson 库中的错误

    Returns:
        Union[_Element, Dict]: 返回数据
    """
    try:
        response = await _async_client.get(
            url,
            params=params,
            headers=headers,
        )
    except ConnectError:
        raise NetWorkError("来自 httpx 库的异常：ConnectError。"
                           "请检查网络状态和代理设置")
    except UnsupportedProtocol:
        raise NetWorkError("来自 httpx 库的异常：UnsupportedProtocol。"
                           "也许你忘了在链接前加上 https://？")
    except ConnectTimeout:
        raise NetWorkError("来自 httpx 库的异常：ConnectTimeout。"
                           "请检查网络状态和延时设置")

    try:
        response.raise_for_status()
    except HTTPStatusError:
        raise NetWorkError("来自 httpx 库的异常：HTTPStatusError。"
                           "可能是服务器问题，请稍后重试")

    if return_type == "html":
        try:
            return etree.HTML(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 lxml 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")
    elif return_type == "json":
        try:
            return usjon_loads(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 ujson 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")


async def AsyncPost(url: str, *, body: Dict = None, headers: Dict = None,
                    return_type: Literal["html", "json"]) \
        -> Union[_Element, Dict]:
    """以异步方式发送 Post 请求

    Args:
        url (str): 目标 URL
        return_type (Literal["html", "json"]): 返回数据类型
        data (Dict, optional): 请求体. Defaults to None.
        headers (Dict, optional): 请求头. Defaults to None.

    Raises:
        NetWorkError: httpx.ConnectError
        NetWorkError: httpx.UnsupportedProtocol
        NetWorkError: httpx.ConnectTimeout
        NetWorkError: httpx.HTTPStatusError
        ParseError: etree 库中的错误
        ParseError: ujson 库中的错误

    Returns:
        Union[_Element, Dict]: 返回数据
    """
    try:
        response = await _async_client.post(
            url,
            json=body,
            headers=headers,
        )
    except ConnectError:
        raise NetWorkError("来自 httpx 库的异常：ConnectError。"
                           "请检查网络状态和代理设置")
    except UnsupportedProtocol:
        raise NetWorkError("来自 httpx 库的异常：UnsupportedProtocol。"
                           "也许你忘了在链接前加上 https://？")
    except ConnectTimeout:
        raise NetWorkError("来自 httpx 库的异常：ConnectTimeout。"
                           "请检查网络状态和延时设置")

    try:
        response.raise_for_status()
    except HTTPStatusError:
        raise NetWorkError("来自 httpx 库的异常：HTTPStatusError。"
                           "可能是服务器问题，请稍后重试")

    if return_type == "html":
        try:
            return etree.HTML(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 lxml 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")
    elif return_type == "json":
        try:
            return usjon_loads(response.content)
        except Exception as e:  # TODO: 明确捕获异常
            raise ParseError(f"来自 ujson 库的异常：{e}"
                             "这可能是 JRT 的问题，请前往 GitHub 反馈")
