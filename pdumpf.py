#!/usr/bin/env python3

import argparse
import subprocess
import os
import re  # Import the regular expression module


def convert_pdf_to_ppms(pdf_path, output_dir, dpi=150):
    """
    Converts a PDF file to a series of PPM images, handling errors and edge cases.

    Args:
        pdf_path (str): Path to the input PDF file.
        output_dir (str): Path to the directory where PPM images will be saved.
        dpi (int, optional): The DPI (dots per inch) for the conversion. Defaults to 150.
    """
    # 1. Validate input PDF path
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return

    # 2. Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)  # Use exist_ok to avoid errors if it exists

    # 3. Use pdftoppm to convert PDF to PPMs (and get page count from it)
    try:
        # Construct the command.  Crucially, add -progress to get page count.
        command = [
            "pdftoppm",
            "-f",
            "1",  # Start from page 1
            "-l",
            "",  # No limit initially, we'll parse output
            "-r",
            str(dpi),
            "-progress",  # Get page count in a portable way
            pdf_path,
            os.path.join(output_dir, "page"),  # Output filename *prefix*
        ]
        result = subprocess.run(
            command, capture_output=True, text=True, check=True
        )  # capture output as text, check raises exception on error.

        # Parse the output to get the number of pages.  This is much more robust.
        num_pages = 0
        for line in result.stderr.splitlines():  # pdftoppm prints to standard error
            match = re.search(r"Page (\d+)/(\d+)", line)
            if match:
                num_pages = int(match.group(2))  # get the *total* pages.
                break  # only need the last one.
        if num_pages == 0:
            print("Error: Could not determine number of pages from pdftoppm output.")
            print(f"Standard Error:\n{result.stderr}")  # Print stderr to help debug
            return

        print(
            f"Converting {num_pages} pages from {pdf_path} to PPMs in {output_dir} at {dpi} dpi."
        )

        # 4. Rename files to be correct.
        for page in range(1, num_pages + 1):
            old_ppm_path = os.path.join(
                output_dir, f"page-{page}-{page}.ppm"
            )  # pdftoppm adds the page number
            new_ppm_path = os.path.join(
                output_dir, f"page-{page}.ppm"
            )  # correct filename
            if os.path.exists(old_ppm_path):  # check exists
                os.rename(old_ppm_path, new_ppm_path)
            else:
                print(
                    f"Warning: Expected file {old_ppm_path} was not created.  Check pdftoppm output."
                )

        print("✅ All pages converted to .ppm and saved.")

    except subprocess.CalledProcessError as e:
        print(f"Error running pdftoppm: {e}")
        print(f"Command: {e.cmd}")  # Print the command that failed
        print(f"Return code: {e.returncode}")
        print(f"Standard Output:\n{e.output}")  # show the output
        print(f"Standard Error:\n{e.stderr}")
        return  # Exit the function on error

    except FileNotFoundError:
        print("Error: pdftoppm is not installed or not in your system's PATH.")
        print("Please install poppler (which provides pdftoppm) and try again.")
        return
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return


def main():
    """
    Parses command-line arguments and calls the PDF to PPM conversion function.
    """
    parser = argparse.ArgumentParser(description="Convert PDF to .ppm images.")
    parser.add_argument("pdf", help="Input PDF file")
    parser.add_argument(
        "--output-dir", default="output_ppms", help="Directory to save .ppm files"
    )
    parser.add_argument(
        "--dpi", type=int, default=150, help="DPI for conversion (default: 150)"
    )

    args = parser.parse_args()
    convert_pdf_to_ppms(args.pdf, args.output_dir, args.dpi)


if __name__ == "__main__":
    main()
