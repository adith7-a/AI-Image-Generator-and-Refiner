import datetime
import openai
import requests
from PIL import Image, ImageFilter, ImageOps, ImageEnhance
import matplotlib.pyplot as plt
from io import BytesIO
import pyttsx3

# Set the OpenAI API key
openai.api_key = "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"

# Initialize the pyttsx3 TTS engine
engine = pyttsx3.init()

# Set the voice properties for a male voice
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Select the male voice index

# Set the speech rate (lower value for slower speed)
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 50)  # Decrease the speech rate by 50

# Get the current local time
current_time = datetime.datetime.now()
current_day = datetime.datetime.now().strftime("%A")

# Extract the hour from the current time
current_hour = current_time.hour

# Print and speak the appropriate greeting based on the hour
if 5 <= current_hour < 12:
    greeting = "HELLO....GOOD MORNING USER, WELCOME TO PICSPOT...!"
elif 12 <= current_hour < 18:
    greeting = "HELLO...GOOD AFTERNOON USER, WELCOME TO PICSPOT...!!"
else:
    greeting = "HELLO...GOOD EVENING USER, WELCOME TO PICSPOT...!!"

print(greeting)
engine.say(greeting)
engine.runAndWait()

engine.say("Let me know what type of posters are u looking for...")
engine.runAndWait()

# Get the prompt from the user
prompt = input("Enter a prompt for the posters: ")

# Generate the images
num_images = 5
response = openai.Image.create(
    prompt=prompt,
    n=num_images,
    size="1024x1024"
)

# Download and display the original image
image_url = response['data'][0]['url']
image_response = requests.get(image_url)
image_data = BytesIO(image_response.content)
original_image = Image.open(image_data)

# Convert the original image to grayscale
original_image_grayscale = original_image.convert('L')

engine.say("Original Poster")
engine.runAndWait()

# Display the original image in grayscale
fig, ax = plt.subplots()
ax.imshow(original_image_grayscale, cmap='gray')
ax.axis('off')
ax.set_title("Original Poster ")
plt.show()

engine.say("Now do some picture refinements in order to show its aesthetics")
engine.runAndWait()

engine.say("Here are some of the filters that makes the poster more pleasant and beautiful...")
engine.runAndWait()

# Get the adjustment choices from the user
print("Select adjustments to apply (separated by comma):")
print("1. Gaussian Blur")
print("2. Edge Enhance")
print("3. Emboss")
print("4. Brightness")
print("5. Contrast")
print("6. Saturation")
print("7. Hue")
print("8. Temperature")


engine.say("Select any of the above adjustments...")
engine.runAndWait()

adjustment_choices = input("Select any of these adjustments: ").split(',')

# Apply the selected adjustments to the original image and display the comparison
filtered_image = original_image.copy()  # Start with the original image

for adjustment_choice in adjustment_choices:
    adjustment_choice = adjustment_choice.strip()

    if adjustment_choice == "1":
        filtered_image = filtered_image.filter(ImageFilter.GaussianBlur(radius=2))
    elif adjustment_choice == "2":
        filtered_image = filtered_image.filter(ImageFilter.EDGE_ENHANCE)
    elif adjustment_choice == "3":
        filtered_image = filtered_image.filter(ImageFilter.EMBOSS)
    elif adjustment_choice == "4":
        engine.say("Give the range for brightness factor...")
        engine.runAndWait()
        brightness_factor = float(input("Enter the brightness factor (0.0 - 2.0): "))
        enhancer = ImageEnhance.Brightness(filtered_image)
        filtered_image = enhancer.enhance(brightness_factor)
    elif adjustment_choice == "5":
        engine.say("Give the range for contrast factor...")
        engine.runAndWait()
        contrast_factor = float(input("Enter the contrast factor (0.0 - 2.0): "))
        enhancer = ImageEnhance.Contrast(filtered_image)
        filtered_image = enhancer.enhance(contrast_factor)
    elif adjustment_choice == "6":
        engine.say("Give the range for saturation factor...")
        engine.runAndWait()
        saturation_factor = float(input("Enter the saturation factor (0.0 - 2.0): "))
        enhancer = ImageEnhance.Color(filtered_image)
        filtered_image = enhancer.enhance(saturation_factor)
    elif adjustment_choice == "7":
        engine.say("Give the range for hue factor...")
        engine.runAndWait()
        hue_factor = float(input("Enter the hue factor (-0.5 - 0.5): "))
        filtered_image = filtered_image.convert('HSV')
        hue_data = filtered_image.split()[0]
        hue_data = hue_data.point(lambda i: i + hue_factor * 255)
        filtered_image = Image.merge('HSV', (hue_data, filtered_image.split()[1], filtered_image.split()[2]))
        filtered_image = filtered_image.convert('RGB')
    elif adjustment_choice == "8":
        engine.say("Give the range for temperature factor...")
        engine.runAndWait()
        temperature_factor = float(input("Enter the temperature factor (-1.0 - 1.0): "))
        r, g, b = filtered_image.split()
        r = r.point(lambda i: i + temperature_factor * 255)
        filtered_image = Image.merge('RGB', (r, g, b))

engine.say("Filtered Poster")
engine.runAndWait()

# Display the comparison
fig, axes = plt.subplots(1, 2, figsize=(10, 5))
axes[0].imshow(original_image_grayscale, cmap='gray')
axes[0].axis('off')
axes[0].set_title("Original Poster ")

axes[1].imshow(filtered_image)
axes[1].axis('off')
axes[1].set_title("Filtered Poster")

plt.show()

engine.say(f"Thank you..., Wishing you a fantastic {current_day.lower()}")
engine.runAndWait()