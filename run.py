import asyncio
from dotenv import load_dotenv

from src.scraper import QuotesScraper
from src.saving import JsonResultsSaver
from src import config

load_dotenv()

config.configure_logging()
input_url = config.get_input_url()
output_file = config.get_output_file()
proxy = config.get_proxy()


async def main():
    results_saver = JsonResultsSaver(output_file)

    scraper = QuotesScraper(
                        input_url=input_url,
                        proxy=proxy,
                        results_saver=results_saver)
    await scraper.scrape_all_pages()

if __name__ == '__main__':
    asyncio.run(main())
