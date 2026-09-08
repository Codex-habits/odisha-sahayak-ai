from PIL import Image
import numpy as np


def analyze_flood_image(image):
    """
    Prototype flood/waterlogging image assessment.

    First performs a conservative check for obvious
    document/card/text images, then analyzes the scene.

    NOTE:
    This is a prototype heuristic, not a trained
    flood-detection classifier.
    """

    # -----------------------------------------
    # Prepare image
    # -----------------------------------------

    image = image.convert("RGB")

    original_width, original_height = image.size

    image = image.resize((224, 224))

    pixels = np.array(image).astype(float)

    red = pixels[:, :, 0]
    green = pixels[:, :, 1]
    blue = pixels[:, :, 2]

    # -----------------------------------------
    # Basic measurements
    # -----------------------------------------

    brightness = pixels.mean()

    red_mean = red.mean()
    blue_mean = blue.mean()

    blue_signal = blue_mean - red_mean

    colour_std = pixels.std()

    # -----------------------------------------
    # Grayscale
    # -----------------------------------------

    gray = (
        0.299 * red
        + 0.587 * green
        + 0.114 * blue
    )

    # -----------------------------------------
    # Edge / texture
    # -----------------------------------------

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

    # -----------------------------------------
    # White area
    # -----------------------------------------

    white_pixels = (
        (red > 190)
        & (green > 190)
        & (blue > 190)
    )

    white_ratio = white_pixels.mean()

    # -----------------------------------------
    # Colour variation
    # -----------------------------------------

    max_channel = np.maximum(
        np.maximum(red, green),
        blue
    )

    min_channel = np.minimum(
        np.minimum(red, green),
        blue
    )

    saturation = max_channel - min_channel

    saturation_mean = saturation.mean()

    # -----------------------------------------
    # Spatial variation
    #
    # Real outdoor scenes usually have
    # significant differences between regions.
    # -----------------------------------------

    grid_means = []

    rows = 4
    cols = 4

    for r in range(rows):
        for c in range(cols):

            y1 = r * 56
            y2 = (r + 1) * 56

            x1 = c * 56
            x2 = (c + 1) * 56

            region = pixels[y1:y2, x1:x2]

            grid_means.append(region.mean())

    spatial_variation = np.std(grid_means)

    # -----------------------------------------
    # Document score
    # -----------------------------------------

    document_score = 0

    # Very large white background
    if white_ratio > 0.60:
        document_score += 2

    # Very low colour variation
    if colour_std < 45:
        document_score += 1

    # Text-like edges
    if edge_signal > 25:
        document_score += 1

    # Low saturation
    if saturation_mean < 30:
        document_score += 1

    # Bright image
    if brightness > 150:
        document_score += 1

    # -----------------------------------------
    # Scene protection
    #
    # If the image has strong spatial variation,
    # it is more likely to be a real scene.
    # -----------------------------------------

    scene_like = (
        spatial_variation > 20
        or colour_std > 70
        or saturation_mean > 50
    )

    # Only reject when document evidence is strong
    # AND the image does not look like a scene.
    if document_score >= 5 and not scene_like:

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
