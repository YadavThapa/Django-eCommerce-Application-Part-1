import urllib.request
from urllib.error import URLError, HTTPError

HOST = "http://127.0.0.1:8000"
paths = ["/", "/shop/", "/products/", "/products", "/shop", "/cart/", "/checkout/"]

results = []
for p in paths:
    url = HOST + p
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            status = r.getcode()
            body = r.read(2000)
            text = body.decode("utf-8", errors="replace")
            results.append((p, status, len(body), "product" in text.lower()))
    except HTTPError as e:
        results.append((p, e.code, 0, False))
    except URLError as e:
        results.append((p, "error", str(e.reason), False))

for r in results:
    print(r)
