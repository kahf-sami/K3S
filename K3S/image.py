import Image
import ImageDraw
import ImageFont

#use ImageDraw.text - but it doesn't do any formating, it just prints string at the given location

img = Image.new('RGB', (200, 100))
d = ImageDraw.Draw(img)
d.text((20, 20), 'Hello', fill=(255, 0, 0))
to find out the text size:
text_width, text_height = d.textsize('Hello')
When creating image, add an aditional argument with the required color (white):
img = Image.new('RGB', (200, 100), (255, 255, 255))
#until you save the image with Image.save method, there would be no file. Then it's only a matter of a proper transformation to put it into your GUI's format for display. This can be done by encoding the image into an in-memory image file:

import cStringIO
s = cStringIO.StringIO()
img.save(s, 'png')
in_memory_file = s.getvalue()
this can be then send to GUI. Or you can send direct raw bitmap data:
raw_img_data = img.tostring()