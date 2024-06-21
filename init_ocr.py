import easyocr

"""Used to initialize the english language model when creating the Docker image."""
reader = easyocr.Reader(['en'], gpu=False)