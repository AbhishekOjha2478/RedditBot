import os
import requests
import praw
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1️⃣ Reddit API Credentials
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD"),
    user_agent=os.getenv("USER_AGENT")
)

# 2️⃣ Get Daily Trending Posts
def get_trending_posts(subreddit_name, limit=5, access_token=None):
    subreddit = reddit.subreddit(subreddit_name)
    trending_posts = subreddit.rising(limit=limit)  # Fetch NEW trending posts

    for post in trending_posts:
        print(f"🔥 {post.title}\n🔗 {post.url}\n")
        post_to_wordpress(post.title, post.url, access_token)  # Post to WordPress

# 3️⃣ Post to WordPress
def post_to_wordpress(post_title, post_content, access_token):
    post_url = f"https://public-api.wordpress.com/rest/v1.1/sites/{os.getenv('WORDPRESS_SITE')}/posts/new"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    post_data = {
        'title': post_title,
        'content': post_content,
        'status': 'publish'  # Change to 'draft' if needed
    }

    response = requests.post(post_url, json=post_data, headers=headers)
    if response.status_code == 201:
        print("✅ Post successfully created!")
    else:
        print(f"❌ Error: {response.status_code} - {response.text}")

# 4️⃣ Automate Daily Posting
if __name__ == "__main__":
    WORDPRESS_ACCESS_TOKEN = os.getenv("WORDPRESS_ACCESS_TOKEN")

    if not WORDPRESS_ACCESS_TOKEN:
        print("❌ Error: No WordPress access token found. Please check your .env file.")
    else:
        get_trending_posts("popular", access_token=WORDPRESS_ACCESS_TOKEN)  # Fetch from "popular" subreddit
