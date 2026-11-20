"""Prepare locally reviewed school photos. Requires Pillow; normal builds do not."""
import json
from pathlib import Path
from PIL import Image, ImageChops, ImageOps

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "media-library/facebook-originals"
ASSETS = ROOT / "static/assets"
SELECTION = [
    ("photo-06.jpg", "classroom-welcome", "Students following a classroom presentation", "Learning", "A classroom full of possibilities"),
    ("photo-07.jpg", "learning-together", "Students sitting together, with several raising their hands", "Together", "Learning alongside one another"),
    ("photo-08.jpg", "finding-voice", "A student standing beside her desk and raising her hand", "Learning", "The courage to take part"),
    ("photo-10.jpg", "bright-smile", "A smiling student at her desk giving a thumbs-up", "Together", "Little moments of confidence"),
    ("photo-11.jpg", "joyful-classroom", "Students and their teacher smiling and waving in a classroom", "Together", "Joy that fills a classroom"),
    ("photo-13.jpg", "shared-joy", "A group of students and an adult raising their arms and smiling", "Together", "Better when we are together"),
    ("photo-14.jpg", "digital-discovery", "A student concentrating on a tablet at his desk", "Learning", "Curiosity in action"),
    ("photo-15.jpg", "screen-skills", "A smiling student holding a tablet in class", "Learning", "Discovering new ways to learn"),
    ("photo-16.jpg", "little-discoveries", "Young learners raising their hands around a classroom table", "Learning", "Small hands, big curiosity"),
    ("photo-17.jpg", "classmates", "Students seated together and waving from their desks", "Together", "Growing with friends"),
    ("photo-18.jpg", "teachers-together", "Students and an adult smiling together in a classroom", "Together", "Learning is a shared journey"),
    ("photo-01.jpg", "storytelling", "A speaker holding a microphone and an eagle puppet during an activity", "Learning", "Bringing a story to life"),
]


def prepare():
    sources = dict(line.split(maxsplit=1) for line in (ROOT / "media-library/facebook-shortlist/sources.txt").read_text().splitlines() if line.strip())
    library = {}
    for filename, key, alt, category, caption in SELECTION:
        image = ImageOps.exif_transpose(Image.open(SOURCE / filename)).convert("RGB")
        # Some Facebook image files contain white letterboxing. Trim only the
        # surrounding border; never modify subjects or enlarge a source image.
        mask = ImageChops.difference(image, Image.new("RGB", image.size, "white")).convert("L").point(lambda value: 255 if value > 22 else 0)
        crop = mask.getbbox()
        image = image.crop(crop)
        assert image.width >= 900, f"Source too small for publication: {filename} ({image.width}px)"
        widths = sorted(set([min(480, image.width), min(768, image.width), image.width]))
        for width in widths:
            resized = image.resize((width, round(image.height * width / image.width)), Image.Resampling.LANCZOS)
            resized.save(ASSETS / f"{key}-{width}.webp", quality=91, method=6)
        library[key] = dict(alt=alt, category=category, caption=caption, widths=widths,
                            width=image.width, height=image.height, source=sources[filename],
                            original=filename, crop=list(crop))
    (ROOT / "photo-library.json").write_text(json.dumps(library, indent=2) + "\n", encoding="utf-8")
    print(f"Prepared {len(library)} reviewed photos without upscaling")


if __name__ == "__main__":
    prepare()
