from io import BytesIO
import matplotlib.pyplot as plt



from google import genai
from google.genai import types
from PIL import Image
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
api_key = os.getenv("api_key")

# Create client
client = genai.Client(api_key=api_key)

# Prompt
prompt = (
    "Generate a 6-step structured portrait drawing tutorial from the uploaded image. "
    "Arrange the steps clearly in a 2x3 grid layout in correct order from Step 1 to Step 6 "
    "(Top row: Step 1, Step 2, Step 3. Bottom row: Step 4, Step 5, Step 6). "
    "Each step must progressively show the drawing process from basic construction lines "
    "to a clean final line art portrait. "
    "Step 1: Basic head oval and guidelines. "
    "Step 2: Refined head shape and hair mass blocking. "
    "Step 3: Facial feature placement using guidelines. "
    "Step 4: Hair flow and clothing structure refinement. "
    "Step 5: Clean line refinement of facial details. "
    "Step 6: Fully finished clean outline drawing only, no shading, no grayscale. "
    "Use grayscale pencil sketch style on white background with clear step labels."
)

# Load local image (put your image in same folder as this script)
image = Image.open("taylor swift.png")

# Generate response
response = client.models.generate_content(
model="gemini-3-pro-image-preview",
    contents=[prompt, image],
)

# Extract generated image
generated_image = None

for part in response.candidates[0].content.parts:
    if part.inline_data:
        generated_image = Image.open(BytesIO(part.inline_data.data))
        generated_image.save("portrait_step_by_step_tutorial.png")
        print("Full image saved successfully!")

if generated_image is None:
    print("No image returned from API")
    exit()

# ----------------------------
# Split into 6 grid images (2 rows x 3 columns)
# ----------------------------

width, height = generated_image.size

rows = 2
cols = 3

slice_width = width // cols
slice_height = height // rows

split_images = []

for r in range(rows):
    for c in range(cols):
        left = c * slice_width
        top = r * slice_height
        right = left + slice_width
        bottom = top + slice_height

        crop = generated_image.crop((left, top, right, bottom))
        split_images.append(crop)

print("Image split into 6 steps successfully!")


def apply_transparency(image, alpha_percent):
    """
    alpha_percent: 0 (invisible) to 100 (fully visible)
    """
    alpha_value = int(255 * (alpha_percent / 100))

    image = image.convert("RGBA")
    alpha_layer = Image.new("L", image.size, alpha_value)
    image.putalpha(alpha_layer)

    return image


# ----------------------------
# Display One by One
# ----------------------------

current_index = 0
total_images = len(split_images)

def show_image(index, opacity):
    transparent_img = apply_transparency(split_images[index], opacity)

    plt.imshow(transparent_img)
    plt.axis("off")
    plt.title(f"Step {index + 1} | Opacity: {opacity}%")
    plt.show()

current_index = 0
total_images = len(split_images)
opacity = 60  # default transparency %

while True:
    show_image(current_index, opacity)

    user_input = input(
        "n=next | p=previous | +=more opacity | -=less opacity | q=quit: "
    )

    if user_input.lower() == 'n':
        current_index = (current_index + 1) % total_images
    elif user_input.lower() == 'p':
        current_index = (current_index - 1) % total_images
    elif user_input == '+':
        opacity = min(100, opacity + 10)
    elif user_input == '-':
        opacity = max(0, opacity - 10)
    elif user_input.lower() == 'q':
        break
