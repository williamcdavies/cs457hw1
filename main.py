import csv

with open('in.csv') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        print(', '.join(row))

# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.firefox.launch(headless=True)
#     page = browser.new_page()
#     page.goto("https://www.unr.edu/admissions/records/academic-calendar/finals-schedule")
#     print(page.title())
#     browser.close()