// Full-page JPEG of storyboard.html (for sharing the sheet as one image)
let pw;
try { pw = require("playwright"); } catch (e) { pw = require("/opt/node-tools/node_modules/playwright"); }
(async () => {
  const [src, out, width] = process.argv.slice(2);
  const browser = await pw.chromium.launch();
  const page = await browser.newPage({ viewport: { width: Number(width || 1600), height: 1000 } });
  await page.goto("file://" + src);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(300);
  await page.screenshot({ path: out, type: "jpeg", quality: 82, fullPage: true });
  await browser.close();
})();
