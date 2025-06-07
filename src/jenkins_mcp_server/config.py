import os
import json
import re
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List


def parse_jsonc(jsonc_str: str) -> Dict[str, Any]:
    """Parse JSON with comments (JSONC) with extra robust error handling"""
    if not jsonc_str or not jsonc_str.strip():
        print("Warning: Empty JSON string")
        return {}
        
    try:
        # First attempt: try direct loading (fastest)
        try:
            return json.loads(jsonc_str)
        except json.JSONDecodeError:
            # Continue to more complex parsing
            pass
            
        # Remove single-line comments (// ...)
        json_str = re.sub(r'//.*$', '', jsonc_str, flags=re.MULTILINE)
        
        # Remove multi-line comments (/* ... */)
        json_str = re.sub(r'/\*.*?\*/', '', json_str, flags=re.DOTALL)
        
        # Replace any control characters with spaces
        json_str = ''.join(ch if ord(ch) >= 32 else ' ' for ch in json_str)
        
        # Try parsing again
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON after comment removal: {e}")
            
        # Try with more aggressive cleanup
        cleaned_str = re.sub(r'\s+', ' ', json_str).strip()
        
        # Fix common JSON syntax errors
        # Remove trailing commas
        cleaned_str = re.sub(r',\s*}', '}', cleaned_str)
        cleaned_str = re.sub(r',\s*]', ']', cleaned_str)
        
        # Add missing braces if necessary
        if not cleaned_str.startswith('{') and not cleaned_str.startswith('['):
            cleaned_str = '{' + cleaned_str
        if not cleaned_str.endswith('}') and not cleaned_str.endswith(']'):
            if cleaned_str.startswith('{'):
                cleaned_str = cleaned_str + '}'
            elif cleaned_str.startswith('['):
                cleaned_str = cleaned_str + ']'
                
        # Try parsing with very aggressive cleanup
        try:
            return json.loads(cleaned_str)
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON after aggressive cleanup: {e}")
            
        # Last resort: manually extract just the Jenkins settings if present
        try:
            jenkins_pattern = r'"jenkins-mcp-server\.jenkins"\s*:\s*{([^}]+)}'
            match = re.search(jenkins_pattern, json_str)
            if match:
                jenkins_str = '{' + f'"jenkins-mcp-server.jenkins": {{{match.group(1)}}}' + '}'
                return json.loads(jenkins_str)
        except Exception as e:
            print(f"Error extracting Jenkins settings: {e}")
            
        return {}
    except Exception as e:
        print(f"Unexpected error parsing JSON: {e}")
        return {}


def get_vscode_settings() -> Dict[str, Any]:
    """Get VS Code settings for Jenkins MCP server"""
    try:
        # Try to find VS Code settings.json
        home = Path.home()
        print("\nLooking for VS Code settings in:")
        settings_paths: List[Path] = [
            # macOS
            home / "Library/Application Support/Code/User/settings.json",
            home / "Library/Application Support/Code - Insiders/User/settings.json",
            # Linux
            home / ".config/Code/User/settings.json",
            home / ".config/Code - Insiders/User/settings.json",
            # Windows
            home / "AppData/Roaming/Code/User/settings.json",
            home / "AppData/Roaming/Code - Insiders/User/settings.json",
        ]
        
        workspace_settings = Path.cwd() / ".vscode/settings.json"
        if workspace_settings.exists():
            settings_paths.insert(0, workspace_settings)
            print(f"Found workspace settings at: {workspace_settings}")
        
        for path in settings_paths:
            print(f"Checking {path}")
            if path.exists():
                print(f"Found settings at: {path}")
                try:
                    with open(path, 'r') as f:
                        # Use our custom parser for JSONC
                        settings = parse_jsonc(f.read())
                        
                        # Check for traditional jenkins-mcp-server.jenkins path
                        jenkins_settings = settings.get("jenkins-mcp-server", {}).get("jenkins", {})
                        if jenkins_settings:
                            print("Found Jenkins settings in VS Code config at jenkins-mcp-server.jenkins")
                            # Don't print sensitive values
                            safe_settings = jenkins_settings.copy()
                            if 'password' in safe_settings:
                                safe_settings['password'] = '****'
                            if 'token' in safe_settings:
                                safe_settings['token'] = '****'
                            print(f"Settings found: {json.dumps(safe_settings, indent=2)}")
                            return jenkins_settings
                        
                        # Check for MCP server configuration path
                        mcp_settings = settings.get("mcp", {}).get("servers", {}).get("jenkins-mcp-server", {})
                        if mcp_settings and "jenkinsConfig" in mcp_settings:
                            jenkins_settings = mcp_settings["jenkinsConfig"]
                            print("Found Jenkins settings in VS Code config at mcp.servers.jenkins-mcp-server.jenkinsConfig")
                            # Don't print sensitive values
                            safe_settings = jenkins_settings.copy()
                            if 'password' in safe_settings:
                                safe_settings['password'] = '****'
                            if 'token' in safe_settings:
                                safe_settings['token'] = '****'
                            print(f"Settings found: {json.dumps(safe_settings, indent=2)}")
                            return jenkins_settings
                        
                        print("No Jenkins settings found in this file")
                except Exception as e:
                    print(f"Error parsing JSON in {path}: {str(e)}")
                    continue
        
        print("No Jenkins settings found in any VS Code settings file")
        return {}
    except Exception as e:
        print(f"Error reading VS Code settings: {e}")
        return {}


class JenkinsSettings(BaseSettings):
    """Jenkins connection settings."""
    jenkins_url: str = "http://localhost:8080"
    username: Optional[str] = None
    password: Optional[str] = None
    token: Optional[str] = None  # API token can be used instead of password
    
    # Pydantic v2 uses model_config for configuration
    model_config = {
        "env_file_encoding": "utf-8",
        "env_prefix": "JENKINS_",
        "case_sensitive": False,
        "populate_by_name": True,
        "env_file": ".env",  # Default .env file
    }
    
    def __init__(self, custom_env_path: Optional[str] = None, **data):
        """Initialize with optional custom .env file path"""
        if custom_env_path:
            # Create a new model_config with the custom env file
            print(f"Using custom .env file: {custom_env_path}")
            # For Pydantic v2, we need to update the class's model_config
            # We can't modify self.model_config directly as it's a property in v2
            model_config_dict = dict(self.__class__.model_config)
            model_config_dict["env_file"] = custom_env_path
            self.__class__.model_config = model_config_dict
        
        super().__init__(**data)


# Function to load settings from all sources
def load_settings(custom_env_path: Optional[str] = None) -> JenkinsSettings:
    """
    Load Jenkins settings from all possible sources with priority:
    1. VS Code settings
    2. Environment variables (from custom .env if provided)
    3. Default values
    """
    # Try to get settings from VS Code global or workspace settings
    print("\nAttempting to load settings...")
    vscode_settings = get_vscode_settings()
    
    # Create settings instance from environment variables (using custom path if provided)
    print("\nLoading environment variables...")
    jenkins_settings = JenkinsSettings(custom_env_path=custom_env_path)
    
    # Override with VS Code settings if available
    if vscode_settings:
        print("\nOverriding with VS Code settings...")
        if 'url' in vscode_settings:
            print(f"Using URL from VS Code: {vscode_settings['url']}")
            jenkins_settings.jenkins_url = vscode_settings['url']
        if 'username' in vscode_settings:
            print(f"Using username from VS Code: {vscode_settings['username']}")
            jenkins_settings.username = vscode_settings['username']
        if 'token' in vscode_settings:
            print("Using token from VS Code settings")
            jenkins_settings.token = vscode_settings['token']
        if 'password' in vscode_settings:
            print("Using password from VS Code settings")
            jenkins_settings.password = vscode_settings['password']
    
    return jenkins_settings

# Create initial settings instance with default paths
jenkins_settings = load_settings()

# Log final configuration
print(f"\nFinal configuration:")
print(f"Jenkins server configured: {jenkins_settings.jenkins_url}")
if jenkins_settings.username:
    print(f"Using authentication for user: {jenkins_settings.username}")
    if jenkins_settings.token:
        print("Authentication method: API Token")
    elif jenkins_settings.password:
        print("Authentication method: Password")
else:
    print("No authentication configured for Jenkins")
