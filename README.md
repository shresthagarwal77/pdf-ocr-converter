# PDF OCR Converter

This is a Python script that converts PDF files to images and performs Optical Character Recognition (OCR) on the images to extract the text content. It uses the `pdf2image` and `pytesseract` libraries to achieve this.

## Features

- Convert PDF files to a sequence of images
- Perform OCR on each image to extract the text content
- Format the OCR text and display the results

## Requirements

- Python 3.6 or above
- Install the required dependencies using the following command:

pip install pdf2image pytesseract pillow

- Install Tesseract OCR and ensure it is properly configured. Refer to the [Tesseract OCR documentation](https://tesseract-ocr.github.io/tessdoc/Installation.html) for installation instructions.

## Usage

1. Clone the repository:

```bash
git clone https://github.com/shresthagarwal77/pdf-ocr-converter.git
```

2. Navigate to the project directory:

```bash
cd pdf-ocr-converter
```
3. Run the script:
```bash
python ocr_converter.py
```

4. A file dialog will open. Select the PDF file you want to convert.

5. The script will convert the PDF to images and perform OCR on each image. The formatted OCR text will be displayed in the console.

## Customization

- Image Preprocessing: If you want to customize the image preprocessing steps, you can modify the `preprocess_image` function in the code.

- OCR Settings: You can adjust the OCR settings by modifying the `perform_ocr_on_image` function. For example, you can change the language, OCR configuration, or experiment with different OCR engines.

## API Endpoint (Optional)

You can also use this PDF to Text Converter as an API endpoint. This allows you to convert PDF files to text programmatically by sending HTTP requests. Here's how to use the API endpoint:

1. Start the Flask server:
```bash
python ocr_converter.py
```

2. Send a POST request to the following endpoint using a tool like Postman:

```bash
POST http://localhost:5000/process_pdf
```

3. Attach the PDF file to the request body.

4. The server will process the PDF file, convert it to text using OCR, and return the extracted text as the response.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions to this project are welcome. Feel free to open an issue or submit a pull request for any improvements or bug fixes.

## Acknowledgements

This project makes use of the following libraries:

- [pdf2image](https://github.com/Belval/pdf2image) - Convert PDF to image
- [pytesseract](https://github.com/madmaze/pytesseract) - OCR engine for Python
- [Pillow](https://python-pillow.org/) - Image processing library
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - Python's standard GUI package

## Resources

- [Tesseract OCR Documentation](https://tesseract-ocr.github.io/tessdoc/)
- [pdf2image Documentation](https://github.com/Belval/pdf2image#readme)
- [pytesseract Documentation](https://pypi.org/project/pytesseract/)
- [Pillow Documentation](https://pillow.readthedocs.io/)
- [Postman](https://www.postman.com/) - API development and testing tool
