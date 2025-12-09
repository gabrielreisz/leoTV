from typing import Any, Optional, Dict
from datetime import datetime, timedelta

class CacheManager:
    def __init__(self, default_ttl_seconds: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.default_ttl = default_ttl_seconds
    
    def _make_key(self, prefix: str, identifier: str) -> str:
        return f"{prefix}:{identifier}"
    
    def get(self, prefix: str, identifier: str) -> Optional[Any]:
        key = self._make_key(prefix, identifier)
        
        if key not in self.cache:
            return None
        
        entry = self.cache[key]
        expires_at = entry.get('expires_at')
        
        if expires_at and datetime.now() > expires_at:
            del self.cache[key]
            return None
        
        return entry.get('data')
    
    def set(self, prefix: str, identifier: str, data: Any, ttl_seconds: Optional[int] = None) -> None:
        key = self._make_key(prefix, identifier)
        ttl = ttl_seconds if ttl_seconds is not None else self.default_ttl
        expires_at = datetime.now() + timedelta(seconds=ttl)
        
        self.cache[key] = {
            'data': data,
            'expires_at': expires_at,
            'cached_at': datetime.now()
        }
    
    def invalidate(self, prefix: str, identifier: str) -> None:
        key = self._make_key(prefix, identifier)
        if key in self.cache:
            del self.cache[key]
    
    def invalidate_prefix(self, prefix: str) -> None:
        keys_to_remove = [key for key in self.cache.keys() if key.startswith(f"{prefix}:")]
        for key in keys_to_remove:
            del self.cache[key]
    
    def clear(self) -> None:
        self.cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        total_entries = len(self.cache)
        expired_entries = 0
        valid_entries = 0
        
        now = datetime.now()
        for entry in self.cache.values():
            expires_at = entry.get('expires_at')
            if expires_at and now > expires_at:
                expired_entries += 1
            else:
                valid_entries += 1
        
        return {
            'total_entries': total_entries,
            'valid_entries': valid_entries,
            'expired_entries': expired_entries,
            'cache_size_mb': self._estimate_size_mb()
        }
    
    def _estimate_size_mb(self) -> float:
        import sys
        total_size = sys.getsizeof(self.cache)
        for key, value in self.cache.items():
            total_size += sys.getsizeof(key) + sys.getsizeof(value)
        return round(total_size / (1024 * 1024), 2)
    
    def cleanup_expired(self) -> int:
        now = datetime.now()
        keys_to_remove = []
        
        for key, entry in self.cache.items():
            expires_at = entry.get('expires_at')
            if expires_at and now > expires_at:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self.cache[key]
        
        return len(keys_to_remove)

_cache_instance: Optional[CacheManager] = None

def get_cache(ttl_seconds: int = 3600) -> CacheManager:
    global _cache_instance
    if _cache_instance is None:
        _cache_instance = CacheManager(default_ttl_seconds=ttl_seconds)
    return _cache_instance

def clear_cache() -> None:
    global _cache_instance
    if _cache_instance:
        _cache_instance.clear()

