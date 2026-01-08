# freelancer_scraper.py
# A simple Python script to scrape job listings from Freelancer.com.
# IMPORTANT: Web scraping may violate the terms of service of websites.
# Always check the site's robots.txt and terms before scraping.
# This is for educational purposes only. Use at your own risk.
# Freelancer.com allows some public access, but automate responsibly.

import requests
from bs4 import BeautifulSoup
import csv
import time

def scrape_freelancer_jobs(pages=1):
    base_url = "https://www.freelancer.com/jobs/"
    jobs = []

    for page in range(1, pages + 1):
        url = f"{base_url}{page}/"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Failed to fetch page {page}. Status code: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')

        # Find job listings - adjust selectors if site changes
        job_cards = soup.find_all('div', class_='JobSearchCard-item')

        for card in job_cards:
            try:
                title = card.find('a', class_='JobSearchCard-primary-heading-link').text.strip()
                description = card.find('p', class_='JobSearchCard-primary-description').text.strip()
                skills_div = card.find('div', class_='JobSearchCard-secondary-tags')
                skills = [skill.text.strip() for skill in skills_div.find_all('a')] if skills_div else []
                budget = card.find('div', class_='JobSearchCard-secondary-price').text.strip()

                job = {
                    'title': title,
                    'description': description,
                    'skills': ', '.join(skills),
                    'budget': budget,
                    'url': 'https://www.freelancer.com' + card.find('a', class_='JobSearchCard-primary-heading-link')['href']
                }
                jobs.append(job)
            except AttributeError:
                # Skip if some elements are missing
                continue

        # Be polite: sleep between requests
        time.sleep(2)

    return jobs

def save_to_csv(jobs, filename='freelancer_jobs.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['title', 'description', 'skills', 'budget', 'url'])
        writer.writeheader()
        writer.writerows(jobs)

if __name__ == "__main__":
    num_pages = 3  # Change this to scrape more pages
    jobs = scrape_freelancer_jobs(num_pages)
    save_to_csv(jobs)
    print(f"Scraped {len(jobs)} jobs and saved to freelancer_jobs.csv")

# Requirements: Install via pip if needed
# pip install requests beautifulsoup4
