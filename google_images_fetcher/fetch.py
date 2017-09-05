#!/usr/bin/env python3
from selenium import webdriver
import time
import requests
from urllib import parse
import shutil
import os

DEBUG = True

def move_to_element_and_click(driver, element):
    actions = webdriver.common.action_chains.ActionChains(driver)
    actions.move_to_element(element)
    actions.click(element)
    actions.perform()

def main():
    print("Scrapper started")

    if DEBUG:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.PhantomJS()
        driver.set_window_size(1120, 550)

    driver.get("https://images.google.com/")
    driver.find_element_by_id("lst-ib").send_keys("trypophobia\n")

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

    urls = [parse.unquote(entry.split("imgurl=")[1].split("&amp")[0]) for entry in ("\n".join([entry for entry in source.split('"') if "imgres?imgurl" in entry])).split(';') if "imgurl" in entry]

    print("Found: ",len(urls)," images")

    if not os.path.isdir("results"):
        os.mkdir("results")

    for url, i in enumerate(urls):
        r = requests.get(settings.STATICMAP_URL.format(url), stream=True)
        if r.status_code == 200:
            with open(os.path.join("results/", "%05d"%i), 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    print("Scrapper finished")
    driver.quit()


if __name__ == "__main__":
    main()
