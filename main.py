import csv

from playwright.sync_api import sync_playwright

with open('input.csv', newline='') as f:
    rdr = csv.DictReader(f)
    lst = list(rdr)

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.unr.edu/admissions/records/academic-calendar/finals-schedule")
    
    tr_locator = page.locator("tr")

    for n in range(tr_locator.count()):
        nth_tr_locator = tr_locator.nth(n)
        td_locator = nth_tr_locator.locator("td")
        
        if td_locator.count() != 3:
            continue
        
        for item in lst:
            if(item['course_start_time'] in td_locator.nth(0).inner_text().strip() and item['course_schedule'] in td_locator.nth(1).inner_text().strip()):
                print(td_locator.nth(2).inner_text().strip())
    
    browser.close()