# Web Scraping Portfolio

This repository contains a collection of web scraping tools and scripts, demonstrating various techniques and approaches to extracting data from websites.

Since a real scraper needs to be under maintenance, the idea of this repository is not the usage of the code (it will stop working as soon as websites change something), but to show how Scrapy and Selenium can be mixed in the structure.

## Disclaimer

This tool is for educational purposes only.
Always respect websites' terms of service and robots.txt files when scraping.

## Project Structure

- `Main`: The entry point of the application, orchestrating the scraping process.
- `Selenium Scraper`: A Selenium-based scraper for a real house renting website.
- `Scrapy Scraper`:  A Scrapy-based scraper from real house renting website.
- `Logger_setup.py`: Configuration for logging throughout the project.

## Features

- Selenium-based web scraping project
- Scrapy-based web scraping project
- Scrapy integration
- Configurable logging
- CSV data export

### Logging

The project uses a custom logging setup defined in `logger_setup.py`, which loads configuration from a YAML file.

## Usage

To run the scraper:

1. Ensure all dependencies are installed via requirements.txt.
2. Run `main.py`

