import feedparser
import smtplib
from email.mime.text import MIMEText
import datetime
from openai import OpenAI

OPENAI_API_KEY = "YOUR_OPENAI_KEY"

EMAIL_ADDRESS = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
TO_EMAIL = "your_email@gmail.com"

client = OpenAI(api_key=OPENAI_API_KEY)

keywords = [
    "Hyundai Motor",
    "Hyundai EV",
    "Hyundai autonomous vehicle",
    "Hyundai software defined vehicle"
]


def collect_news():

    articles = []

    for keyword in keywords:

        url = f"https://news.google.com/rss/search?q={keyword}"

        feed = feedparser.parse(url)

        for entry in feed.entries[:5]:

            articles.append(
                f"{entry.title} ({entry.link})"
            )

    return articles


def summarize(news):

    news_text = "\n".join(news)

    prompt = f"""
You are an automotive industry analyst.

Summarize the following news into sections:

1. Strategic Moves
2. Industry Trends
3. Market Signals

Each item should include:
- Headline
- Key Point
- Strategic Impact

News:
{news_text}
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


def send_email(summary):

    today = datetime.date.today()

    subject = f"Daily Mobility Intelligence - {today}"

    msg = MIMEText(summary)
    msg["Subject"] = subject
    msg["From"] = EMAIL_ADDRESS
    msg["To"] = TO_EMAIL

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

    server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

    server.sendmail(
        EMAIL_ADDRESS,
        TO_EMAIL,
        msg.as_string()
    )

    server.quit()


def main():

    news = collect_news()

    summary = summarize(news)

    send_email(summary)


if __name__ == "__main__":
    main()
