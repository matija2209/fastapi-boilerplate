import io

from magic import Magic
from PIL import Image


def process_image(image_data):
    """
    
    """
    # Identify format
    mime_type = Magic(mime=True).from_buffer(image_data)

    # Check if image format is supported
    if mime_type in ("image/png", "image/jpeg", "image/gif"):
        # Handle each format differently
        if mime_type == "image/png":
            img = Image.open(io.BytesIO(image_data)).convert("RGB")  # Convert to RGB for JPEG
        elif mime_type == "image/jpeg":
            img = Image.open(io.BytesIO(image_data))
        else:  # GIF needs special handling
            # ... (code for handling GIFs, convert to PNG/JPEG if needed)
            pass
        # Resize if needed
        if img.height > 400:
            ratio = img.width / img.height
            new_width = int(400 * ratio)
            img = img.resize((new_width, 400))

        # Convert to JPG and compress
        output_buffer = io.BytesIO()
        img.save(output_buffer, format="JPEG", quality=55)  # Adjust quality as needed
        compressed_image_data = output_buffer.getvalue()

        # Return compressed image data and format
        return compressed_image_data, "image/jpeg"
    else:
        # Handle unsupported formats (raise error, log, etc.)
        print(f"IGNORED: Unsupported image format: {mime_type}")
        return
        # raise ValueError(f"Unsupported image format: {mime_type}")

