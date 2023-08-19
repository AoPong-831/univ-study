from PIL import Image
import pyocr
import os

path = ';C:\\Users\\produ\\AppData\\Local\\Programs\\Tesseract-OCR'
os.environ['PATH'] = os.environ['PATH'] + path

tools = pyocr.get_available_tools()
tool = tools[0]

img = Image.open("test.png")

builder = pyocr.builders.TextBuilder(tesseract_layout=6)
text = tool.image_to_string(img, lang="jpn", builder=builder)

text = text.replace(' ', '')
print(text)