from PIL import Image
import numpy as np


def analyze_flood_image(image):
    """
    Prototype computer-vision assessment.

    This analyzes simple visual characteristics of the image.
    It is NOT a trained flood classifier.
    """

    image = image.convert("RGB")
    image = image.resize((224, 224))

    pixels = np.array(image).astype(float)

    # Average brightness
    brightness = pixels.mean()

    # Blue-channel dominance
    blue = pixels[:, :, 2].mean()
    red = pixels[:, :, 0].mean()

    blue_ratio = blue - red

    # Prototype visual assessment
    if brightness < 70 and blue_ratio > 5:
        severity = "HIGH"
    elif brightness < 120 or blue_ratio > 8:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "severity": severity,
        "brightness": round(float(brightness), 2),
        "blue_signal": round(float(blue_ratio), 2)
    }
