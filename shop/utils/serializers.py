"""
Shim for `shop.utils.serializers` that defers to `main.shop.utils.serializers`.
"""
try:
    from main.shop.utils.serializers import *  # noqa: F401,F403
except Exception:
    # Minimal fallback serializer to avoid import errors during tests.
    import pickle

    class PickleSerializer:
        def dumps(self, obj):
            return pickle.dumps(obj)

        def loads(self, data):
            return pickle.loads(data)
