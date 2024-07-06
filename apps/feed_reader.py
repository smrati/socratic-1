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
        'https://www.bhaskar.com/rss-v1--category-1061.xml',
        'https://www.firstpost.com/commonfeeds/v1/mfp/rss/india.xml',
        'https://www.firstpost.com/commonfeeds/v1/mfp/rss/world.xml',
        'https://www.firstpost.com/commonfeeds/v1/mfp/rss/politics.xml',
        'https://zeenews.india.com/rss/india-national-news.xml'
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
                    'URL': link,
                    'published': published
                }
            )
        final_feeds += feeds
    df = pd.DataFrame(final_feeds)

    # Convert the URL column to clickable links
    df['URL'] = df['URL'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')

    # Display the DataFrame
    st.markdown(df.to_html(escape=False), unsafe_allow_html=True)