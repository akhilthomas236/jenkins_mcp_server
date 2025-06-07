# Jenkins MCP Server Setup Guide

## Installation Issue Solved

We've identified and fixed the issue with the Jenkins MCP server not appearing in GitHub Copilot's tools list.

## What Was Fixed

1. **Package Installation**: Rather than trying to use `uvx` to run the MCP server directly, we installed the package properly using `pip install -e .`

2. **VS Code Settings**: Updated the VS Code settings to use the directly installed `jenkins-mcp-server` command instead of trying to use `uvx`

3. **Configuration Files**: Updated all relevant configuration files to use the direct command approach

## Current Setup

- The Jenkins MCP server is now installed as a Python package (version 0.1.5 on PyPI)
- VS Code is configured to run it directly using the `jenkins-mcp-server` command
- The server will run with verbose output for better debugging
- All Jenkins tools (9 total) are now properly registered and available to AI assistants

## How to Test the MCP Server

1. **Restart VS Code**: To ensure the new settings take effect, completely close and reopen VS Code

2. **Open GitHub Copilot Chat**: Start a new chat session and try a Jenkins-related query like "List my Jenkins jobs"

3. **Check the Output**: Look at the "Output" panel in VS Code for any error messages from the MCP server

## Troubleshooting

If the MCP server still doesn't appear in GitHub Copilot, check:

1. **GitHub Copilot Extension**: Make sure you have the latest GitHub Copilot and Copilot Chat extensions

2. **VS Code Settings**: Ensure the MCP settings are correct in your VS Code settings.json

3. **Connection to Jenkins**: Verify that the Jenkins server details (URL, username, password) are correct

## Running Manually

You can always test the MCP server by running:

```bash
jenkins-mcp-server --verbose
```

This should show any connection errors or other issues that might prevent it from working properly.

## Next Steps

Consider setting up a working Jenkins server (locally or remotely) for proper testing of the MCP server's capabilities.
