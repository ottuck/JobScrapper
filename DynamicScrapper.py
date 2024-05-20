import os
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import time
import csv

# User-Agent 설정
user_agent = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/90.0.4430.85 Safari/537.36")

# playwright 라이브러리를 사용하여 동적 스크래핑
with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(user_agent=user_agent)
    page = context.new_page()

    page.goto("https://www.wanted.co.kr/")
    page.click("button.Aside_searchButton__Xhqq3")
    time.sleep(1)
    page.get_by_placeholder("검색어를 입력해 주세요.").fill("js")
    time.sleep(1)
    page.keyboard.press("Enter")
    time.sleep(1)
    page.click("a#search_tab_position")

    for _ in range(5):
        time.sleep(1)
        page.keyboard.press("End")

    time.sleep(1)
    content = page.content()
    
    # 브라우저 인스턴스 종료
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

print(f"{len(job_list)}개의 채용 정보를 찾았습니다.")

# 파일명 중복 방지
base_filename = "jobs"
file_counter = 1
filename = f"{base_filename}_{file_counter}.csv"

while os.path.exists(filename):
    filename = f"{base_filename}_{file_counter}.csv"
    file_counter += 1

# CSV 파일로 저장
with open(filename, "w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Company", "Reward", "Link"])
    for job in job_list:
        writer.writerow(job.values())

print(f"{filename} 파일로 저장되었습니다.")