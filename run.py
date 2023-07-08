import asyncio
import os
from dotenv import load_dotenv
from scraper import QuotesScraper
from saving import JsonResultsSaver


load_dotenv()

input_url = os.getenv('INPUT_URL')
output_file = os.getenv('OUTPUT_FILE')


async def main():
    results_saver = JsonResultsSaver(output_file)

    scraper = QuotesScraper(
                        input_url=input_url,
                        results_saver=results_saver)
    await scraper.scrape_all_pages()

if __name__ == '__main__':
    asyncio.run(main())
