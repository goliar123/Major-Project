"""
SHA256 Prompt Hashing Cache Engine.
Supports SQLite (local default), Redis, MongoDB, and In-Memory caching.
Prevents duplicate LLM inference calls to maximize free-tier GPU quota efficiency.
"""
import hashlib
import json
import sqlite3
from typing import Optional, Dict, Any, Tuple
from datetime import datetime, timezone
from pathlib import Path
from config.settings import settings
from config.logging_config import logger

class AttributionCache:
    def __init__(self):
        self.backend_type = settings.CACHE_BACKEND
        self.sqlite_path = Path(settings.SQLITE_DB_PATH)
        self.hits = 0
        self.misses = 0
        self._memory_cache: Dict[str, Dict[str, Any]] = {}
        self._init_backend()

    def _init_backend(self):
        """Initializes database tables or connections."""
        try:
            if self.backend_type == "sqlite":
                conn = sqlite3.connect(self.sqlite_path)
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS prompt_cache (
                        prompt_hash TEXT PRIMARY KEY,
                        model_name TEXT,
                        prompt_text TEXT,
                        response_json TEXT,
                        created_at TEXT
                    )
                """)
                conn.commit()
                conn.close()
                logger.info(f"Initialized SQLite Cache at {self.sqlite_path}")
            elif self.backend_type == "mongodb":
                import pymongo
                self.mongo_client = pymongo.MongoClient(settings.MONGODB_URI, serverSelectionTimeoutMS=2000)
                self.mongo_client.server_info()
                self.mongo_db = self.mongo_client[settings.MONGODB_DB_NAME]
                self.mongo_collection = self.mongo_db["prompt_cache"]
                self.mongo_collection.create_index("prompt_hash", unique=True)
                logger.info("Connected to MongoDB Cache successfully.")
            elif self.backend_type == "redis":
                import redis
                self.redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses=True, socket_timeout=2)
                self.redis_client.ping()
                logger.info("Connected to Redis Cache successfully.")
        except Exception as e:
            logger.warning(f"Could not connect to {self.backend_type} cache ({e}). Falling back to SQLite/In-Memory.")
            self.backend_type = "sqlite"
            conn = sqlite3.connect(self.sqlite_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS prompt_cache (
                    prompt_hash TEXT PRIMARY KEY,
                    model_name TEXT,
                    prompt_text TEXT,
                    response_json TEXT,
                    created_at TEXT
                )
            """)
            conn.commit()
            conn.close()

    @staticmethod
    def compute_hash(prompt_text: str, model_name: str = "") -> str:
        """Computes deterministic SHA256 hash of prompt and model name."""
        content = f"{model_name.strip()}||{prompt_text.strip()}".encode("utf-8")
        return hashlib.sha256(content).hexdigest()

    def get(self, prompt_text: str, model_name: str = "") -> Optional[Dict[str, Any]]:
        """Retrieves cached response if present."""
        if not settings.CACHE_ENABLED:
            return None

        prompt_hash = self.compute_hash(prompt_text, model_name)

        # In-Memory check first
        if prompt_hash in self._memory_cache:
            self.hits += 1
            return self._memory_cache[prompt_hash]

        try:
            if self.backend_type == "sqlite":
                conn = sqlite3.connect(self.sqlite_path)
                cursor = conn.cursor()
                cursor.execute("SELECT response_json FROM prompt_cache WHERE prompt_hash = ?", (prompt_hash,))
                row = cursor.fetchone()
                conn.close()
                if row:
                    self.hits += 1
                    res = json.loads(row[0])
                    self._memory_cache[prompt_hash] = res
                    return res

            elif self.backend_type == "mongodb":
                doc = self.mongo_collection.find_one({"prompt_hash": prompt_hash})
                if doc and "response_json" in doc:
                    self.hits += 1
                    res = json.loads(doc["response_json"])
                    self._memory_cache[prompt_hash] = res
                    return res

            elif self.backend_type == "redis":
                cached = self.redis_client.get(f"cache:{prompt_hash}")
                if cached:
                    self.hits += 1
                    res = json.loads(cached)
                    self._memory_cache[prompt_hash] = res
                    return res

        except Exception as e:
            logger.error(f"Cache retrieval error: {e}")

        self.misses += 1
        return None

    def set(self, prompt_text: str, response_data: Dict[str, Any], model_name: str = "") -> bool:
        """Stores evaluation response in cache."""
        if not settings.CACHE_ENABLED:
            return False

        prompt_hash = self.compute_hash(prompt_text, model_name)
        response_json = json.dumps(response_data)
        now_str = datetime.now(timezone.utc).isoformat()

        self._memory_cache[prompt_hash] = response_data

        try:
            if self.backend_type == "sqlite":
                conn = sqlite3.connect(self.sqlite_path)
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT OR REPLACE INTO prompt_cache (prompt_hash, model_name, prompt_text, response_json, created_at)
                    VALUES (?, ?, ?, ?, ?)
                """, (prompt_hash, model_name, prompt_text, response_json, now_str))
                conn.commit()
                conn.close()
                return True

            elif self.backend_type == "mongodb":
                self.mongo_collection.update_one(
                    {"prompt_hash": prompt_hash},
                    {"$set": {
                        "prompt_hash": prompt_hash,
                        "model_name": model_name,
                        "prompt_text": prompt_text,
                        "response_json": response_json,
                        "created_at": now_str
                    }},
                    upsert=True
                )
                return True

            elif self.backend_type == "redis":
                self.redis_client.set(f"cache:{prompt_hash}", response_json)
                return True

        except Exception as e:
            logger.error(f"Cache store error: {e}")

        return False

    def get_stats(self) -> Dict[str, Any]:
        """Returns cache hit/miss and hit rate statistics."""
        total = self.hits + self.misses
        hit_rate = (self.hits / total * 100.0) if total > 0 else 0.0
        cached_count = 0
        if self.backend_type == "sqlite" and self.sqlite_path.exists():
            try:
                conn = sqlite3.connect(self.sqlite_path)
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM prompt_cache")
                row = cursor.fetchone()
                if row:
                    cached_count = row[0]
                conn.close()
            except Exception:
                pass
        return {
            "backend": self.backend_type,
            "hits": self.hits,
            "misses": self.misses,
            "total_queries": total,
            "hit_rate_pct": round(hit_rate, 2),
            "stored_prompt_records": cached_count
        }

    def clear(self):
        """Clears cache entries."""
        self._memory_cache.clear()
        self.hits = 0
        self.misses = 0
        if self.backend_type == "sqlite" and self.sqlite_path.exists():
            conn = sqlite3.connect(self.sqlite_path)
            conn.execute("DELETE FROM prompt_cache")
            conn.commit()
            conn.close()

cache_manager = AttributionCache()
