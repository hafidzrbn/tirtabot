import os
import sys
import json
import pandas as pd

try:
    from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
except ImportError:
    print("Installing youtube-comment-downloader...")
    os.system(f"{sys.executable} -m pip install youtube-comment-downloader pandas")
    from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR

video_urls = [
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

downloader = YoutubeCommentDownloader()
all_comments = []

for idx, url in enumerate(video_urls, 1):
    print(f"[{idx}/{len(video_urls)}] Fetching comments for: {url}")
    try:
        comments = downloader.get_comments_from_url(url, sort_by=SORT_BY_POPULAR)
        count = 0
        for comment in comments:
            all_comments.append({
                "video_url": url,
                "video_id": url.split("/")[-1].split("?")[0],
                "cid": comment.get("cid"),
                "author": comment.get("author"),
                "text": comment.get("text"),
                "time": comment.get("time"),
                "votes": comment.get("votes"),
                "replies": comment.get("replies")
            })
            count += 1
            if count % 100 == 0:
                print(f"   Fetched {count} comments so far...")
        print(f" Finished video {url}: total {count} comments.")
    except Exception as e:
        print(f" Error fetching {url}: {e}")

print(f"\nTotal comments collected across all videos: {len(all_comments)}")

df = pd.DataFrame(all_comments)
csv_path = "youtube_comments_dr_tirta.csv"
json_path = "youtube_comments_dr_tirta.json"

df.to_csv(csv_path, index=False, encoding="utf-8-sig")
df.to_json(json_path, orient="records", force_ascii=False, indent=2)

print(f"Saved to {csv_path} and {json_path}")
