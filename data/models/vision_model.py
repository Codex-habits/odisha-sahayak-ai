from PIL import Image
import numpy as np


def analyze_flood_image(image):
    """
    Prototype flood/waterlogging image assessment.

    First checks whether the uploaded image appears to be
    a real outdoor scene rather than a document/card image.
    """

    image = image.convert("RGB")
    image = image.resize((224, 224))

    pixels = np.array(image).astype(float)

    # -----------------------------------------
    # Basic visual measurements
    # -----------------------------------------

    brightness = pixels.mean()

    red = pixels[:, :, 0].mean()
    green = pixels[:, :, 1].mean()
    blue = pixels[:, :, 2].mean()

    blue_signal = blue - red

    # Colour variation
    colour_std = pixels.std()

    # -----------------------------------------
    # Detect likely document/card images
    # -----------------------------------------

    gray = (
        0.299 * pixels[:, :, 0]
        + 0.587 * pixels[:, :, 1]
        + 0.114 * pixels[:, :, 2]
    )

    # Edge strength
    horizontal_edges = np.abs(np.diff(gray, axis=1)).mean()
    vertical_edges = np.abs(np.diff(gray, axis=0)).mean()

    edge_signal = horizontal_edges + vertical_edges

    # Documents/cards usually have:
    # - relatively uniform background
    # - strong rectangular/text edges
    # - comparatively low colour variation

    likely_document = (
        edge_signal > 18
        and colour_std < 65
        and brightness > 80
    )

    if likely_document:
        return {
            "valid_scene": False,
            "flood_detected": False,
            "severity": "INVALID",
            "assessment": (
                "This image appears to be a document, "
                "card, or non-scene image. Please upload "
                "a road, street, or outdoor area photograph."
            ),
            "brightness": round(float(brightness), 2),
            "blue_signal": round(float(blue_signal), 2)
        }

    # -----------------------------------------
    # Flood / waterlogging assessment
    # -----------------------------------------

    possible_water = (
        blue_signal > 8
        and brightness < 150
    )

    strong_water_signal = (
        blue_signal > 15
        and brightness < 100
    )

    if strong_water_signal:

        flood_detected = True
        severity = "HIGH"

        assessment = (
            "Strong visual signals may indicate "
            "possible waterlogging."
        )

    elif possible_water:

        flood_detected = True
        severity = "MEDIUM"

        assessment = (
            "Some visual signals may indicate "
            "possible waterlogging."
        )

    else:

        flood_detected = False
        severity = "LOW"

        assessment = (
            "No strong visual evidence of waterlogging "
            "was detected by this prototype."
        )

    return {
        "valid_scene": True,
        "flood_detected": flood_detected,
        "severity": severity,
        "assessment": assessment,
        "brightness": round(float(brightness), 2),
        "blue_signal": round(float(blue_signal), 2)
    }
