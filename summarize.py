import os
from transformers import pipeline
import textwrap

# Step 1: Load the model
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6", framework="pt")

# Step 2: Path to a single book file
book_path = "download_books/book_1342.txt"  # Example: Pride and Prejudice

# Step 3: Read the entire book text
with open(book_path, "r", encoding="utf-8") as f:
    text = f.read().replace('\n', ' ').strip()

# Step 4: Split into chunks (about 1000 characters per chunk)
chunks = textwrap.wrap(text, width=1000)

print(f"📚 Total Chunks Created: {len(chunks)}")

# Step 5: Summarize each chunk and collect results
partial_summaries = []

for i, chunk in enumerate(chunks):
    try:
        print(f"🧠 Summarizing chunk {i+1}/{len(chunks)}...")
        summary = summarizer(chunk, max_length=120, min_length=40, do_sample=False)[0]['summary_text']
        partial_summaries.append(summary)
    except Exception as e:
        print(f"⚠️ Failed at chunk {i+1}: {e}")
        continue

# Step 6: Combine all small summaries into one long final summary
final_summary = " ".join(partial_summaries)

# Step 7: Save to a single file
with open("final_long_summary.txt", "w", encoding="utf-8") as f:
    f.write(final_summary)

print("\n✅ Done! Combined summary saved to final_long_summary.txt")
