"""Optional live browser smoke test; run manually from project root."""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True, executable_path='/usr/bin/chromium', args=['--no-sandbox'])
    page = browser.new_page(viewport={'width': 1280, 'height': 900})
    errors=[]
    page.on('pageerror', lambda err: errors.append(str(err)))
    page.goto('http://127.0.0.1:8765', wait_until='networkidle')
    assert page.locator('#topic-grid .topic-card').count() == 6
    page.locator('.mode-card[data-mode="hard"]').click()
    assert page.locator('.mode-card[data-mode="hard"]').get_attribute('aria-pressed') == 'true'
    page.locator('.topic-card').first.click()
    assert page.locator('#mode-select').input_value() == 'hard'
    assert page.locator('.question-meta').inner_text().startswith('HARD MODE')
    for i in range(4):
        page.locator('.option').first.click()
        page.locator('.feedback').wait_for()
        assert page.locator('.feedback p').inner_text()
        page.locator('.next-row button').click()
    assert 'Hard mode complete' in page.locator('.question-prompt').inner_text()
    page.locator('#mode-select').select_option('medium')
    assert page.locator('.question-meta').inner_text().startswith('MEDIUM MODE')
    page.locator('.option').nth(1).click()
    page.locator('.feedback').wait_for()
    page.locator('[data-route="insights"]').click()
    assert 'Not attempted' not in page.locator('#hard-performance').inner_text()
    assert 'Not attempted' not in page.locator('#medium-performance').inner_text()
    page.locator('[data-route="overview"]').click()
    page.screenshot(path='/mnt/data/daybreak_modes_desktop.png', full_page=True)
    page.set_viewport_size({'width': 390, 'height': 844})
    page.screenshot(path='/mnt/data/daybreak_modes_mobile.png', full_page=True)
    assert not errors, errors
    print('BROWSER SMOKE: Passed; difficulty choice, hard questions, explanations, completion, mode switch, insights, no JS errors')
    browser.close()
