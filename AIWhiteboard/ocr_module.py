from PIL import Image, ImageOps, ImageFilter
import pytesseract
import difflib
import re

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

CANON_TOPICS = [
    "gravity",
    "gravitational force",
    "newton's laws of motion",
    "triangle",
    "photosynthesis",
    "left",
    "right",
    "area of triangle",
    "pythagorean theorem",
    "biodiversity",
    "photosynthesis process",
    "cell division",
    "electric current",
    "momentum",
    "kinetic energy",
    "potential energy"
]

COMMON_FIXES = {
    "triangf": "triangle",
    "gravty": "gravity",
    "graviry": "gravity",
    "gravitatio": "gravitation",
    "lefl": "left",
    "rigbt": "right",
    "newton s": "newton's",
    "photosvnthesis": "photosynthesis"
}

def _preprocess(pil_img: Image.Image) -> Image.Image:

    # Convert image to grayscale
    img = pil_img.convert("L")

    # Remove small noise
    img = img.filter(ImageFilter.MedianFilter(size=3))

    # Improve contrast
    img = ImageOps.autocontrast(img)

    # Convert to black and white
    img = img.point(
        lambda x: 0 if x < 180 else 255,
        mode="1"
    )

    # Convert back to grayscale for Tesseract
    img = img.convert("L")

    return img

def _postfix(text: str) -> str:

    s = text.lower().strip()

    # Apply common OCR corrections
    for k, v in COMMON_FIXES.items():
        s = s.replace(k, v)

    # Normalize spaces
    s = re.sub(r"\s+", " ", s).strip()

    # Match against known educational topics
    best = difflib.get_close_matches(
        s,
        CANON_TOPICS,
        n=1,
        cutoff=0.86
    )

    return best[0] if best else s


def extract_text_from_pil(pil_img: Image.Image) -> str:

    # Preprocess image
    img = _preprocess(pil_img)

    # Tesseract configuration
    cfg = (
        r"--oem 1 "
        r"--psm 6 "
        r"-c tessedit_char_whitelist="
        r"abcdefghijklmnopqrstuvwxyz"
        r"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        r"0123456789-()'"
    )

    # Run OCR and obtain confidence information
    data = pytesseract.image_to_data(
        img,
        output_type=pytesseract.Output.DICT,
        config=cfg,
        lang="eng"
    )

    words = []

    for w, conf in zip(data["text"], data["conf"]):

        try:
            confidence = float(conf)

            if w and confidence >= 65:
                words.append(w)

        except (ValueError, TypeError):
            continue

    text = " ".join(words).strip()

    # Fallback if confidence filtering removed everything
    if not text:

        text = pytesseract.image_to_string(
            img,
            config=cfg,
            lang="eng"
        ).strip()

    # Clean spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Apply corrections / topic matching
    return _postfix(text)