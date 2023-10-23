import os
from PIL import Image

# Function to convert PNG to JPG
def convert_png_to_jpg(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith('.png'):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + '.jpg')

            image = Image.open(input_path)
            image = image.convert('RGB')
            image.save(output_path)
            print(f"Converted {filename} to JPG")

if __name__ == "__main__":
    input_folder = r"G:\surf\screenshots\fromdrive"  # Replace with the path to your folder containing PNG files
    output_folder = r"G:\surf\screenshots\fromdrive\jpeg"  # Output folder for the converted JPG files

    convert_png_to_jpg(input_folder, output_folder)
