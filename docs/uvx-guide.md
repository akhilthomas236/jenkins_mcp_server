# Using UVX with Jenkins MCP Server

This guide explains how to use the `uvx` command to install and run the Jenkins MCP server.

## What is UVX?

`uvx` is a command-line utility that simplifies installation and execution of Python packages directly from Git repositories or local directories, without requiring a virtual environment setup. It's particularly useful for MCP servers that need to be installed globally.

## Installation

### 1. Install the UV package manager

```bash
pip install uv
```

### 2. Install Jenkins MCP Server

```bash
# Install from GitHub repository
uvx install git+https://github.com/yourusername/jenkins-mcp-server.git

# OR install from a local directory
cd /path/to/jenkins-mcp-server
uvx install .
```

## Running the Server

Once installed, you can run the Jenkins MCP server directly with:

```bash
uvx jenkins-mcp-server
```

Optional flags:
- `--verbose` or `-v`: Shows additional connection information
- `--version`: Shows the version of the MCP server

## VS Code Integration

UVX is the recommended method for running the MCP server with VS Code:

```json
"mcp.servers": {
  "jenkins-mcp-server": {
    "type": "stdio",
    "command": "uvx",
    "args": ["jenkins-mcp-server"]
  }
}
```

## Upgrading

To upgrade to a newer version:

```bash
uvx install --upgrade git+https://github.com/yourusername/jenkins-mcp-server.git
```

## Uninstalling

To remove the package:

```bash
uvx uninstall jenkins-mcp-server
```

## Troubleshooting

If you encounter issues:

1. Ensure you have the latest version of `uv`:
   ```bash
   pip install --upgrade uv
   ```

2. Try with verbose output:
   ```bash
   uvx jenkins-mcp-server --verbose
   ```

3. Check your Jenkins server settings in VS Code global settings or `.env` file
