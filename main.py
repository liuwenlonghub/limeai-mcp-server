import os
import httpx
import random
import string
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 常量
LIMEAI_API_BASE = "https://web.limeai.net/api"
LIMEAI_ACCESS_TOKEN = os.getenv('LIMEAI_ACCESS_TOKEN')

# 初始化 FastMCP 服务器
mcp = FastMCP("LimeAI-MCP-Server")

# 生成随机字符串
def generate_string(length=8):
    chars = string.ascii_letters + string.digits  # 包含字母和数字
    return ''.join(random.choices(chars, k=length))


@mcp.tool(name="get_user_info", description="获取当前用户信息")
async def get_user_info() -> Any:
    """
    获取当前用户信息
    """
    try:
        # 从环境变量获取访问令牌   
        if not LIMEAI_ACCESS_TOKEN:
            raise Exception("环境变量中没有 LIMEAI_ACCESS_TOKEN")
 
        # 构建 API URL 
        url = f"{LIMEAI_API_BASE}/mcp/user/userinfo"
        
        # 设置请求头
        headers = {
            "Access-Token": LIMEAI_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }
 
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers)
            response.raise_for_status()
            result = response.json()
 
        if result.get("status") != "success":
            error_msg = result.get("message", "unknown error")
            raise Exception(f"API 响应错误: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP 请求失败: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"解析响应失败: {str(e)}") from e
 

@mcp.tool(name="save_markdown", description="保存文本内容（markdown格式）到 LimeAI")
async def save_markdown(
    text_content: str,
    file_name: str = None,
) -> Any:
    """
    保存文本内容（markdown格式）到 LimeAI
    :param text_content: 对话内容
    :param file_name: 文件名 非必填
    :return: API response

    """
    try:
        # 从环境变量获取访问令牌   
        if not LIMEAI_ACCESS_TOKEN:
            raise Exception("环境变量中没有 LIMEAI_ACCESS_TOKEN")
 
        # 构建 API URL 
        url = f"{LIMEAI_API_BASE}/mcp/resource/create-document"
        
        # 设置请求头
        headers = {
            "Access-Token": LIMEAI_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        # 处理文件名
        if file_name:
            # 检查文件名是否已包含 .md 后缀
            if not file_name.lower().endswith('.md'):
                file_name = f"{file_name}.md"
        else:
            # 如果没有提供文件名，生成一个随机文件名
            file_name = f"mcp_{generate_string()}.md"

        # 设置请求数据
        payload = {
            "content": text_content,
            "file_name": file_name,
            "content_type": "text/markdown",
            "type": "markdown",
            "file_extension": ".md",
        }

        # 向 API 发送请求
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
 
        if result.get("status") != "success":
            error_msg = result.get("message", "unknown error")
            raise Exception(f"API 响应错误: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP 请求失败: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"解析响应失败: {str(e)}") from e
    

@mcp.tool(name="save_html", description="保存 html 代码到 LimeAI")
async def save_html(
    html_content: str,
    file_name: str = None,
) -> Any:
    """
    保存 html 代码到 LimeAI
    :param html_content: 对话内容
    :return: API response

    """
    try:
        # 从环境变量获取访问令牌   
        if not LIMEAI_ACCESS_TOKEN:
            raise Exception("环境变量中没有 LIMEAI_ACCESS_TOKEN")
 
        #
        # 构建 API URL 
        url = f"{LIMEAI_API_BASE}/mcp/resource/create-document"
        
        # 设置请求头
        headers = {
            "Access-Token": LIMEAI_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        # 处理文件名
        if file_name:
            # 检查文件名是否已包含 .html 后缀
            if not file_name.lower().endswith('.html'):
                file_name = f"{file_name}.html"
        else:
            # 如果没有提供文件名，生成一个随机文件名
            file_name = f"mcp_{generate_string()}.html"

        # 设置请求数据
        payload = {
            "content": html_content,
            "file_name": file_name,
            "content_type": "text/html",
            "type": "html",
            "file_extension": ".html",
        }

        # 向 API 发送请求
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
 
        if result.get("status") != "success":
            error_msg = result.get("message", "unknown error")
            raise Exception(f"API 响应错误: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP 请求失败: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"解析响应失败: {str(e)}") from e
   

if __name__ == "__main__":
    # 初始化并运行服务器
    mcp.run()