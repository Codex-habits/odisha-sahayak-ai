import torch
from PIL import Image
from transformers import CLIPProcessor, CLIPModel


# --------------------------------------------------
# LOAD PRE-TRAINED AI VISION MODEL
# --------------------------------------------------

MODEL_NAME = "openai/clip-vit-base-patch32"

_processor = None
_model = None


def load_model():

    global _processor
    global _model

    if _model is None:

        _processor = CLIPProcessor.from_pretrained(
            MODEL_NAME
        )

        _model = CLIPModel.from_pretrained(
            MODEL_NAME
        )

        _model.eval()

    return _processor, _model


# --------------------------------------------------
# IMAGE ANALYSIS
# --------------------------------------------------

def analyze_flood_image(image):

    processor, model = load_model()

    image = image.convert("RGB")

    # --------------------------------------------------
    # HIGH-LEVEL IMAGE CATEGORIES
    # --------------------------------------------------

    labels = [
        "a photo of an identity card or Aadhaar card",
        "a photo of a document or official paper",
        "a screenshot containing text",
        "a photo of a computer or phone screen",
        "a photo of a flooded street",
        "a photo of a waterlogged road",
        "a photo of a normal outdoor road",
        "a photo of an outdoor area"
    ]

    inputs = processor(
        text=labels,
        images=image,
        return_tensors="pt",
        padding=True
    )

    with torch.no_grad():

        outputs = model(**inputs)

        scores = outputs.logits_per_image[0]

        probabilities = torch.softmax(
            scores,
            dim=0
        )

    # --------------------------------------------------
    # FIND BEST CATEGORY
    # --------------------------------------------------

    best_index = int(
        torch.argmax(probabilities)
    )

    best_label = labels[best_index]

    confidence = float(
        probabilities[best_index]
    )

    # --------------------------------------------------
    # DOCUMENT / SCREEN REJECTION
    # --------------------------------------------------

    document_indices = [
        0,  # Aadhaar / identity card
        1,  # document
        2,  # screenshot
        3   # computer/phone screen
    ]

    if best_index in document_indices:

        return {
            "valid_scene": False,
            "flood_detected": False,
            "severity": "INVALID",

            "assessment": (
                "This image appears to be a document, "
                "identity card, screenshot, or screen. "
                "Please upload a road, street, outdoor "
                "area, or flood photograph."
            ),

            "brightness": 0,
            "blue_signal": 0,

            "confidence": round(
                confidence * 100, 1
            )
        }

    # --------------------------------------------------
    # FLOOD DETECTION
    # --------------------------------------------------

    flood_indices = [
        4,  # flooded street
        5   # waterlogged road
    ]

    if best_index in flood_indices:

        return {
            "valid_scene": True,
            "flood_detected": True,
            "severity": "HIGH",

            "assessment": (
                "The AI vision model identified the "
                "image as a possible flood or "
                "waterlogging scene."
            ),

            "brightness": 0,
            "blue_signal": 0,

            "confidence": round(
                confidence * 100, 1
            )
        }

    # --------------------------------------------------
    # NORMAL OUTDOOR SCENE
    # --------------------------------------------------

    return {
        "valid_scene": True,
        "flood_detected": False,
        "severity": "LOW",

        "assessment": (
            "The AI vision model identified the "
            "image as an outdoor scene without a "
            "strong flood indication."
        ),

        "brightness": 0,
        "blue_signal": 0,

        "confidence": round(
            confidence * 100, 1
        )
    }
