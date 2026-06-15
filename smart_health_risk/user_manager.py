"""
user_manager.py
Handles user registration, login, and JSON-based history storage.
Uses only Python standard library: json, os, datetime.
"""

import json
import os
from datetime import datetime

DATA_FILE = "users.json"


# ─────────────────────────────────────────────────────────────
#  Internal helpers
# ─────────────────────────────────────────────────────────────

def _load() -> dict:
    """Load the JSON data file; return empty dict if it doesn't exist."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}


def _save(data: dict) -> None:
    """Persist the data dict to disk as formatted JSON."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


# ─────────────────────────────────────────────────────────────
#  Public API
# ─────────────────────────────────────────────────────────────

def register_user(username: str) -> bool:
    """
    Register a new user.
    Returns True on success, False if the username already exists.
    """
    data = _load()
    if username in data:
        return False
    data[username] = {"created": datetime.now().strftime("%Y-%m-%d"), "history": []}
    _save(data)
    return True


def user_exists(username: str) -> bool:
    """Return True if the username is already registered."""
    return username in _load()


def save_result(username: str, params: dict, scores: dict) -> None:
    """Append one health-check result to the user's history."""
    data = _load()
    if username not in data:
        return  # silently ignore unknown users

    entry = {
        "date":   datetime.now().strftime("%Y-%m-%d %H:%M"),
        "params": params,
        "scores": scores,
    }
    data[username]["history"].append(entry)
    _save(data)


def get_history(username: str) -> list:
    """Return the user's full history list (may be empty)."""
    data = _load()
    return data.get(username, {}).get("history", [])


def delete_user(username: str) -> bool:
    """
    Remove a user and all their data.
    Returns True if deleted, False if not found.
    """
    data = _load()
    if username not in data:
        return False
    del data[username]
    _save(data)
    return True


def list_users() -> list:
    """Return a sorted list of all registered usernames."""
    return sorted(_load().keys())
