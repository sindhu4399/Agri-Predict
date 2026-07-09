const puppeteer = require('puppeteer');

(async () => {
  const url = process.env.URL || 'http://localhost:5174';
  const browser = await puppeteer.launch({ headless: true, args: ['--no-sandbox','--disable-setuid-sandbox'] });
  const page = await browser.newPage();
  page.setDefaultTimeout(30000);

  try {
    await page.goto(url);
    await page.waitForSelector('.chat-panel-button');
    await page.click('.chat-panel-button');
    await page.waitForSelector('.chat-panel');
    await page.waitForSelector('.chat-input');

    const question = 'What fertilizer should I use for maize in loam soil?';
    await page.type('.chat-input', question);
    await page.click('.send-btn');

    // Wait for a bot reply to appear
    await page.waitForFunction(() => {
      const msgs = Array.from(document.querySelectorAll('.message-bot'));
      return msgs.some(m => m.innerText && m.innerText.trim().length > 10);
    }, { timeout: 30000 });

    const reply = await page.evaluate(() => {
      const msgs = Array.from(document.querySelectorAll('.message-bot'));
      const last = msgs[msgs.length - 1];
      return last ? last.innerText.trim() : '';
    });

    console.log('BOT_REPLY:', reply);
    await browser.close();

    if (!reply || reply.length < 10) {
      console.error('No meaningful reply received');
      process.exit(2);
    }

    process.exit(0);
  } catch (err) {
    console.error('E2E_TEST_ERROR', err);
    await browser.close();
    process.exit(3);
  }
})();
