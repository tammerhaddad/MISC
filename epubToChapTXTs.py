import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os

def split_epub(epub_path, output_dir):
    # Create output directory if not exists
    os.makedirs(output_dir, exist_ok=True)

    # Load epub
    book = epub.read_epub(epub_path)

    chapter_count = 0
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            # Extract text content
            soup = BeautifulSoup(item.get_content(), "html.parser")
            text = soup.get_text(separator="\n", strip=True)

            if text.strip():  # Skip empty chapters
                chapter_count += 1
                out_file = os.path.join(output_dir, f"chapter_{chapter_count}.txt")
                with open(out_file, "w", encoding="utf-8") as f:
                    f.write(text)
                print(f"Saved {out_file}")

    print(f"✅ Done! Extracted {chapter_count} chapters to {output_dir}")

# Example usage
split_epub("resources/The Crafting of Chess (Kit Falbo).epub", "TestFolder/output_chapters")