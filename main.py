import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import os
import time
'''
scrape jobs from the list and look for data analyst
'''


class SraperBot:
    def __init__(self):

        self.today = date.today()
        self.file_name = f"hyd_data_jobs_{self.today}.csv"

    def sagility_health(self, job):
        link = 'https://career.sagilityhealth.com/in/en/current-openings?search_job=&locations%5B%5D=103'

        # -------------------- initialize requests --------------------
        response = requests.get(link)
        # -------------------- initialize bs4 --------------------
        soup = BeautifulSoup(response.text, "html.parser")

        data = []

        rows = soup.find_all("tr")
        for row in rows:
            cols = row.find_all("td")
            if len(cols) >= 6:
                job_title = cols[0].get_text(strip=True)
                location = cols[1].get_text(strip=True)
                job_id = cols[2].get_text(strip=True)
                openings = cols[3].get_text(strip=True)
                date_posted = cols[4].get_text(strip=True)

                links = [a['href'] for a in cols[5].find_all("a", href=True)]
                view_link = links[0] if links else None
                apply_link = links[1] if len(links) > 1 else None

                job_link = f'https://career.sagilityhealth.com/in/en/current-openings/{job_id}'

                # ✅ Filter only Hyderabad jobs
                if "Hyderabad" in location and job in job_title.lower():
                    # print(f"Job Title : {job_title}")
                    # print(f"Location  : {location}")
                    # print(f"Job ID    : {job_id}")
                    # print(f"Openings  : {openings}")
                    # print(f"Date      : {date_posted}")
                    # print(f"View More : {view_link}")
                    # print(f"Job Link  : {job_link}")
                    # print(f"Apply Now : {apply_link}")

                    data.append({
                        "Date": self.today,
                        "Job Title": job_title,
                        "Location": location,
                        "Job ID": job_id,
                        "Openings" :openings,
                        "Post Date":date_posted,
                        "View More" :view_link,
                        "Job Link" :job_link,
                        "Apply Now":apply_link
                    })

                    # new_row = pd.DataFrame([{
                    #     "Date": self.today,
                    #     "Job Title": job_title,
                    #     "Location": location,
                    #     "Job ID": job_id,
                    #     "Openings" :openings,
                    #     "Post Date":date_posted,
                    #     "View More" :view_link,
                    #     "Job Link" :job_link,
                    #     "Apply Now":apply_link}])
                    #
                    # try:
                    #     new_row.to_csv(self.file_name, mode="a", index=False, header=False)
                    #     print("# sagility health: append mode")
                    # except FileNotFoundError:
                    #     new_row.to_csv(self.file_name, index=False)
                    #     print("# sagility health: file doesn’t exist yet → create with header")

        df = pd.DataFrame(data)

        if not df.empty:
            if os.path.exists(self.file_name):
                # Read existing file
                existing = pd.read_csv(self.file_name)

                # Combine old + new
                combined = pd.concat([existing, df], ignore_index=True)

                # Drop duplicates based on Job Link
                combined.drop_duplicates(subset=["Job Link"], inplace=True)

                # Save back
                combined.to_csv(self.file_name, index=False)
                print(f"# sagility: merged {len(df)} new rows → total {len(combined)} (deduplicated)")
            else:
                df.to_csv(self.file_name, index=False)
                print("# sagility: file created")
        else:
            print("# sagility: no matching jobs found")

        print(f"Excel file created sagility health {self.today}")

    def deloitte(self, job):
        link = 'https://southasiacareers.deloitte.com/go/Deloitte-India/718244/?q=&q2=&alertId=&locationsearch=&title=&location=Hyderabad&date='

        # -------------------- initialize requests --------------------
        response = requests.get(link)
        # -------------------- initialize bs4 --------------------
        soup = BeautifulSoup(response.text, "html.parser")

        data = []

        for row in soup.find_all("tr", class_="data-row"):
            title = row.find("a", class_="jobTitle-link").get_text(strip=True)
            location = row.find("td", class_="colLocation").get_text(strip=True)
            date = row.find("td", class_="colDate").get_text(strip=True)
            link_tag = row.find("a", class_="jobTitle-link")

            link = link_tag["href"]  # get href attribute

            # Filter by location and title
            if "hyderabad, in" in location.lower() and job in title.lower():
                # print(f"Title: {title}")
                # print(f"Location: {location}")
                # print(f"Date: {date}")
                # print("-" * 40)

                data.append({
                    "Date": self.today,
                    "Job Title": title,
                    "Location": location,
                    "Job ID": "",
                    "Openings": "",
                    "Post Date": date,
                    "View More": "",
                    "Job Link": f"https://southasiacareers.deloitte.com/{link}",
                    "Apply Now": ""
                })

                # new_row = pd.DataFrame([{
                #     "Date": self.today,
                #     "Job Title": title,
                #     "Location": location,
                #     "Job ID": "",
                #     "Openings": "",
                #     "Post Date": date,
                #     "View More": "",
                #     "Job Link": f"https://southasiacareers.deloitte.com/{link}",
                #     "Apply Now": ""}])

                # try:
                #     new_row.to_csv(self.file_name, mode="a", index=False, header=False)
                #     print("# deloitte: append mode")
                # except FileNotFoundError:
                #     new_row.to_csv(self.file_name, index=False)
                #     print("# deloitte: file doesn’t exist yet → create with header")

        df = pd.DataFrame(data)

        if not df.empty:
            if os.path.exists(self.file_name):
                # Read existing file
                existing = pd.read_csv(self.file_name)

                # Combine old + new
                combined = pd.concat([existing, df], ignore_index=True)

                # Drop duplicates based on Job Link
                combined.drop_duplicates(subset=["Job Link"], inplace=True)

                # Save back
                combined.to_csv(self.file_name, index=False)
                print(f"# deloitte: merged {len(df)} new rows → total {len(combined)} (deduplicated)")
            else:
                df.to_csv(self.file_name, index=False)
                print("# deloitte: file created")
        else:
            print("# deloitte: no matching jobs found")

        print(f"Excel file created deloitte {self.today}")

    def run(self):
        keywords = ['data analyst', 'associate analyst']    # ENTER TEXTS HERE
        for i in list(keywords):
            self.deloitte(i)
            time.sleep(3)  # sleeps for 3 seconds
            self.sagility_health(i)
            time.sleep(3)  # sleeps for 3 seconds


sb = SraperBot()
if __name__ == "__main__":
    sb.run()
