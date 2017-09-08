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

DEBUG = False

@asyncio.coroutine
def download_file(url, position, download_folder, session, semaphore):
    # this routine is protected by a semaphore
    with (yield from semaphore):
        response = yield from session.get(url)

        # create random filename
        length = 10
        file_string = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(length))
        filename = "/tmp/%s"%format(file_string)

        try:
            with closing(response), open(filename, 'wb') as file:
                while True:  # save file
                    chunk = yield from response.content.read()
                    if not chunk:
                        break
                    file.write(chunk)
                #analyze
                if os.path.isfile(filename):
                    extension = imghdr.what(filename)
                    if (extension is not None) and (not 'gif' == extension):
                        hash = md5(open(filename, 'rb').read()).hexdigest()
                        shutil.move(filename, os.path.join(download_folder,"%05d-%s.%s"%(position, hash, extension)))
        finally:
            if os.path.isfile(filename):
                os.remove(filename)

@asyncio.coroutine
def wait_with_progressbar(coros):
    for f in tqdm.tqdm(asyncio.as_completed(coros), total=len(coros)):
        yield from f


def move_to_element_and_click(driver, element):
    actions = webdriver.common.action_chains.ActionChains(driver)
    actions.move_to_element(element)
    actions.click(element)
    actions.perform()

def main():

    if len(sys.argv) != 4:
        print("Usage: [query] [download_folder] [limit]")
        return

    try:
        query = sys.argv[1]
        download_folder = sys.argv[2]
        limit = int(sys.argv[3])

        if limit == 0:
            limit = 100000
    except:
        print("Invalid args")
        return

    print("Scrapper started for query: %s"%query)

    if DEBUG:
        driver = webdriver.Chrome()
    else:
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36")
        driver = webdriver.PhantomJS(desired_capabilities=dcap)
        driver.set_window_size(1120, 550)

    try:
        driver.get("https://images.google.com/")
        driver.find_element_by_id("lst-ib").send_keys(query+"\n")

        print("Started infinite scroll")
        #simulate infinite scroll:
        while(1):
            pos = driver.execute_script("window.scrollBy(0,2000000);")

            if driver.find_element_by_id("smb").is_displayed() or driver.find_element_by_id("isr_cld").is_displayed():
                time.sleep(0.5)
            else:
                break
            move_to_element_and_click(driver, driver.find_element_by_id("smb"))

        print("Infinite scroll finished")

        source = driver.page_source

        urls = [
            parse.unquote(
                entry.split("imgurl=")[1].split("&amp")[0]) for entry in
            ("\n".join([entry for entry in source.split('"') if "imgres?imgurl" in entry])).split(';') if "imgurl" in entry][:limit]

        print("Found: ",len(urls)," images")

        if not os.path.isdir(download_folder):
            os.mkdir(download_folder)
        else:
            response = input("Folder %s already exists, proceed(y/n): "%download_folder)
            if response != 'y':
                return

        with closing(asyncio.get_event_loop()) as loop, \
             closing(aiohttp.ClientSession()) as session:

            semaphore = asyncio.Semaphore(10)

            coroutines = [download_file(url, rank, download_folder, session, semaphore) for rank, url in enumerate(urls)]
            eloop = asyncio.get_event_loop()
            eloop.run_until_complete(asyncio.gather(wait_with_progressbar(coroutines)))


        print("Scrapper finished")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
