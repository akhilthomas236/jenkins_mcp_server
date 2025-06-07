from . import server
import asyncio
import argparse
from .config import load_settings

def main():
    """
    Main entry point for the package.
    
    Parses command-line arguments and runs the server.
    """
    parser = argparse.ArgumentParser(description='Jenkins MCP Server')
    
    # Add arguments
    parser.add_argument('--env-file', 
                      help='Path to a custom .env file with Jenkins credentials')
    parser.add_argument('--verbose', action='store_true',
                      help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Reload settings with custom env file if specified
    if args.env_file:
        from . import config
        config.jenkins_settings = load_settings(custom_env_path=args.env_file)
        print(f"Loaded settings from custom .env file: {args.env_file}")
    
    # Run the server
    asyncio.run(server.main())

# Optionally expose other important items at package level
__all__ = ['main', 'server']