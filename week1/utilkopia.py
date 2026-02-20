import requests

REPO_OWNER = "kopia"
REPO_NAME = "kopia"
BASE_PATH = "site/content/docs"
REF = "master" # or "main" if your default branch is main
GITHUB_API = "https://api.github.com"

EXCLUDE_PATTERNS = [
    "contributing"
    "privacy",
    "release-notes",
    "privacy-policy"
    ]

def is_excluded(path):
    lower = path.lower()
    for pat in EXCLUDE_PATTERNS:
        if pat in lower: 
            return True 
        return False

def list_docs_index_md_files(path):
    results = []
    url = f"{GITHUB_API}/repos/{REPO_OWNER}/{REPO_NAME}/contents/{path}?ref={REF}"
    resp = requests.get(url)
    resp.raise_for_status()
    items = resp.json() # items can be a dict if we hit a file directly; handle both if isinstance(items, dict): items = [items]

    for item in items:
        item_type = item.get("type")
        item_path = item.get("path", "")
        if is_excluded(item_path):
            continue
        if item_type == "dir":
            results.extend(list_docs_index_md_files(item_path))
        elif item_type == "file":
            name = item.get("name", "")
            if name.endswith("_index.md"):
                # Collect the blob URL (the URL to view the file on GitHub)
                blob_url = item.get("html_url") or item.get("url")
                # If html_url exists, that's the human-friendly page URL
                results.append(blob_url)
    return results

def get_urls():
    docs_indexes = list_docs_index_md_files(BASE_PATH) # Optional: print as a simple list for u in docs_indexes: print(u)
    return docs_indexes

kopia_urls = [
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Actions/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Architecture/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Caching/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Compatibility/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Compression/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Consistency/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/ECC/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Encryption/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Kopiaignore/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Logging/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Maintenance/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Ransomware%20Protection/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Sharding/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Storage%20Tiers/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/Synchronization/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Advanced/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Contribution%20guidelines/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/FAQs/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Features/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Getting%20started/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Installation/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Mounting/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Reference/Command-Line/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Reference/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Release%20Notes/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Repositories/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Repository%20Server/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/Upgrade/_index.md',
    'https://github.com/kopia/kopia/blob/master/site/content/docs/_index.md'
    ]

kopia_raw = [
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Actions/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Architecture/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Caching/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Compatibility/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Compression/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Consistency/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/ECC/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Encryption/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Kopiaignore/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Logging/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Maintenance/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Ransomware%20Protection/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Sharding/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Storage%20Tiers/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/Synchronization/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Advanced/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Contribution%20guidelines/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/FAQs/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Features/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Getting%20started/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Installation/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Mounting/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Reference/Command-Line/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Reference/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Release%20Notes/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Repositories/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Repository%20Server/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/Upgrade/_index.md',
    'https://raw.githubusercontent.com/kopia/kopia/refs/heads/master/site/content/docs/_index.md'
     ]