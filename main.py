import os
import httpx
import random
import string
from typing import Any
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# load_dotenv()
load_dotenv()

# Constants
LIMEAI_API_BASE = "https://web.limeai.net/api"
LIMEAI_ACCESS_TOKEN = os.getenv('LIMEAI_ACCESS_TOKEN')

# Initialize FastMCP server
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
        # Get the access token from environment variables   
        if not LIMEAI_ACCESS_TOKEN:
            raise Exception("There is no LIMEAI_ACCESS_TOKEN in environment variables")
 
        # Build the API URL 
        url = f"{LIMEAI_API_BASE}/mcp/user/userinfo"
        
        # Set the headers for the request
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
            raise Exception(f"API response error: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e
 

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
        # Get the access token from environment variables   
        if not LIMEAI_ACCESS_TOKEN:
            raise Exception("There is no LIMEAI_ACCESS_TOKEN in environment variables")
 
        # Build the API URL 
        url = f"{LIMEAI_API_BASE}/mcp/resource/create-document"
        
        # Set the headers for the request
        headers = {
            "Access-Token": LIMEAI_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        #  Process file name
        if file_name:
            # Check if the file name already contains the .md suffix
            if not file_name.lower().endswith('.md'):
                file_name = f"{file_name}.md"
        else:
            # If no file name is provided, generate a random file name.
            file_name = f"mcp_{generate_string()}.md"

        # Set the data for the request
        payload = {
            "content": text_content,
            "file_name": file_name,
            "content_type": "text/markdown",
            "type": "markdown",
            "file_extension": ".md",
        }

        # Send the request to the API
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
 
        if result.get("status") != "success":
            error_msg = result.get("message", "unknown error")
            raise Exception(f"API response error: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e
    

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
        # Get the access token from environment variables   
        if not LIMEAI_ACCESS_TOKEN:
            raise Exception("There is no LIMEAI_ACCESS_TOKEN in environment variables")
 
        # Build the API URL 
        url = f"{LIMEAI_API_BASE}/mcp/resource/create-document"
        
        # Set the headers for the request
        headers = {
            "Access-Token": LIMEAI_ACCESS_TOKEN,
            "Content-Type": "application/json"
        }

        #  Process file name
        if file_name:
            # Check if the file name already contains the .html suffix
            if not file_name.lower().endswith('.html'):
                file_name = f"{file_name}.html"
        else:
            # If no file name is provided, generate a random file name.
            file_name = f"mcp_{generate_string()}.html"

        # Set the data for the request
        payload = {
            "content": html_content,
            "file_name": file_name,
            "content_type": "text/html",
            "type": "html",
            "file_extension": ".html",
        }

        # Send the request to the API
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()
 
        if result.get("status") != "success":
            error_msg = result.get("message", "unknown error")
            raise Exception(f"API response error: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse response: {str(e)}") from e
   

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run()
