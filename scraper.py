from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import os

load_dotenv()

USER = os.getenv("TWITTER_USER")
PASS = os.getenv("TWITTER_PASS")

def scrapeSocialMedia():
    with sync_playwright() as p:
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        # Open a new page
        page = browser.new_page()
        # Navigate to Twitter login page
        page.goto('https://twitter.com/login')
        # Fill in the username and password fields and log in
        page.fill('input[class="r-30o5oe r-1dz5y72 r-13qz1uu r-1niwhzg r-17gur6a r-1yadl64 r-deolkf r-homxoj r-poiln3 r-7cikom r-1ny4l3l r-t60dpp r-fdjqy7"]', USER)
        page.click('button[class="css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-ywje51 r-184id4b r-13qz1uu r-2yi16 r-1qi8awa r-3pj75a r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l"]')
        page.fill('input[type="password"]', PASS)
        page.click('button[class="css-175oi2r r-sdzlij r-1phboty r-rs99b7 r-lrvibr r-19yznuf r-64el8z r-1fkl15p r-1loqt21 r-o7ynqc r-6416eg r-1ny4l3l"]')
        
        # Wait for navigation after login
        page.wait_for_url('https://x.com/home')

        # Navigate to the search page for exoplanets
        page.goto('https://twitter.com/search?q=exoplanets&src=typed_query')

        page.wait_for_selector('article')
        previous_tweet_count = 0
        new_tweet_count = len(page.query_selector_all("article"))

        # Keep scrolling until no new tweets are loaded
        while new_tweet_count > previous_tweet_count:
            previous_tweet_count = new_tweet_count
            # Update the count of tweets loaded
            # Scroll down to load more tweets
            tweets = page.query_selector_all("article")
            for tweet in tweets:
                img_link = tweet.query_selector('img[alt="Image"]')
                video_link = tweet.query_selector('video')
                article_link = tweet.query_selector('a[href*="https"]')
                res = img_link.get_attribute('src') if img_link is not None else video_link.get_attribute('src') if video_link is not None else article_link.get_attribute('href') if article_link is not None else ""
                print(tweet.inner_text().split("\n"))
                print(res)
            # Scroll to the bottom of the page
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            page.wait_for_selector('article')  # Wait for the page to load
            new_tweet_count = len(page.query_selector_all("article"))
        # Close the browser
        browser.close()

scrapeSocialMedia()