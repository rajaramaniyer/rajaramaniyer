import PyPDF2
from wand.image import Image

# Open the PDF
with open("D:/Books/Govinda Shatakam/Govinda_Shatakam_Tamil.pdf", "rb") as file:
    reader = PyPDF2.PdfReader(file)
    # Iterate over every page
    for page in reader.pages:
        # Create an image object from the page
        with Image(filename="D:/Books/Govinda Shatakam/GSTamil{}".format(page)) as img:
            # Save the image
            img.save(filename="page{}.jpg".format(page))
