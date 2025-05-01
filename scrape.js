const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

(async () => {
  // Configure logging
  const log = (message) => console.log(new Date().toISOString() + ' - INFO - ' + message);
  const logError = (message) => console.error(new Date().toISOString() + ' - ERROR - ' + message);

  const searchQuery = process.argv[2] || 'iphones'; // Default search term or get from command line
  const maxPages = 2;
  const baseUrl = 'https://dir.indiamart.com/search.mp';
  const allProducts = [];

  // Launch browser with more debugging
  log('Launching Puppeteer...');
  const browser = await puppeteer.launch({
    headless: false, // Set to false for visible browser to debug
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-blink-features=AutomationControlled'],
    defaultViewport: null, // Use full page size
    slowMo: 50, // Slow down operations for debugging (optional)
  });

  const page = await browser.newPage();

  // Set user agent and additional headers to mimic a real browser
  await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36');
  await page.setExtraHTTPHeaders({
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
  });

  let pageNumber = 1;

  while (pageNumber <= maxPages) {
    try {
      log(`Scraping page ${pageNumber}...`);

      // Navigate to the search page with extended wait
      const searchParams = new URLSearchParams({ ss: searchQuery.replace(' ', '+') });
      const url = `${baseUrl}?${searchParams.toString()}`;
      await page.goto(url, { 
        waitUntil: 'domcontentloaded', // Wait until DOM is fully loaded
        timeout: 30000 // Increase timeout to 30 seconds
      });

      // Wait for products with a longer timeout and fallback
      try {
        await page.waitForSelector('div.prd-card-simple', { timeout: 20000 }); // Increased to 20 seconds
      } catch (e) {
        logError(`Selector 'div.prd-card-simple' not found after 20s. Taking screenshot for debugging.`);
        await page.screenshot({ path: `debug_page_${pageNumber}.png` }); // Save screenshot for debugging
        throw e; // Re-throw to handle in outer catch
      }

      // Extract products
      const products = await page.$$eval('div.prd-card-simple', (elements) => 
        elements.map(product => {
          return {
            name: product.querySelector('.prd-name')?.textContent.trim() || null,
            price: product.querySelector('.prc.cur')?.textContent.trim() || null,
            min_order: product.querySelector('.moq')?.textContent.replace('Min. Order: ', '').trim() || null,
            supplier: product.querySelector('.comp-name a')?.textContent.trim() || null,
            supplier_url: product.querySelector('.comp-name a')?.href || null,
            rating: product.querySelector('.rtg-val')?.textContent.trim() || null,
            location: product.querySelector('.loc')?.textContent.trim() || null,
            product_url: product.querySelector('a.prd-name')?.href || null,
          };
        })
      );

      allProducts.push(...products);
      log(`Scraped ${products.length} products from page ${pageNumber}`);

      // Check for next page
      const nextButton = await page.$('a[rel="next"]');
      if (!nextButton) {
        log('No next page found.');
        break;
      }

      // Click next button and wait for navigation
      await Promise.all([
        page.waitForNavigation({ waitUntil: 'domcontentloaded', timeout: 30000 }),
        nextButton.click(),
      ]);

      pageNumber++;
      await new Promise(resolve => setTimeout(resolve, randomIntFromInterval(3000, 5000))); // Increased random delay

    } catch (e) {
      logError(`Error on page ${pageNumber}: ${e.message}`);
      break;
    }
  }

  // Save to CSV
  const csvContent = [
    'name,price,min_order,supplier,supplier_url,rating,location,product_url',
    ...allProducts.map(product => 
      Object.values(product).map(value => `"${value || ''}"`).join(',')
    )
  ].join('\n');

  fs.writeFileSync(`indiamart_${searchQuery.replace(' ', '_')}.csv`, csvContent);
  log(`Saved ${allProducts.length} records to indiamart_${searchQuery.replace(' ', '_')}.csv`);

  await browser.close();
  log('Browser closed.');

})();

// Helper function for random delay
function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min);
}