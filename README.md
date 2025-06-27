# Jenkins MCP Server

A Python-based Jenkins MCP server using the Model Context Protocol Python SDK. This server integrates with Jenkins CI/CD systems to provide AI-powered insights, build management, and debugging capabilities.

> **Note:** This server follows the [Model Context Protocol (MCP)](https://modelcontextprotocol.io/), enabling AI assistants to interact with Jenkins systems directly.

## Installation

### Option 1: Install as a Python Package (Recommended)

The easiest way to install and run this server is as a Python package:

```bash
# Install from PyPI
pip install jenkins-mcp-server==0.1.5

# Or install with uv
uv pip install jenkins-mcp-server==0.1.5

# Run the server
jenkins-mcp-server --verbose
```

### Option 2: Clone and Run

```bash
# Clone the repository
git clone https://github.com/yourusername/jenkins-mcp-server.git
cd jenkins-mcp-server

# Create a virtual environment and install dependencies
uv venv
uv pip install -e .

# Run the server
python -m jenkins_mcp_server
```

## VS Code Integration

### Configure for VS Code

For quick installation, use one of the one-click install buttons below:

[![Install with UV in VS Code](https://img.shields.io/badge/VS_Code-UV-0098FF?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=jenkins&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22jenkins-mcp-server%3D%3D0.1.5%22%5D%2C%22env%22%3A%7B%22JENKINS_URL%22%3A%22%24%7BPROMPT%3AJENKINS_URL%7D%22%2C%22JENKINS_USERNAME%22%3A%22%24%7BPROMPT%3AJENKINS_USERNAME%7D%22%2C%22JENKINS_TOKEN%22%3A%22%24%7BSECRET%3AJENKINS_TOKEN%7D%22%7D%7D) [![Install with UV in VS Code Insiders](https://img.shields.io/badge/VS_Code_Insiders-UV-24bfa5?style=flat-square&logo=visualstudiocode&logoColor=white)](https://insiders.vscode.dev/redirect/mcp/install?name=jenkins&config=%7B%22command%22%3A%22uvx%22%2C%22args%22%3A%5B%22jenkins-mcp-server%3D%3D0.1.5%22%5D%2C%22env%22%3A%7B%22JENKINS_URL%22%3A%22%24%7BPROMPT%3AJENKINS_URL%7D%22%2C%22JENKINS_USERNAME%22%3A%22%24%7BPROMPT%3AJENKINS_USERNAME%7D%22%2C%22JENKINS_TOKEN%22%3A%22%24%7BSECRET%3AJENKINS_TOKEN%7D%22%7D%7D&quality=insiders)

For manual installation:

1. Install the Model Context Protocol (MCP) extension for VS Code
2. Create a `.vscode/mcp.json` file in your workspace with the following configuration:

```json
{
  "servers": {
    "jenkins-mcp-server": {
      "type": "stdio",
      "command": "jenkins-mcp-server",
      "args": ["--verbose"],
      "env": {
        "JENKINS_URL": "http://your-jenkins-server:8080",
        "JENKINS_USERNAME": "your-username",
        "JENKINS_TOKEN": "your-api-token"
        // Or use JENKINS_PASSWORD instead of JENKINS_TOKEN if using password authentication
      }
    }
  }
}
```

3. Configure your authentication method:
   - **Recommended**: Use API token authentication by setting `JENKINS_TOKEN`
   - Alternatively: Use password authentication by setting `JENKINS_PASSWORD`

4. Connect any AI assistant that supports MCP (like GitHub Copilot) to your Jenkins environment

## Components

### Resources

The server provides access to Jenkins jobs as resources:
- Custom jenkins:// URI scheme for accessing individual jobs
- Each job resource contains details about the job and its builds in JSON format
- Job status is reflected in the resource description

### Prompts

The server provides prompts for Jenkins data analysis:

1. **analyze-job-status**: Creates analysis of all Jenkins jobs
   - Optional "detail_level" argument to control analysis depth (brief/detailed)
   - Analyzes job statuses, identifies potential issues, and suggests improvements

2. **analyze-build-logs**: Analyzes build logs for a specific job
   - Required "job_name" argument to specify which job to analyze
   - Optional "build_number" argument (defaults to latest build)
   - Examines build logs to identify issues, errors, warnings, and suggests fixes

### Tools

The server implements the following tools for Jenkins operations:

1. **trigger-build**: Triggers a Jenkins job build
   - Required "job_name" argument to specify which job to build
   - Optional "parameters" object containing job parameters
   - Returns build queue information

2. **stop-build**: Stops a running Jenkins build
   - Required "job_name" and "build_number" arguments 
   - Halts an in-progress build execution

3. **get-job-details**: Gets detailed information about a specific job
   - Required "job_name" argument
   - Returns comprehensive job information including recent builds
   
4. **list-jobs**: Lists all Jenkins jobs
   - Returns a list of all Jenkins jobs with their statuses

5. **get-build-info**: Gets information about a specific build
   - Required "job_name" and "build_number" arguments
   - Returns build status, duration, and other details

6. **get-build-console**: Gets console output from a build
   - Required "job_name" and "build_number" arguments
   - Returns the console log output from a specific build

7. **get-queue-info**: Gets information about the Jenkins build queue
   - Returns information about pending builds in the queue

8. **get-node-info**: Gets information about a Jenkins node/agent
   - Required "node_name" argument
   - Returns node status and configuration details

9. **list-nodes**: Lists all Jenkins nodes/agents
   - Returns a list of all Jenkins nodes/agents and their statuses

## Configuration

### Option 1: VS Code Settings (Recommended)

Configure your Jenkins connection in VS Code settings:

1. Open VS Code Settings (Press `Cmd+,` on Mac or `Ctrl+,` on Windows/Linux)
2. Click on the "Open Settings (JSON)" button in the top right
3. Add these settings:

<details>
<summary>Using the User Settings (JSON)</summary>

```json
{
  "mcp.servers": {
    "jenkins": {
      "type": "stdio",
      "command": "uvx",
      "args": ["jenkins-mcp-server"]
    }
  },
  "jenkins-mcp-server.jenkins": {
    "url": "http://your-jenkins-server:8080",
    "username": "your-username",
    "token": "********"  // Replace with your Jenkins API token
  }
}
```
</details>

<details>
<summary>Using workspace .vscode/mcp.json file</summary>

Create a file at `.vscode/mcp.json` with these contents:

```json
{ 
  "servers": { 
    "jenkins-mcp-server": { 
      "type": "stdio", 
      "command": "jenkins-mcp-server", 
      "args": [
        "--verbose"
      ]
    }
  }
}
```

And in your `.vscode/settings.json` file:

```json
{
  "jenkins-mcp-server.jenkins": {
    "url": "http://your-jenkins-server:8080",
    "username": "your-username",
    "token": "********"  // Replace with your Jenkins API token
  }
}
```
</details>

This configuration:
- Registers the MCP server in VS Code
- Stores your Jenkins credentials securely in VS Code settings
- Uses `uvx` to run the server automatically when needed

### Option 2: Environment Variables

Alternatively, configure your Jenkins connection by setting environment variables:

1. Copy the `.env.example` file to create a `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file with your Jenkins details:
   ```
   JENKINS_URL=http://your-jenkins-server:8080
   JENKINS_USERNAME=your-username
   JENKINS_PASSWORD=your-password
   # OR use an API token instead of password (recommended)
   JENKINS_TOKEN=your-api-token
   ```

> **Security Note:** Using VS Code settings is more secure as they are stored encrypted. Environment variables in a `.env` file are stored in plain text.

## Usage with AI Assistants

Once configured, AI assistants that support MCP can now interact with your Jenkins server through natural language. Here are some examples of what you can do:

### GitHub Copilot Chat

1. Open GitHub Copilot Chat in VS Code
2. Type prompts like:
   - "List all my Jenkins jobs"
   - "What's the status of my 'deployment' job?"
   - "Show me the build logs for the failed build in 'test-project'"
   - "Trigger a new build for 'deploy-api'"

### Command Line Usage

You can also run the server directly from the command line:

```bash
# Run the MCP server
uvx jenkins-mcp-server

# In another terminal, use curl to test it:
curl -X POST http://localhost:8080/mcp/v1/listResources -H "Content-Type: application/json" -d '{}'
```

## Command-Line Usage

The `uvx` command makes it easy to use the MCP server in command-line environments without VS Code:

```bash
# Install UVX if you don't have it yet
pip install uv

# Install the Jenkins MCP server
uvx install jenkins-mcp-server

```bash
# Install UVX if you don't have it yet
pip install uv

# Install the Jenkins MCP server from PyPI
uvx install jenkins-mcp-server==0.1.5

# Run the server with verbose output
uvx jenkins-mcp-server --verbose
```

### Testing from Command Line

You can manually send JSON-RPC requests:

```bash
echo '{"jsonrpc":"2.0","id":1,"method":"listResources","params":{}}' | uvx jenkins-mcp-server
```

## Development Setup

If you're developing this MCP server:

1. Clone this repository
2. Install dependencies:
   ```bash
   uv venv
   uv pip install -e ".[dev]"
   ```
3. Run the server in development mode:
   ```bash
   python -m jenkins_mcp_server --verbose
   ```

### VS Code Configuration for Development

For development in VS Code:

```json
"mcp": {
  "servers": {
    "jenkins-mcp-server": {
      "type": "stdio",
      "command": "bash",
      "args": [
        "-c", 
        "cd ${workspaceFolder} && python -m jenkins_mcp_server --verbose"
      ]
    }
  }
}
```

3. Install the GitHub Copilot Chat extension
4. Enable MCP in Copilot settings
5. Start a new chat with Copilot and interact with your Jenkins server!

#### 3. Claude Desktop

For Claude Desktop users:

On MacOS: `~/Library/Application\ Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%/Claude/claude_desktop_config.json`

<details>
  <summary>Development Configuration</summary>
  
  ```json
  "mcpServers": {
    "jenkins-mcp-server": {
      "command": "uv",
      "args": [
        "run",
        "jenkins-mcp-server"
      ]
    }
  }
  ```
</details>

<details>
  <summary>Published Configuration (using uvx)</summary>
  
  ```json
  "mcpServers": {
    "jenkins-mcp-server": {
      "command": "uvx",
      "args": [
        "jenkins-mcp-server"
      ]
    }
  }
  ```
</details>

## Development

### Building and Publishing

To prepare the package for distribution:

1. Sync dependencies and update lockfile:
```bash
uv sync
```

2. Build package distributions:
```bash
uv build
```

This will create source and wheel distributions in the `dist/` directory.

3. Publish to PyPI:
```bash
uv publish
```

Note: You'll need to set PyPI credentials via environment variables or command flags:
- Token: `--token` or `UV_PUBLISH_TOKEN`
- Or username/password: `--username`/`UV_PUBLISH_USERNAME` and `--password`/`UV_PUBLISH_PASSWORD`

### Debugging

Since MCP servers run over stdio, debugging can be challenging. For the best debugging
experience, we strongly recommend using the [MCP Inspector](https://github.com/modelcontextprotocol/inspector).


You can launch the MCP Inspector via [`npm`](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) with this command:

```bash
# If installed globally with uvx
npx @modelcontextprotocol/inspector uvx jenkins-mcp-server

# If installed in development mode
npx @modelcontextprotocol/inspector python -m jenkins_mcp_server
```


Upon launching, the Inspector will display a URL that you can access in your browser to begin debugging.