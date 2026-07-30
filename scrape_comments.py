import os
import sys
import pandas as pd

try:
    from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
except ImportError:
    os.system(f"{sys.executable} -m pip install youtube-comment-downloader pandas")
    from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

# Target YouTube Video URLs (Dr. Tirta Podcasts, Health Education, and Shoe Reviews)
VIDEO_URLS = [
    "https://youtu.be/CoVz4-TPYgM",
    "https://youtu.be/lqeDF5JwYvM",
    "https://youtu.be/dSq0Z5XpoLc",
    "https://youtu.be/l5pK6sfhxt0",
    "https://youtu.be/LCWsCEqAU8s",
    "https://youtu.be/UyalifZrhGM",
    "https://youtu.be/QtIxl1YM9Bk",
    "https://youtu.be/7mrwndoqyMk",
    "https://youtu.be/2qWR_b1HE18",
    "https://youtu.be/41itFALrNU8"
]

def scrape_youtube_comments(urls):
    downloader = YoutubeCommentDownloader()
    all_comments = []
    
    for idx, url in enumerate(urls, 1):
        print(f"[{idx}/{len(urls)}] Fetching comments: {url}")
        try:
            comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
            count = 0
            for c in comments:
                all_comments.append({
                    "video_url": url,
                    "video_id": url.split("/")[-1].split("?")[0],
                    "cid": c.get("cid"),
                    "author": c.get("author"),
                    "text": c.get("text"),
                    "time": c.get("time"),
                    "votes": c.get("votes"),
                    "replies": c.get("replies")
                })
                count += 1
            print(f"   Completed {url} -> {count:,} comments.")
        except Exception as e:
            print(f"   Error fetching {url}: {e}")
            
    return pd.DataFrame(all_comments)

if __name__ == "__main__":
    df = scrape_youtube_comments(VIDEO_URLS)
    print(f"\nTotal comments collected: {len(df):,}")
    
    df.to_csv("youtube_comments_dr_tirta.csv", index=False, encoding="utf-8-sig")
    df.to_json("youtube_comments_dr_tirta.json", orient="records", force_ascii=False, indent=2)
    print("Dataset saved to 'youtube_comments_dr_tirta.csv' and '.json'.")
