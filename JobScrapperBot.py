import requests
from bs4 import BeautifulSoup

#스크래핑할 웹사이트 주소
url = 'https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings'
response = requests.get(url)
soup = BeautifulSoup(
    response.content, 
    "html.parser",
    )

#웹사이트에서 원하는 정보 추출
jobs = soup.find(
    "section", class_ = "jobs",
    ).find_all("li")[1:-1]
# print(jobs)

#추출한 정보를 딕셔너리에 저장한 후 리스트에 저장
all_jobs = []
for job in jobs:
    title = job.find("span", class_ = "title").text
    company = job.find("span", class_ = "company").text
    location = job.find("span", class_ = "region").text
    link = job.find("a")["href"]
    job_data = {"Title": title, "Company": company, "Location": location, "Link": link}
    # print(job_data)
    all_jobs.append(job_data)

print(all_jobs)