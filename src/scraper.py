import asyncio
import logging
from playwright.async_api import async_playwright


class QuotesScraper:
    def __init__(self, input_url, proxy, results_saver):
        self.input_url = input_url
        self.proxy = proxy
        self.results_saver = results_saver
        self.all_quotes = []
        self.logger = logging.getLogger(__name__)

    async def get_quotes(self, page):
        loaded_quotes = page.locator('#quotesPlaceholder')
        await loaded_quotes.wait_for()

        quotes = await page.evaluate('''() => {
                    const quoteElements = Array.from(
                        document.querySelectorAll('#quotesPlaceholder .quote'));
                    return quoteElements.map((quoteElement) => {
                        const text = quoteElement.querySelector('.text')
                            .textContent.replace(/["“”]/g, '');
                        const author = quoteElement.querySelector('.author')
                            .textContent;
                        const tags = Array.from(quoteElement.querySelectorAll(
                            '.tag')).map((tag) => tag.textContent);
                        return { 'text': text, 'by': author, 'tags': tags };
                    });
                }''')

        self.all_quotes.extend(quotes)

    async def scrape_single_page(self, page, page_number):
        self.logger.info('Scraping page %s', page_number)

        await self.get_quotes(page)
        await self.next_page(page, page_number)

    async def next_page(self, page, page_number):
        next_page_button = page.locator('li.next a')

        while await next_page_button.is_visible():
            page_number += 1
            await asyncio.gather(next_page_button.click())

            await self.scrape_single_page(page, page_number)

    async def scrape_all_pages(self):
        async with async_playwright() as playwright:
            page_number = 1

            browser = await playwright.chromium.launch(proxy=self.proxy)
            page = await browser.new_page()

            await page.goto(self.input_url)
            await self.scrape_single_page(page, page_number)

            await browser.close()
            self.logger.info('Scraping finished, saving to file...')
            self.results_saver.save_results(self.all_quotes)
            self.logger.info('Results saved succesfully.')
