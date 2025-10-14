import os
import sys
from pathlib import Path

# Add repo root and main/ to sys.path (same logic as manage.py)
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "main"))

# Set Postgres env vars for this run
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main.ecommerce_project.settings")
os.environ["DB_ENGINE"] = "postgres"
os.environ["DB_NAME"] = "ecommerce_db"
os.environ["DB_USER"] = "postgres"
os.environ["DB_PASSWORD"] = "postgres"
os.environ["DB_HOST"] = "127.0.0.1"
os.environ["DB_PORT"] = "15433"

# Import and setup Django after configuring env vars
import django  # noqa: E402

django.setup()

# Execute the listing script in-process
script_path = os.path.join(os.path.dirname(__file__), "list_product_images.py")
with open(script_path, "r", encoding="utf-8") as f:
    code = f.read()
exec(compile(code, script_path, "exec"), globals())
