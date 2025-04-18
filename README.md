# LimeAI MCP Server (Python)

### 环境要求
 - Python 3.10 或更高版本。

## 1. 设置环境
首先，我们来安装`uv`：

  MacOS/Linux
  ```bash MacOS/Linux
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```
 Windows
  ```powershell Windows
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

## 2. 获取 LimeAI MCP Server

  ```bash
  # LimeAI Mcp Server 官方开源仓库下载
  git@github.com:liuwenlonghub/limeai-mcp-server.git
  cd limeai-mcp-server

  # 创建虚拟环境并激活
  uv venv
  source .venv/bin/activate

  # 安装依赖
  uv add "mcp[cli]" httpx

  ```

#### 获取 `LIMEAI_ACCESS_TOKEN`
 - 登录 LimeAI（www.limeai.net） > 个人资料 > 访问令牌


## 3. 在Cursor中使用

打开`Cursor`配置（其它客户端类似），在MCP中添加MCP Server

在配置文件中添加如下内容后保存

```json
{
  "mcpServers": {
      "limeai-mcp-server": {
        "command": "uv",
        "args": [
          "--directory",
          "{YOUR_PATH}/limeai-mcp-server/",
          "run",
          "main.py"
        ],
        "env": {
        "LIMEAI_ACCESS_TOKEN": "<USER_LIMEAI_ACCESS_TOKEN>"
        }
      }
    }
}

```

回到配置，此时 LimeAI MCP Server已经启用
