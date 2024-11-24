import os
import json
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Function to get the last 5 Instagram post links using Selenium
def get_instagram_posts(username):
    # Set up the WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run browser in headless mode (without GUI)
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    # Initialize the Chrome WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Open the Instagram page of the specified user
        driver.get(f'https://www.instagram.com/{username}/')

        # Wait for the page to load (may need to increase the time depending on your connection speed)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        
        # Scroll down to load more posts (optional but can help load posts)
        body = driver.find_element(By.TAG_NAME, 'body')
        for _ in range(5):  # Scroll five times to load more posts
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        # Wait for posts to load
        posts = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//a[contains(@href, '/p/')]")))

        # Get unique post URLs (some may be duplicated during scrolling)
        post_links = []
        for post in posts[:5]:  # Limit to the first 5 posts
            # Get the post link without the base URL
            post_link = post.get_attribute("href")
            # Only append the post part (after '/p/')
            if post_link not in post_links:
                post_links.append(post_link)

        return post_links

    finally:
        # Close the browser after extraction
        driver.quit()

# Function to push the JSON file to GitHub
def push_to_github(json_file):
    # Stage and commit the file
    subprocess.run(["git", "add", json_file])
    subprocess.run(["git", "commit", "-m", "Update Instagram post links"])
    
    # Push to GitHub (replace with your repository branch name, e.g., 'main')
    subprocess.run(["git", "push", "origin", "main"])

# Example usage
username = 'erasmus_plus_projects'  # Replace with the Instagram username you want to scrape
posts = get_instagram_posts(username)

# Save the links to a file to be used by the website
if posts:
    with open("../instagram_posts.json", "w") as f:
        json.dump(posts, f)
    
    # After saving the file, push it to GitHub
    push_to_github("../instagram_posts.json")

