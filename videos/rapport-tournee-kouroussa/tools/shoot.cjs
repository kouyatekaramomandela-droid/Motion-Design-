// Screenshot static sketch pages listed in a jobs.json file: [{html, png, w, h}]
const fs = require("fs");
let pw;
try { pw = require("playwright"); } catch (e) { pw = require("/opt/node-tools/node_modules/playwright"); }

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
  const browser = await pw.chromium.launch();
  for (const j of jobs) {
    const page = await browser.newPage({ viewport: { width: j.w, height: j.h } });
    await page.goto("file://" + j.html);
    await page.evaluate(() => document.fonts.ready);
    await page.waitForTimeout(150);
    await page.screenshot({ path: j.png, type: "jpeg", quality: 86 });
    await page.close();
  }
  await browser.close();
})();
