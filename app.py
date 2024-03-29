import streamlit as st
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas
import io
import base64
import numpy as np
import pytesseract 
import pyttsx3


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
def ocr(image):
    text=pytesseract.image_to_string(image, lang = 'eng')
    print("Recognized Text:", repr(text))
    return text

def draw_Text(draw, position, size=5):
    draw.ellipse(position, fill="white")

def speak_text(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

def get_image_download_link(image):
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_str = base64.b64encode(buffered.getvalue()).decode()
    href = f'<a href="data:file/png;base64,{image_str}" download="signed_image.png">Download Text</a>'
    return href


def main():
    # Apply a light background color to the entire app
    theme = """
    <style>
        body {
            background-color: #f0f0f0; /* Light mode background color */
            color: #333; /* Light mode text color */
        }
    </style>
    """
    st.markdown(theme, unsafe_allow_html=True)

    st.title("HandScribeVoice")

    # Draw Text
    st.header("Draw Text")
    st.warning("Use the canvas below to draw your Text.")

    # Create a blank canvas with a white background
    canvas_result = st_canvas(
        fill_color="white",  # Set the canvas background color to white
        stroke_width=5,  # Width of the drawing stroke
        stroke_color="#000",  # Color of the drawing stroke
        update_streamlit=True,
        height=400,  # Set the height of the canvas
    )

    # Get the drawn Text from the canvas
    if canvas_result.image_data is not None:
        # Convert canvas image data to NumPy array
        image_array = np.array(canvas_result.image_data)

        # Create Image from NumPy array
        Text_image = Image.fromarray(image_array.astype('uint8'), 'RGBA')

        st.image(Text_image, caption="Text", use_column_width=True)

        # Save the image with the drawn Text
        st.markdown(get_image_download_link(Text_image), unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("Choose an image...", type="png")

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Perform OCR on the image
        text_result = ocr(image)

        # Display the recognized text
        st.header("Recognized Text:")
        st.text(text_result)

    st.warning("Click the button below to listen to the recognized text.")
    if st.button("Listen to Text"):
        speak_text(text_result)


if __name__ == "__main__":
    main()