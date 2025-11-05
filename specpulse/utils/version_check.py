"""
Version checking utility for SpecPulse
"""

import json
import urllib.request
import urllib.error
from typing import Optional, Tuple
from packaging import version
import socket


def check_pypi_version(package_name: str = "specpulse", timeout: int = 2) -> Optional[str]:
    """
    Check the latest version of a package on PyPI

    Args:
        package_name: Name of the package to check
        timeout: Timeout in seconds for the request

    Returns:
        Latest version string or None if check fails
    """
    try:
        # Set a short timeout to avoid blocking
        socket.setdefaulttimeout(timeout)

        url = f"https://pypi.org/pypi/{package_name}/json"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())
            return data["info"]["version"]
    except (urllib.error.URLError, urllib.error.HTTPError, json.JSONDecodeError, KeyError, socket.timeout):
        # Silently fail - don't interrupt user workflow
        return None
    finally:
        # Reset default timeout
        socket.setdefaulttimeout(None)


def compare_versions(current: str, latest: str) -> Tuple[bool, bool]:
    """
    Compare current version with latest version

    Args:
        current: Current installed version
        latest: Latest available version

    Returns:
        Tuple of (is_outdated, is_major_update)
    """
    try:
        current_v = version.parse(current)
        latest_v = version.parse(latest)

        is_outdated = current_v < latest_v

        # Check if it's a major version update
        is_major = False
        if is_outdated:
            # Major version changed
            if latest_v.major > current_v.major:
                is_major = True

        return is_outdated, is_major
    except:
        return False, False


def get_update_message(current: str, latest: str, is_major: bool) -> Tuple[str, str]:
    """
    Generate update notification message

    Args:
        current: Current version
        latest: Latest version
        is_major: Whether this is a major update

    Returns:
        Tuple of (formatted update message, color string)
    """
    # Determine update type
    curr_parts = current.split('.')
    latest_parts = latest.split('.')

    update_type = "patch"
    if len(curr_parts) >= 2 and len(latest_parts) >= 2:
        if curr_parts[0] != latest_parts[0]:
            update_type = "major"
        elif curr_parts[1] != latest_parts[1]:
            update_type = "minor"
        else:
            update_type = "patch"

    if is_major:
        urgency = f"[!] MAJOR ({update_type} update)"
        color = "bright_red"
    else:
        urgency = f"[i] {update_type.upper()}"
        color = "yellow"

    message = f"""
{urgency} Update Available!
Current: v{current}
Latest:  v{latest}

Update with: pip install --upgrade specpulse
"""

    return message, color


def should_check_version() -> bool:
    """
    Determine if we should check for updates

    Returns:
        True if we should check, False otherwise
    """
    import os
    from pathlib import Path
    from datetime import datetime, timedelta

    try:
        # Check once per day maximum
        cache_file = Path.home() / ".specpulse" / "last_version_check"

        if cache_file.exists():
            # Check if last check was within 24 hours
            last_check = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - last_check < timedelta(hours=24):
                return False

        # Create cache directory if needed
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        # Update timestamp
        cache_file.touch()
        return True
    except:
        # If anything fails, don't check
        return False