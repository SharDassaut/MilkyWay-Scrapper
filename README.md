MilkyWay Ediciones Scraper

This project is a web scraper designed to extract product information from the MilkyWay Ediciones website. It retrieves details about products such as title, volume, authors, price, cover URL, tags, and other metadata, and saves the collected data to a JSON file.
Features

    Scrapes product data from all pages of the MilkyWay Ediciones catalog.
    Extracts detailed information for each product, including:
        Title and volume
        Authors
        Price
        Cover image URL
        Tags and filtered tags
        Additional metadata (e.g., format, size, ISBN)
    Handles pagination and stops scraping when no more products are found.
    Saves the scraped data into a JSON file named products.json.

Usage

    Install the necessary dependencies:

> pip install -r requirements.txt

Run the scraper:

>    python rework.py

    The resulting JSON file will be saved in the current directory.

Notes

    The scraper uses asynchronous HTTP requests to improve performance.
    Error handling is implemented for connection issues and unexpected responses.
    The program stops automatically when all catalog pages have been processed.

This tool is useful for collecting product data for analysis or integration into other systems