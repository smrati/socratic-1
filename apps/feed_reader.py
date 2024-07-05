import streamlit as st
import pandas as pd
import aiohttp
import asyncio
import feedparser


async def fetch_rss(session, url):
    async with session.get(url) as response:
        return await response.text()

async def parse_rss(session, url):
    rss_content = await fetch_rss(session, url)
    feed = feedparser.parse(rss_content)
    return feed

async def fetch_all_rss(feeds):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_rss(session, url) for url in feeds]
        results = await asyncio.gather(*tasks)
        return results
def fetch_feeds():
    st.title('Feed Reader')
    feeds = [
        'http://feeds.bbci.co.uk/news/rss.xml',
        'http://rss.cnn.com/rss/edition.rss',
        'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml'
    ]

    results = asyncio.run(fetch_all_rss(feeds))

    final_feeds = []
    for result in results:
        feeds = []
        for entry in result.entries:
            title = entry.title
            link = entry.link
            published = None
            try:
                published = entry.published
            except:
                pass
            feeds.append(
                {
                    'title': title,
                    'link': link,
                    'published': published
                }
            )
        final_feeds += feeds
    final_df = pd.DataFrame(final_feeds)
    st.dataframe(final_df)