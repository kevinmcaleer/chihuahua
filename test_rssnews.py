import feedparser

# Define the RSS feed URL
rss_url = "http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/front_page/rss.xml"

# Parse the RSS feed
feed = feedparser.parse(rss_url)

# Check for errors
if feed.bozo:
    print(f"Error fetching the RSS feed: {feed.bozo_exception}")
else:
    # Fetch the top 5 headlines
    headlines = [entry.title for entry in feed.entries[:5]]

    # Print the headlines
    print("Top 5 Headlines:")
    for i, headline in enumerate(headlines, start=1):
        print(f"{i}. {headline}")
