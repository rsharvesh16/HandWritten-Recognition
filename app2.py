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
    with open('test.jpg', 'wb') as image_file:
        image_file.write(base64.urlsafe_b64decode(image_str))
    return ""

def main():
    # Apply a light background color to the entire app
    # background_image = Image.open("crop.jpg")
    # st.image(background_image, use_column_width=True)

    # theme = f"""
    # <style>
    #     body {{
    #         background: url(data:image/jpeg;base64,{base64.b64encode(background_image.tobytes()).decode()});
    #         background-size: cover;
    #         color: #333; /* Light mode text color */
    #     }}
    # </style>
    # """
    # st.markdown(theme, unsafe_allow_html=True)

    page_bg_img = '''
    <style>
    [data-testid="stAppViewContainer"]{
    background-image: url("https://wallpapercave.com/wp/wp9163623.jpg");
    background-size: cover;
    opacity: 0.8;
    }

    [data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
    }

    [date-testid="stToolbar"]{
    right =
    }
    </style>
    '''

    st.markdown(page_bg_img, unsafe_allow_html=True)

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
        
    # Display the uploaded image
    image = Image.open("test.jpg")

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