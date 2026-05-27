import { chromium } from 'playwright-core';

const BASE = 'http://127.0.0.1:4331/';
const OUT = '/tmp/cochon-shots';

const sections = [
  { name: '01-hero',         id: '#hero' },
  { name: '02-gault-millau', id: 'main > section:nth-of-type(2)' },
  { name: '03-esprit',       id: 'main > section:nth-of-type(3)' },
  { name: '04-pate',         id: '#carte' },
  { name: '05-comptoir',     id: 'main > section:nth-of-type(5)' },
  { name: '06-specialites',  id: '#specialites' },
  { name: '07-transition',   id: '.transition-silence' },
  { name: '08-cave',         id: '.cave-section' },
  { name: '09-avis',         id: 'main > section:nth-of-type(9)' },
  { name: '10-venir',        id: 'main > section:last-of-type' },
  { name: '11-footer',       id: 'footer' },
];

const viewports = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile',  width: 390,  height: 844 },
];

const browser = await chromium.launch({
  executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  headless: true,
  args: ['--no-sandbox', '--disable-dev-shm-usage'],
});

for (const vp of viewports) {
  const ctx = await browser.newContext({
    viewport: { width: vp.width, height: vp.height },
    deviceScaleFactor: 1,
    reducedMotion: 'reduce',
  });
  const page = await ctx.newPage();
  await page.goto(BASE, { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => {
    document.querySelectorAll('.fade-in-up').forEach((el) => el.classList.add('is-visible'));
  });
  await page.waitForTimeout(600);

  await page.screenshot({ path: `${OUT}/${vp.name}-00-full.png`, fullPage: true });
  console.log(`✅ ${vp.name} full page`);

  for (const sect of sections) {
    try {
      const el = await page.$(sect.id);
      if (!el) {
        console.log(`  ⏭️  ${vp.name} ${sect.name} (${sect.id}) not found`);
        continue;
      }
      await el.scrollIntoViewIfNeeded();
      await page.waitForTimeout(400);
      await page.screenshot({ path: `${OUT}/${vp.name}-${sect.name}.png`, fullPage: false });
      console.log(`  · ${vp.name} ${sect.name}`);
    } catch (e) {
      console.log(`  ❌ ${vp.name} ${sect.name}: ${e.message}`);
    }
  }
  await ctx.close();
}
await browser.close();
console.log('Done.');
