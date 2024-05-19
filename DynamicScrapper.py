from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

# playwright 라이브러리를 사용하여 동적 스크래핑
p = sync_playwright().start()

browser = p.chromium.launch(headless=False)

page = browser.new_page()

page.goto("https://www.wanted.co.kr/")

page.click("button.Aside_searchButton__Xhqq3")

time.sleep(1)

page.get_by_placeholder("검색어를 입력해 주세요.").fill("python")

time.sleep(1)

page.keyboard.press("Enter")

time.sleep(1)

page.click("a#search_tab_position")

for _ in range(5):
    time.sleep(1)
    page.keyboard.press("End")

time.sleep(1)

content = page.content()

browser.close()

# BeautifulSoup 라이브러리를 사용하여 잡 리스트 추출
soup = BeautifulSoup(content, "html.parser")

jobs = soup.find_all("div", class_ = "JobCard_container__FqChn")

job_list = []

for job in jobs:
    link = f"https://www.wanted.co.kr{job.find('a')['href']}"
    title = job.find("strong", class_ = "JobCard_title__ddkwM").text
    company = job.find("span", class_ = "JobCard_companyName__vZMqJ").text
    reward = job.find("span", class_ = "JobCard_reward__sdyHn").text
    job = {"Title": title, "Company": company, "Reward": reward, "Link": link}
    job_list.append(job)

print(job_list)
print(len(job_list))

# CSV 파일로 저장
file = open("jobs.csv", "w")
writer = csv.writer(file)
writer.writerow(["Title", "Company", "Reward", "Link"])
for job in job_list:
    writer.writerow(job.values())
file.close()