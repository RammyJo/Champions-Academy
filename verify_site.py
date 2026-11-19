"""Check generated links, images and metadata before a static deployment."""
import json
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
from PIL import Image

ROOT = Path(__file__).resolve().parent
DIST = ROOT / "dist"


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.images = []
        self.ids = []
        self.h1 = 0
        self.canonicals = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1": self.h1 += 1
        if a.get("id"): self.ids.append(a["id"])
        if tag in ("a", "script", "link"):
            if tag == "link" and a.get("rel") == "canonical": self.canonicals += 1
            self.links.append(a.get("href", a.get("src", "")))
        if tag == "img":
            assert "alt" in a, "Image missing alt"
            if a.get("src"): self.images.append(a["src"])
            self.images.extend(item.strip().split()[0] for item in a.get("srcset", "").split(",") if item.strip())


def verify():
    checked = 0
    for path in DIST.rglob("*.html"):
        p = PageParser()
        p.feed(path.read_text(encoding="utf-8"))
        assert p.h1 == 1, (path, p.h1)
        assert len(p.ids) == len(set(p.ids)), (path, "Duplicate IDs")
        assert p.canonicals == (0 if path.name == "404.html" else 1), (path, "Canonical")
        for url in p.links + p.images:
            parsed = urlsplit(url)
            if parsed.scheme or parsed.netloc or not parsed.path: continue
            destination = DIST / parsed.path.lstrip("/")
            if destination.is_dir(): destination /= "index.html"
            assert destination.is_file(), (path, url)
            checked += 1
    for image in (DIST / "assets").iterdir():
        with Image.open(image) as data: data.verify()
    library = json.loads((ROOT / "photo-library.json").read_text())
    for key, record in library.items():
        for width in record["widths"]:
            with Image.open(DIST / "assets" / f"{key}-{width}.webp") as data:
                assert data.width == width <= record["width"], (key, "Unexpected scaling")
    print(f"PASS: {len(list(DIST.rglob('*.html')))} HTML pages, {checked} local references, all images decode, {len(library)} source records")


if __name__ == "__main__":
    verify()
