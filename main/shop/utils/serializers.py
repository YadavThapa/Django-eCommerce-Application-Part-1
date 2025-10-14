"""Compact Pickle-based session serializer kept in a utilities package.

This preserves previous behaviour (accepts base64 or raw pickle bytes)
while being concise and easy to maintain.
"""

import base64
import pickle
from typing import Any


class PickleSerializer:
    """Compact Pickle-based serializer used for session data.

    The serializer emits base64-encoded pickle bytes for safe storage in
    Django sessions and accepts both raw pickle bytes and base64-encoded
    strings when loading.
    """

    def dumps(self, obj: Any) -> bytes:
        """Return base64-encoded pickle bytes."""
        raw = pickle.dumps(obj, protocol=pickle.HIGHEST_PROTOCOL)
        return base64.b64encode(raw)

    def loads(self, data):
        """Accept bytes or str; try base64 then raw pickle."""
        if data is None:
            return None
        raw = data.encode("ascii") if isinstance(data, str) else data
        try:
            return pickle.loads(base64.b64decode(raw, validate=True))
        except (pickle.UnpicklingError, TypeError, ValueError):
            return pickle.loads(raw)
