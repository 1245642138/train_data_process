from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import time

start_date = datetime(2024, 9, 20)
end_date = datetime(2024, 9, 30)


csv_file = "Train_fault_information_description"
with open(csv_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["date", "text"])

# Selenium 配置（无头模式）
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

total_records = 0
current_date = start_date

while current_date <= end_date:
    date_str = current_date.strftime("%d_%m_%Y")
    url = f"https://trainstats.altervista.org/avvisi.php?data={date_str}"
    print(f"📡 Fetching {date_str} ...")

    try:
        driver.get(url)
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        avvisi = []
        for tag in soup.find_all(["div", "p", "li"]):
            text = tag.get_text(strip=True)
            if text and len(text) > 5:
                avvisi.append(text)

        if avvisi:
            with open(csv_file, "a", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                for item in avvisi:
                    writer.writerow([current_date.strftime("%Y-%m-%d"), item])
            total_records += len(avvisi)

    except Exception as e:
        print(f" Error on {date_str}: {e}")

    current_date += timedelta(days=1)

driver.quit()
Print(f"Completed! A total of {total_records} announcements have been crawled and saved to {csv_file}")
