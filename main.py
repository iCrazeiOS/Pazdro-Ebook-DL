import requests, gettoken
from math import ceil

email = input("Enter your email/username: ")
password = input("Enter your password: ")
bookID = input("Enter book ID (Found at: https://ebook.pazdro.com.pl/app/book/<ID HERE>/full): ")

if not (email and password and bookID):
	print("Must fill in each field")
	exit()

print("\n[*] Attempting to login with credentials...")

response = gettoken.getToken(email, password)
if response["error"]:
	print(f"[!] Error: {response['message']}")
	exit()

print(f"[*] Got access token")

headers = {
	"User-Agent": "iCraze",
	"Accept": "application/pdf",
	"Accept-Language": "en-GB,en;q=0.5",
	"Authorization": f"Bearer {response['message']}",
	"Connection": "keep-alive",
	"Referer": f"https://ebook.pazdro.com.pl/app/book/{bookID}/full",
	"Sec-Fetch-Dest": "empty",
	"Sec-Fetch-Mode": "cors",
	"Sec-Fetch-Site": "same-origin"
}

print("[*] Fetching PDF...")
with requests.get(f"https://ebook.pazdro.com.pl/api/library-cards/me/purchased-books/{bookID}/content", headers=headers, stream=True) as r:
	if r.status_code != 200:
		print("[!] Error - Book ID may be incorrect")
		exit()
	r.raise_for_status()

	totalChunks = ceil(int(r.headers["content-length"])/8192)
	with open(f"{bookID}.pdf", 'wb') as f:
		currentChunk = 1
		for chunk in r.iter_content(chunk_size=8192):
			print(f"[*] Fetching chunk {currentChunk}/{totalChunks}", end="\r")
			f.write(chunk)
			currentChunk += 1

		print(f"\n\n[*] Done - Saved to {bookID}.pdf!")
