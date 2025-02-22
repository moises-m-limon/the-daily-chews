import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from transformers import pipeline

# URL for Google Trends
URL = "https://trends.google.com/trending?geo=US&hours=24"

# Initialize zero-shot classification pipeline
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
# Candidate labels
candidate_labels = ["sports", "politics", "entertainment", "science"]

def initialize_driver():
    """Initialize and return a Selenium WebDriver instance."""
    driver = webdriver.Chrome()
    return driver

def get_category(text):
    """Classify a trend into categories."""
    if pd.isnull(text):
        return 'other'
    result = classifier(text, candidate_labels)
    return result['labels'][0]

def get_trends():
    """Extract trending topics and return as a DataFrame."""
    driver = initialize_driver()
    driver.get(URL)
    time.sleep(5)
    
    try:
        trends_table = driver.find_element(By.XPATH, "//table[contains(@class, 'enOdEe-wZVHld-zg7Cn')]")
    except Exception as e:
        print(f"Could not locate the trends table: {e}")
        driver.quit()
        return pd.DataFrame()
    
    trend_rows = trends_table.find_elements(By.XPATH, ".//tr[@role='row']")
    if len(trend_rows) > 1:
        trend_rows = trend_rows[1:]
    
    data = []
    for trend in trend_rows[:25]:
        try:
            trend_name = trend.find_element(By.XPATH, ".//td[contains(@class, 'jvkLtd')]//div").text.strip()
            search_volume = trend.find_element(By.XPATH, ".//td[contains(@class, 'dQOTjf')]//div").text.strip()
            
            breakdown_elements = trend.find_elements(By.XPATH, ".//td[contains(@class, 'xm9Xec')]//button")
            breakdown_keywords = [b.text.strip() for b in breakdown_elements if b.text.strip()]
            
            time_started = trend.find_element(By.XPATH, ".//td[contains(@class, 'WirRge')]//div").text.strip()
            
            data.append({
                "Trend": trend_name,
                "Search Volume": search_volume,
                "Trend Breakdown": ", ".join(breakdown_keywords),
                "Time Started": time_started
            })
        except Exception as e:
            print(f"Error extracting trend: {e}")
    
    driver.quit()
    df = pd.DataFrame(data)
    
    def add_categories(df):
        """Apply category classification to trends."""
        df['category'] = df['Trend'].apply(get_category)
        return df
    
    return add_categories(df)
