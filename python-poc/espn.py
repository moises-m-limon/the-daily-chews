import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def initialize_driver():
    chrome_options = Options()
    # Run with GUI first for debugging, then enable headless mode if working
    # chrome_options.add_argument("--headless")  
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def search_espn_and_extract_articles(query):
    query = query.replace(" ", "+")  # Format query for URL
    url = f"https://www.espn.com/search/results?q={query}"

    driver = initialize_driver()
    driver.get(url)
    
    # Wait for page to load
    time.sleep(5)

    try:
        # Locate the main `article__Results` container
        articles_container = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CLASS_NAME, "article__Results"))
        )

        # Find all articles inside `article__Results`
        articles = articles_container.find_elements(By.CLASS_NAME, "article__Results__Item")

        articles_data = []
        for article in articles:
            try:
                # Get the article link
                link_element = article.find_element(By.CLASS_NAME, 
                    "AnchorLink.contentItem__content.contentItem__content--standard.overflow-hidden.contentItem__content--fullWidth.flex.hasImage")
                article_link = link_element.get_attribute("href")

                # Convert relative URLs to absolute ESPN links
                if article_link.startswith("/"):
                    article_link = "https://www.espn.com" + article_link

                # Get the article title
                title_element = article.find_element(By.CLASS_NAME, "contentItem__title")
                article_title = title_element.text.strip()

                # Store the data
                articles_data.append({"Title": article_title, "URL": article_link})

            except Exception as e:
                print(f"Error extracting article details: {e}")
                continue

    except Exception as e:
        print(f"Error locating articles: {e}")
        articles_data = []

    driver.quit()

    # Convert to DataFrame
    df = pd.DataFrame(articles_data)
    return df

def extract_espn_article_text(article_url):
    """
    Given an ESPN article URL, this function extracts and concatenates all paragraph (<p>) tags
    inside the class 'article-body' into a single string.
    """
    driver = initialize_driver()
    driver.get(article_url)

    # Wait for the article body to load
    try:
        article_body = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "article-body"))
        )

        # Extract all paragraph tags
        paragraphs = article_body.find_elements(By.TAG_NAME, "p")

        # Concatenate into a single string
        article_text = " ".join([p.text.strip() for p in paragraphs if p.text.strip()])

    except Exception as e:
        print(f"Error extracting article text: {e}")
        article_text = ""

    driver.quit()
    return article_text
