import pymupdf


def pdf_to_images(file_path: str):
    document = pymupdf.open(file_path)

    images = []

    for page in document:
        pixmap = page.get_pixmap(matrix=pymupdf.Matrix(2, 2))
        image_bytes = pixmap.tobytes("png")
        images.append(image_bytes)

    document.close()

    return images