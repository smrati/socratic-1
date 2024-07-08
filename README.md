# socratic-1
RSS feed reader created using streamlit

Select Feed source from the dropdown

![RSS feed reader](./rss_feed_reader.png)

You can add more sources to rss feed reader by going to apps > feed_reader.py file and adding data under
`feeds` variable in line 30


To run streamlit application
```
streamlit run main.py --server.port 8002
```
It will start a streamlit server in your localhost at port 8002
