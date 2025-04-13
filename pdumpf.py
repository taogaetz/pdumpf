#!/usr/bin/env python3

import argparse
import subprocess
import os
import re  # Import the regular expression module


def convert_pdf_to_jpgs(pdf_path, output_dir, dpi=150):
    """
    Converts a PDF file to a series of JPG images using ImageMagick.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Path to the directory where JPG images will be saved.
        dpi (int, optional): The DPI (dots per inch) for the conversion. Defaults to 150.
    """
    # 1. Validate input PDF path
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    # 2. Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # 3. Use ImageMagick's convert command
    try:
        print(f"Converting PDF: {pdf_path} to JPGs in {output_dir} at {dpi} dpi.")
        command = [
            "convert",
            "-density",
            str(dpi),
            pdf_path,
            os.path.join(output_dir, "page-%03d.jpg"),  # Output filename pattern
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        # ImageMagick usually prints to standard output, even for conversions.
        print(result.stdout)
        print("✅ All pages converted to .jpg and saved.")

    except subprocess.CalledProcessError as e:
        print(f"Error running ImageMagick convert: {e}")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Standard Output:\n{e.output}")
        print(f"Standard Error:\n{e.stderr}")
        return
    except FileNotFoundError:
        print(
            "Error: ImageMagick's convert command is not installed or not in your system's PATH."
        )
        print(
            "Please install ImageMagick and ensure the 'convert' command is accessible."
        )
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return


def main():
    """
    Parses command-line arguments and calls the PDF to JPG conversion function.
    """
    parser = argparse.ArgumentParser(
        description="Convert PDF to JPG images using ImageMagick."
    )
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument(
        "--output-dir", default="output_jpgs", help="Directory to save JPG files"
    )
    parser.add_argument(
        "--dpi", type=int, default=150, help="DPI for conversion (default: 150)"
    )

    args = parser.parse_args()
    convert_pdf_to_jpgs(args.pdf, args.output_dir, args.dpi)


if __name__ == "__main__":
    main()
