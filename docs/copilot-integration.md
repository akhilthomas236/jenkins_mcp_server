# Jenkins MCP Server - Copilot Integration Guide

If your Jenkins MCP server isn't showing up in the GitHub Copilot tools list, follow these steps:

## 1. Make sure you have the right extensions installed

- GitHub Copilot (latest version)
- GitHub Copilot Chat (latest version)

## 2. Check your VS Code settings

Your VS Code `settings.json` should have this exact format:

```json
{
    "mcp": {
        "servers": {
            "jenkins-mcp-server": {
                "type": "stdio",
                "command": "uvx",
                "args": ["jenkins-mcp-server==0.1.5"]
            }
        }
    },
    
    "jenkins-mcp-server.jenkins": {
        "url": "http://localhost:8080",
        "username": "admin",
        "password": "password"
    },
    
    "github.copilot.advanced": {
        "mcp.enabled": true
    }
}
```

## 3. Restart VS Code

After updating your settings, completely restart VS Code:
1. Close VS Code completely
2. Wait a few seconds
3. Start VS Code again

## 4. Test that the MCP Server works

Run this command in a terminal:

```bash
uvx jenkins-mcp-server --verbose
```

You should see output related to connecting to your Jenkins server.

## 5. Try using Copilot Chat

In Copilot Chat, try asking:
- "What Jenkins tools do you have access to?"
- "List my Jenkins jobs"

## 6. Check for errors

If you're still having issues:
1. Open VS Code Developer Tools (Help → Toggle Developer Tools)
2. Look for any errors related to MCP or Copilot

## 7. Verify the server is registered correctly

The MCP protocol requires that the server responds to certain initialization methods. Try running:

```bash
# If installed with uvx
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"capabilities":{}}}' | uvx jenkins-mcp-server

# If installed as a package
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"capabilities":{}}}' | jenkins-mcp-server
```

You should see a response with server capabilities.

## Additional Troubleshooting

If you're still having issues, try:

1. Check if the `uvx` command works directly:
   ```bash
   which uvx
   uvx --version
   ```

2. Try installing the MCP server globally:
   ```bash
   # Install from PyPI (recommended)
   pip install uv
   uvx install jenkins-mcp-server==0.1.5
   
   # Or if working with a local clone
   cd /path/to/jenkins-mcp-server
   uvx install -e .
   ```

3. Update your copilot settings to use the global install:
   ```json
   "mcp": {
       "servers": {
           "jenkins-mcp-server": {
               "type": "stdio",
               "command": "uvx",
               "args": ["jenkins-mcp-server"]
           }
       }
   }
   ```
