import { test } from '@playwright/test';

const URL = 'file:///C:/Users/techai/PKA%20testing/Owner\'s%20Inbox/ai_army_architecture_v3.html';
const OUT  = 'C:/Users/techai/PKA testing/';

test('hardware map', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 900 });
  await page.goto(URL);
  await page.waitForTimeout(2000);
  const el = page.locator('.section').nth(1); // hardware section (0=stack, 1=hw)
  await el.screenshot({ path: OUT + 'tmp_v3_hw.png' });
});

test('agent army', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 900 });
  await page.goto(URL);
  await page.waitForTimeout(2000);
  const el = page.locator('.section').nth(3);
  await el.screenshot({ path: OUT + 'tmp_v3_agents.png' });
});

test('flywheel', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 900 });
  await page.goto(URL);
  await page.waitForTimeout(3000);
  const el = page.locator('.section').nth(6);
  await el.screenshot({ path: OUT + 'tmp_v3_flywheel.png' });
});

test('patent strip', async ({ page }) => {
  await page.setViewportSize({ width: 1400, height: 200 });
  await page.goto(URL);
  await page.waitForTimeout(2000);
  const el = page.locator('.patent-strip');
  await el.screenshot({ path: OUT + 'tmp_v3_patent.png' });
});
