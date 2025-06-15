import re

HTML_FILE = "index.html"
TWEET_FILE = "tweets.txt"
SECTIONS = ["Tortured", "Realistic", "Optimistic", "Delusional", "Point of No Return"]

def generate_embed(tweet_url):
    return f'<blockquote class="twitter-tweet"><a href="{tweet_url}"></a></blockquote>'

def load_tweet_urls():
    with open(TWEET_FILE, "r") as file:
        lines = file.read().splitlines()

    tweets = {}
    current_section = None

    for line in lines:
        line = line.strip()
        if line.startswith("[") and line.endswith("]"):
            current_section = line[1:-1]
            tweets[current_section] = []
        elif line and current_section:
            tweets[current_section].append(line)

    return tweets

def update_html_section(section_name, embed_html):
    with open(HTML_FILE, "r", encoding="utf-8") as file:
        html = file.read()

    start_tag = f"<!-- SECTION: {section_name} START -->"
    end_tag = f"<!-- SECTION: {section_name} END -->"

    new_content = f"{start_tag}\n{embed_html}\n{end_tag}"
    html = re.sub(f"{start_tag}.*?{end_tag}", new_content, html, flags=re.DOTALL)

    with open(HTML_FILE, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"[✔] Updated section: {section_name}")

def main():
    tweets = load_tweet_urls()
    print("[▶] Injecting manual tweet embeds...")

    for section in SECTIONS:
        tweet_urls = tweets.get(section, [])
        if not tweet_urls:
            print(f"  [!] No tweets found for {section}")
            continue

        embed_html = "\n".join(generate_embed(url) for url in tweet_urls)
        update_html_section(section, embed_html)

    print("[✅] All sections updated.")

if __name__ == "__main__":
    main()
