# Google Images Scrapper

> Usage: ./fetch.py \[query\] \[download_folder\] \[limit\]

This script for a given Google Images `[query]` retrieves from the search results at most `[limit]` urls to original images hosted on the web and then tries to retrieve them to a folder located at `[download_folder]`.

#### Dependencies
- Selenium
- PhantomJS
- aiohttp
- tqdm