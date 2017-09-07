#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from urllib import parse
import shutil
import asyncio
import aiohttp
import tqdm
import string
import random
import os
import imghdr
from contextlib import closing
import sys
from hashlib import md5
from queue import Queue
from threading import Thread
import requests

class URLRetriever:
    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")
        self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver.set_window_size(1120, 550)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #print("Something failed")
        self.driver.quit()

    def clear_session(self):
        #self.driver.getSessionStorage().clear()
        #self.driver.getLocalStorage().clear()
        self.driver.delete_all_cookies()

    def get_urls_and_ranks(self, query, limit, depth=0):
        #self.clear_session()
        try:
            self.driver.get("https://images.google.com/")

            self.driver.find_element_by_id("lst-ib").send_keys(query + "\n")

            source = self.driver.page_source
            urls = [
                       parse.unquote(
                           entry.split("imgurl=")[1].split("&amp")[0]) for entry in
                       ("\n".join([entry for entry in source.split('"') if "imgres?imgurl" in entry])).split(';') if
                       "imgurl" in entry][:limit]

            #self.driver.quit()
            #self.__init__()
            return list(enumerate(urls))
        except:
            if(depth == 3):
                return []
            #print("Something failed")
            self.driver.quit()
            self.__init__()
            return self.get_urls_and_ranks(query, limit, depth+1)

def process_url(url_queue):
    while True:
        job = url_queue.get()
        url = job[1]
        position = job[0]
        download_folder = "./results"

        with requests.Session() as ses:
            try:
                r = ses.get(url, stream=True)
            except Exception as ex:
                print(ex)
                pass
            if r.status_code == 200:
                r.raw.decode_content = True

                # create random filename
                length = 10
                file_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
                filename = "/tmp/%s" % format(file_string)
                try:
                    with open(filename, 'wb') as file:
                        for chunk in r.iter_content(chunk_size=1024):
                            if chunk:  # filter out keep-alive new chunks
                                file.write(chunk)

                    # analyze
                    if os.path.isfile(filename):
                        extension = imghdr.what(filename)
                        if (extension is not None) and (not 'gif' == extension):
                            hash = md5(open(filename, 'rb').read()).hexdigest()
                            shutil.move(filename,
                                        os.path.join(download_folder, "%05d-%s.%s" % (position, hash, extension)))
                except:
                    pass
                finally:
                    if os.path.isfile(filename):
                        os.remove(filename)

        url_queue.task_done()

def retrieve_url(word_queue, url_queue):
    with URLRetriever() as scraper:
        while True:
            query = word_queue.get()

            batch = scraper.get_urls_and_ranks(query, 2)
            for entry in batch:
                url_queue.put(entry)
            time.sleep(random.random()/5)

            word_queue.task_done()


def main():
    filename = "words.txt"

    with open(filename, 'r') as f:
        dictionary = f.read().split('\n')

    url_queue = Queue(maxsize=0)
    word_queue = Queue(maxsize=0)

    images_workers = [Thread(target=process_url, args=(url_queue,)) for _ in range(10)]
    for worker in images_workers:
        worker.setDaemon(True)
        worker.start()

    url_workers = [Thread(target=retrieve_url, args=(word_queue, url_queue,)) for _ in range(5)]
    for worker in url_workers:
        worker.setDaemon(True)
        worker.start()

    print("Searching images")
    to_fetch = [random.choice(dictionary) for _ in range(2000)]

    for query in to_fetch:
        word_queue.put(query)

    pbar = tqdm.tqdm(total=len(to_fetch))
    prev_left = len(to_fetch)
    while(1):
        left = word_queue.qsize()
        pbar.update(prev_left-left)
        prev_left = left
        time.sleep(0.1)

    word_queue.join()
    url_queue.join()
    print("Finished")

if __name__ == "__main__":
    main()

