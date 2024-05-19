import requests
from bs4 import BeautifulSoup

#스크래핑할 웹사이트 주소
# url = 'https://weworkremotely.com/categories/remote-full-stack-programming-jobs#job-listings'

#웹사이트에서 추출한 구인정보를 저장할 리스트
all_jobs = []

def scrape_page(url):
    print(f"Scrapping {url}...")
    response = requests.get(url)
    soup = BeautifulSoup(
        response.content, 
        "html.parser",
        )
    #웹사이트에서 원하는 정보 추출
    jobs = soup.find(
        "section", class_ = "jobs",
        ).find_all("li")[1:-1]
    #추출한 정보를 딕셔너리에 저장한 후 리스트에 저장
    for job in jobs:
        title = job.find("span", class_ = "title").text
        company = job.find("span", class_ = "company").text
        location = job.find("span", class_ = "region").text
        url = job.find("a")["href"]
        job_data = {"Title": title, "Company": company, "Location": location, "Url": f"https://weworkremotely.com{url}"}
        all_jobs.append(job_data)

#스크래핑할 페이지 수를 구하는 함수
def get_pages(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    return len(soup.find("div", class_ = "pagination").find_all("span", class_ = "page"))

total_pages = get_pages("https://weworkremotely.com/remote-full-time-jobs?page=1")

for i in range(total_pages):
    url = f"https://weworkremotely.com/remote-full-time-jobs?page={i+1}"
    scrape_page(url)

print(len(all_jobs))