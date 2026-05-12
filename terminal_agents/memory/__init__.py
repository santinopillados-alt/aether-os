"""Memory management system."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path


class MemoryManager:
    """Manages working memory, episodic memory, semantic memory."""

    def __init__(self, db_path: str = ".agents/memory.db"):
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_database()
        self.working_memory = {}
        print(f"✓ Memory initialized at {db_path}")

    def _init_database(self):
        """Initialize SQLite database."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS memory_entries (
                    id TEXT PRIMARY KEY,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    timestamp TEXT NOT NULL
                )
            """)
            conn.commit()

    async def store_entry(self, key: str, value: dict):
        """Store a memory entry."""
        self.working_memory[key] = value
        
    async def retrieve_entry(self, key: str):
        """Retrieve a memory entry."""
        return self.working_memory.get(key)

    def get_stats(self):
        """Get memory statistics."""
        return {
            "working_memory_keys": len(self.working_memory),
            "db_path": str(self.db_path)
        }
