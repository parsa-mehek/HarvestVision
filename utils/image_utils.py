from PIL import Image
import streamlit as st


class ImageUtils:
    def __init__(self, image_size=(224, 224)):
        self.image_size = image_size

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

    def save_image(self, image, save_path):
        """
        Save image.
        """
        if image is not None:
            image.save(save_path)