from PIL import Image
import argparse
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('--input', help='input image path')
parser.add_argument('--output', help='output image path')
parser.add_argument('--degree', help='rotation degree', default=-3.87)

args = parser.parse_args()

input_image_path = args.input
output_image_path = args.output

rotation_degrees = float(args.degree)

image = Image.open(input_image_path)

width, height = image.size
split_point = width // 2
left_image = image.crop((0, 0, split_point, height))
right_image = image.crop((split_point, 0, width, height))

rotated_right = right_image.rotate(rotation_degrees, expand=False)

merged_image = Image.new('RGB', (width, height))
merged_image.paste(left_image, (0, 0))
merged_image.paste(rotated_right, (split_point, 0))

merged_image.save(output_image_path)

print(f"Image rotated by {rotation_degrees} degrees and saved as {output_image_path}")
