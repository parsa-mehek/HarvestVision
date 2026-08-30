from collections import Counter
from PIL import Image
import streamlit as st


class ImageUtils:
    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size

    @staticmethod
    def _luminance(pixel):
        red, green, blue = pixel
        return (0.299 * red) + (0.587 * green) + (0.114 * blue)

    @staticmethod
    def _is_background(pixel):
        red, green, blue = pixel
        return red > 235 and green > 235 and blue > 235

    def _leaf_pixels(self, image):
        resized = image.convert("RGB").resize((160, 160))
        pixels = list(resized.getdata())
        leaf_pixels = [pixel for pixel in pixels if not self._is_background(pixel)]

        return leaf_pixels if leaf_pixels else pixels

    def load_image(self, uploaded_file):
        """
        Load uploaded image using Pillow.
        """
        if uploaded_file is None:
            return None

        image = Image.open(uploaded_file)
        return image

    def resize_image(self, image):
        """
        Resize image.
        """
        if image is None:
            return None

        return image.resize(self.image_size)

    def display_image(self, image, caption="Leaf Image"):
        """
        Display image in Streamlit.
        """
        if image is not None:
            st.image(
                image,
                caption=caption,
                use_container_width=True
            )

    def image_info(self, image):
        """
        Return basic image information.
        """
        if image is None:
            return None

        return {
            "Width": image.width,
            "Height": image.height,
            "Mode": image.mode,
            "Format": image.format
        }

    def detect_leaf_color(self, image):
        """
        Estimate the dominant leaf color from the uploaded image.
        """

        leaf_pixels = self._leaf_pixels(image)
        votes = Counter()

        for red, green, blue in leaf_pixels:
            if green >= red and green >= blue and (green - min(red, blue)) >= 14:
                votes["Green"] += 1
            elif red >= 110 and green >= 110 and abs(red - green) <= 70 and blue <= min(red, green):
                votes["Yellow"] += 1
            else:
                votes["Brown"] += 1

        return votes.most_common(1)[0][0] if votes else "Green"

    def detect_leaf_spot(self, image):
        """
        Estimate whether the leaf contains spot-like discoloration.
        """

        leaf_pixels = self._leaf_pixels(image)
        average_luminance = sum(self._luminance(pixel) for pixel in leaf_pixels) / len(leaf_pixels)
        average_red = sum(pixel[0] for pixel in leaf_pixels) / len(leaf_pixels)
        average_green = sum(pixel[1] for pixel in leaf_pixels) / len(leaf_pixels)
        average_blue = sum(pixel[2] for pixel in leaf_pixels) / len(leaf_pixels)

        spot_pixels = 0

        for red, green, blue in leaf_pixels:
            luminance = self._luminance((red, green, blue))
            color_distance = abs(red - average_red) + abs(green - average_green) + abs(blue - average_blue)

            if luminance < average_luminance * 0.78 and color_distance > 45:
                spot_pixels += 1
            elif luminance < 82 and red < average_red and green < average_green and blue < average_blue:
                spot_pixels += 1

        return "Yes" if (spot_pixels / len(leaf_pixels)) >= 0.10 else "No"

    def detect_leaf_attributes(self, image):
        """
        Detect leaf color and spot presence from the image.
        """

        return {
            "Leaf_Color": self.detect_leaf_color(image),
            "Leaf_Spot": self.detect_leaf_spot(image),
        }

    def save_image(self, image, save_path):
        """
        Save image.
        """
        if image is not None:
            image.save(save_path)