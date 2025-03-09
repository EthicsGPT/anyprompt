#!/usr/bin/env python3
"""
Command line interface for anyprompt.
"""
import argparse
import sys
import logging
import webbrowser
import time
from pathlib import Path
from anyprompt.server import start_server

logger = logging.getLogger('anyprompt')

def main():
    """Main entry point for the CLI."""
    parser = argparse.ArgumentParser(
        description="anyprompt - Monitor and visualize LLM prompts",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '--port', '-p',
        type=int,
        default=2400,
        help='Port to run the server on'
    )
    
    parser.add_argument(
        '--no-open', '-n',
        action='store_true',
        help='Do not automatically open the browser'
    )
    
    parser.add_argument(
        '--clear', '-c',
        action='store_true',
        help='Clear all existing prompts before starting'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help='Show version and exit'
    )
    
    args = parser.parse_args()
    
    # Handle version flag
    if args.version:
        from anyprompt import __version__
        print(f"anyprompt version {__version__}")
        return 0
    
    # Handle clear flag
    if args.clear:
        prompts_file = Path.cwd() / "prompts" / "prompts.json"
        try:
            if prompts_file.exists():
                prompts_file.unlink()  # Delete the file
                logger.info("✓ Cleared all existing prompts")
        except Exception as e:
            logger.error(f"Failed to clear prompts: {e}")
    
    # Ensure the prompts directory exists
    prompts_dir = Path.cwd() / "prompts"
    prompts_dir.mkdir(exist_ok=True)
    
    # Start the server
    server_url = f"http://localhost:{args.port}"
    logger.info(f"✨ Starting anyprompt server at {server_url}")
    
    # Open browser if requested
    if not args.no_open:
        logger.info("🌐 Opening browser...")
        # Open after a short delay to give server time to start
        webbrowser.open(server_url)
    
    # Start server (this will block until Ctrl+C)
    try:
        start_server(args.port)
    except KeyboardInterrupt:
        logger.info("👋 anyprompt server stopped")
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 