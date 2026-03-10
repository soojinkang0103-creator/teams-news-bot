import requests
import feedparser
import datetime
import pytz
from openai import OpenAI

OPENAI_API_KEY = "YOUR_OPENAI_KEY"
TEAMS_WEBHOOK = "YOUR_TEAMS_WEBHOOK"

client = OpenAI(api_key=OPENAI_API_KEY)

keywords = [
"Hyundai Motor",
"Hyundai EV",
"Hyundai autonomous",
"Hyundai software defined vehicle"
]

def collect_news():

    articles = []

    for keyword in keywords:

        url = f"https://news.google.com/rss/search?q={keyword}"

        feed = feedparser.parse(url)

        for entry in feed.entries[:10]:

            articles.append({
                "title": entry.title,
                "link": entry.link
            })

    return articles


def deduplicate(articles):

    seen = set()
    unique = []

    for a in articles:

        if a["title"] not in seen:

            unique.append(a)
            seen.add(a["title"])

    return unique[:20]


def summarize(news):

    text = "\n".join(
        [f"{a['title']} ({a['link']})" for a in news]
    )

    prompt = f"""
You are an automotive industry analyst.

Analyze the following news.

Group insights into:

1. Strategic Moves
2. Industry Trends
3. Market Signals

For each item include

Headline
Key point
Strategic impact

News:
{text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role":"user","content":prompt}]
    )

    return response.choices[0].message.content


def send_to_teams(summary):

    today = datetime.date.today().strftime("%Y-%m-%d")

    payload = {
        "text": f"""
📊 Daily Mobility Intelligence
Date: {today}

{summary}
"""
    }

    requests.post(TEAMS_WEBHOOK, json=payload)


def main():

    news = collect_news()

    news = deduplicate(news)

    summary = summarize(news)

    send_to_teams(summary)


if __name__ == "__main__":
    main()
