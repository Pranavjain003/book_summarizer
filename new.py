import requests
from bs4 import BeautifulSoup
import time

# Step 1: Get the Top 100 page
top_url = "https://www.gutenberg.org/browse/scores/top"
response = requests.get(top_url)
soup = BeautifulSoup(response.text, "html.parser")

# Step 2: Extract top 100 book links from the second <ol> in the page (the 'Top 100 EBooks last 30 days' section)
all_ol = soup.find_all("ol")
top_books = all_ol[4].find_all("a")  # This is the second list

book_ids = []

for a_tag in top_books:
    href = a_tag.get("href")  # Example: /ebooks/2701
    if href and href.startswith("/ebooks/"):
        book_id = href.split("/")[-1]
        if book_id.isdigit():
            book_ids.append(int(book_id))

print(f"📚 Found {len(book_ids)} book IDs: {book_ids[:5]}...")

# Step 3: Download each book's plain text version
for book_id in book_ids:
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    try:
        res = requests.get(url)
        if res.status_code == 200:
            filename = f"book_{book_id}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(res.text)
            print(f"✅ Downloaded: {filename}")
        else:
            print(f"❌ Failed to download book {book_id}. Status: {res.status_code}")
    except Exception as e:
        print(f"⚠️ Error for book {book_id}: {e}")
    
    time.sleep(1)  # Be polite to the server
