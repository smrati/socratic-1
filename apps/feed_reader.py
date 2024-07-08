import streamlit as st
import pandas as pd
import aiohttp
import asyncio
import feedparser


async def fetch_rss(session, url):
    async with session.get(url) as response:
        return await response.text()


async def parse_rss(session, url, source):
    rss_content = await fetch_rss(session, url)
    feed = feedparser.parse(rss_content)
    return {"feed": feed, "source": source}



async def fetch_all_rss(feed_source_map):
    async with aiohttp.ClientSession() as session:
        tasks = [parse_rss(session, url, source) for source, url in feed_source_map.items()]
        results = await asyncio.gather(*tasks)
        return results



def fetch_feeds():
    st.title('Feed Reader')
    feeds = {
        "Bhaskar": 'https://www.bhaskar.com/rss-v1--category-1061.xml',
        "FP : India": 'https://www.firstpost.com/commonfeeds/v1/mfp/rss/india.xml',
        "FP: World": 'https://www.firstpost.com/commonfeeds/v1/mfp/rss/world.xml',
        "FP : Politics": 'https://www.firstpost.com/commonfeeds/v1/mfp/rss/politics.xml',
        "Zee News :  National": 'https://zeenews.india.com/rss/india-national-news.xml'
    }

    results = asyncio.run(fetch_all_rss(feeds))

    final_feeds = []
    for result in results:
        feeds = []
        for entry in result["feed"].entries:
            title = entry.title
            link = entry.link
            published = None
            source = result["source"]
            try:
                published = entry.published
            except:
                pass
            feeds.append(
                {
                    'title': title,
                    'URL': link,
                    'published': published,
                    'source' : source
                }
            )
        final_feeds += feeds
    df = pd.DataFrame(final_feeds)

    # Convert the URL column to clickable links
    df['link'] = df.apply(lambda row: f'<a href="{row["URL"]}">{row["title"]}</a>', axis=1)
    # Select only the required columns
    new_df = df[['link', 'published', 'source']]

    # Dropdown widget
    selected_source = st.selectbox('Select a source:', ['All'] + new_df['source'].unique().tolist())

    # Function to filter DataFrame based on dropdown selection
    def filter_df(source):
        if source == 'All':
            return new_df[['link', 'published', 'source']]
        else:
            return new_df[new_df['source'] == source][['link', 'published', 'source']]

    # Filtered DataFrame
    filtered_df = filter_df(selected_source)

    # Display DataFrame in Streamlit
    st.write(filtered_df.to_html(escape=False), unsafe_allow_html=True)

    # # Display the DataFrame
    # st.markdown(new_df.to_html(escape=False), unsafe_allow_html=True)