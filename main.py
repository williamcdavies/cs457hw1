# Written by William Chuter-Davies

import csv

from playwright.sync_api import sync_playwright

# read `input.csv` into a list of dicts (`lst`)
# taken in part from https://docs.python.org/3/library/csv.html#csv.DictReader
with open('input.csv', newline='') as f:
    rdr = csv.DictReader(f)
    lst = list(rdr)

# for all dicts in 'lst' whose content is matchable to at least one table 
# row, insert the key-value pairs ('final_schedule', (string)) and ('fina
# l_time', (string)) where ('final_schedule', (string)) is the stripped c
# aption belonging to the first matchable table and ('final_time', (strin
# g)) is the stripped third table data cell belonging to the first matcha
# ble row
# taken in part from https://playwright.dev/python/docs/library#usage
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.goto("https://www.unr.edu/admissions/records/academic-calendar/finals-schedule")
    
    tables = page.locator("table")

    for i in range(tables.count()):
        tables = tables.nth(i)
        caption = tables.locator("caption").inner_text().strip().split(',')[0]
        trs = tables.locator("tr")

        for j in range(trs.count()):
            tr = trs.nth(j)
            td = tr.locator("td")

            if td.count() != 3:
                continue
        
            for item in lst:
                if(item['course_time'] in td.nth(0).inner_text() and 
                   item['course_schedule'] in td.nth(1).inner_text()):
                    item["final_time"] = td.nth(2).inner_text().strip()
                    item["final_schedule"] = caption
                    break
    
    browser.close()

# write `lst` into `output.csv`
# taken in part from https://docs.python.org/3/library/csv.html#csv.DictWriter
with open('output.csv', 'w', newline='') as f:
    fieldnames = ['course_code', 'course_title', 'course_schedule', 'course_time', 'final_schedule', 'final_time']
    wtr = csv.DictWriter(f, fieldnames=fieldnames)
    wtr.writeheader()
    for item in lst:
        wtr.writerow(item)