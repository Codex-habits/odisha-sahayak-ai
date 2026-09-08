from PIL import Image
import numpy as np


def analyze_flood_image(image):
    """
    Prototype computer-vision assessment.

    The system first tries to reject likely:
    - documents
    - ID cards
    - screenshots
    - text-heavy images

    Then it performs a simple flood/waterlogging
    visual assessment.

    NOTE:
    This is a heuristic prototype, NOT a trained
    flood or document classifier.
    """

    # --------------------------------------------------
    # PREPARE IMAGE
    # --------------------------------------------------

    image = image.convert("RGB")

    original_width, original_height = image.size

    image = image.resize((224, 224))

    pixels = np.array(image).astype(float)

    # --------------------------------------------------
    # BASIC IMAGE FEATURES
    # --------------------------------------------------

    brightness = pixels.mean()

    red = pixels[:, :, 0]
    green = pixels[:, :, 1]
    blue = pixels[:, :, 2]

    red_mean = red.mean()
    green_mean = green.mean()
    blue_mean = blue.mean()

    blue_signal = blue_mean - red_mean

    # Colour variation
    colour_std = pixels.std()

    # --------------------------------------------------
    # GRAYSCALE IMAGE
    # --------------------------------------------------

    gray = (
        0.299 * red
        + 0.587 * green
        + 0.114 * blue
    )

    # --------------------------------------------------
    # EDGE / TEXT SIGNAL
    # --------------------------------------------------

    horizontal_edges = np.abs(
        np.diff(gray, axis=1)
    ).mean()

    vertical_edges = np.abs(
        np.diff(gray, axis=0)
    ).mean()

    edge_signal = (
        horizontal_edges
        + vertical_edges
    )

    # --------------------------------------------------
    # BRIGHT / WHITE REGION
    # --------------------------------------------------

    white_pixels = (
        (red > 180)
        & (green > 180)
        & (blue > 180)
    )

    white_ratio = white_pixels.mean()

    # --------------------------------------------------
    # DARK REGION
    # --------------------------------------------------

    dark_pixels = (
        (red < 70)
        & (green < 70)
        & (blue < 70)
    )

    dark_ratio = dark_pixels.mean()

    # --------------------------------------------------
    # SATURATION
    # --------------------------------------------------

    max_channel = np.maximum(
        np.maximum(red, green),
        blue
    )

    min_channel = np.minimum(
        np.minimum(red, green),
        blue
    )

    saturation = (
        max_channel - min_channel
    )

    saturation_mean = saturation.mean()

    # --------------------------------------------------
    # DOCUMENT / CARD DETECTION
    # --------------------------------------------------

    document_score = 0

    # Large white background
    if white_ratio > 0.35:
        document_score += 2

    # Low colour variation
    if colour_std < 65:
        document_score += 1

    # Strong edge/text-like pattern
    if edge_signal > 18:
        document_score += 2

    # Low saturation
    if saturation_mean < 45:
        document_score += 1

    # Bright image
    if brightness > 120:
        document_score += 1

    # Very wide document-like image
    aspect_ratio = (
        original_width / max(original_height, 1)
    )

    if aspect_ratio > 1.8:
        document_score += 1

    # --------------------------------------------------
    # TEXT / SCREENSHOT-LIKE DETECTION
    # --------------------------------------------------

    text_like = False

    if (
        edge_signal > 22
        and white_ratio > 0.25
        and brightness > 100
    ):
        text_like = True

    # --------------------------------------------------
    # INVALID IMAGE DECISION
    # --------------------------------------------------

    if document_score >= 4 or text_like:

        return {
            "valid_scene": False,
            "flood_detected": False,
            "severity": "INVALID",
            "assessment": (
                "This image appears to be a document, "
                "ID card, screenshot, or text-heavy image. "
                "Please upload a road, street, outdoor area, "
                "or waterlogging photograph."
            ),
            "brightness": round(
                float(brightness), 2
            ),
            "blue_signal": round(
                float(blue_signal), 2
            )
        }

    # --------------------------------------------------
    # FLOOD / WATERLOGGING ANALYSIS
    # --------------------------------------------------

    possible_water = (
        blue_signal > 8
        and brightness < 150
    )

    strong_water_signal = (
        blue_signal > 15
        and brightness < 100
    )

    # --------------------------------------------------
    # HIGH
    # --------------------------------------------------

    if strong_water_signal:

        flood_detected = True
        severity = "HIGH"

        assessment = (
            "Strong visual signals may indicate "
            "possible waterlogging."
        )

    # --------------------------------------------------
    # MEDIUM
    # --------------------------------------------------

    elif possible_water:

        flood_detected = True
        severity = "MEDIUM"

        assessment = (
            "Some visual signals may indicate "
            "possible waterlogging."
        )

    # --------------------------------------------------
    # LOW
    # --------------------------------------------------

    else:

        flood_detected = False
        severity = "LOW"

        assessment = (
            "No strong visual evidence of waterlogging "
            "was detected by this prototype."
        )

    # --------------------------------------------------
    # FINAL RESULT
    # --------------------------------------------------

    return {
        "valid_scene": True,
        "flood_detected": flood_detected,
        "severity": severity,
        "assessment": assessment,
        "brightness": round(
            float(brightness), 2
        ),
        "blue_signal": round(
            float(blue_signal), 2
        )
    }
