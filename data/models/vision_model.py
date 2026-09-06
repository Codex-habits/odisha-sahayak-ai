from PIL import Image
import numpy as np


def analyze_flood_image(image):
    """
    Prototype visual assessment.

    This separates the result into:
    - Flood/waterlogging indication
    - No obvious flood indication
    - Uncertain

    It is NOT a trained flood-detection model.
    """

    image = image.convert("RGB")
    image = image.resize((224, 224))

    pixels = np.array(image).astype(float)

    brightness = pixels.mean()

    red = pixels[:, :, 0].mean()
    green = pixels[:, :, 1].mean()
    blue = pixels[:, :, 2].mean()

    blue_signal = blue - red

    # Prototype visual signals
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
        "flood_detected": flood_detected,
        "severity": severity,
        "assessment": assessment,
        "brightness": round(float(brightness), 2),
        "blue_signal": round(float(blue_signal), 2)
    }
