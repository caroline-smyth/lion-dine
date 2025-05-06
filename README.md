# Lion Dine

<a href="https://liondine.com">Lion Dine</a> displays all the Columbia Dining menus on one page to let students compare options instantly, rather than having to click through 11 separate menus on https://dining.columbia.edu and https://dineoncampus.com/barnard/whats-on-the-menu. We receive 6,000+ views from 2,000+ users per day, out of ~7,500 meal plan holders. Over 500,000 total views since launching on October 14, 2024.

# How it works

- Scrape menu data from Columbia and Barnard dining websites using Python and Selenium. Upload a json file with all dining data to an AWS S3 bucket. The scraping file is automated through GitHub Actions to run multiple times per day.
- Flask app pulls the json file from the S3 bucket and processes it to determine which items to display based on the operating hours of the dining halls and their stations.
- Hosted on a Render Web Service.
