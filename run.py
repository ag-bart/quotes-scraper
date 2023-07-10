import asyncio
import os
import logging
from dotenv import load_dotenv
from scraper import QuotesScraper
from saving import JsonResultsSaver


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

load_dotenv()

input_url = os.getenv('INPUT_URL')
output_file = os.getenv('OUTPUT_FILE')

        'username': usr,
        'password': pswrd
}

async def main():
    results_saver = JsonResultsSaver(output_file)

    scraper = QuotesScraper(
                        input_url=input_url,
                        results_saver=results_saver)
    await scraper.scrape_all_pages()

if __name__ == '__main__':
    asyncio.run(main())
