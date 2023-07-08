import asyncio
from playwright.async_api import async_playwright


class QuotesScraper:
    def __init__(self, input_url, results_saver):
        self.input_url = input_url
        self.results_saver = results_saver
        self.all_quotes = []

    async def get_quotes(self, page):
        await page.wait_for_selector('#quotesPlaceholder .quote')

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

    async def scrape_single_page(self, page):
        await self.get_quotes(page)
        next_page = await page.query_selector('nav .next a')
        if next_page:
            await asyncio.gather(page.click('nav .next a'))
            await self.scrape_single_page(page)

    async def scrape_all_pages(self):
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page()

            await page.goto(self.input_url)
            await self.scrape_single_page(page)

            await browser.close()
            self.results_saver.save_results(self.all_quotes)
