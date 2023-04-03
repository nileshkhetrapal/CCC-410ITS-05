import os
import re
import requests
import pandas as pd
from bs4 import BeautifulSoup

url = "https://samples.vx-underground.org/samples/Families/"
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, "html.parser")

family_links = [a["href"] for a in soup.find_all("a", href=True) if re.match(r'https://samples.vx-underground.org/samples/Families/[\w-]+/', a["href"])]

data = []
download_path = os.getcwd()

for family_link in family_links:
    family_name = family_link.split('/')[-2]
    print(f'Downloading files for {family_name}...')
    family_html_content = requests.get(family_link).text
    family_soup = BeautifulSoup(family_html_content, "html.parser")
    
    sample_links = [a["href"] for a in family_soup.find_all("a", href=True) if a["href"].endswith(".7z")]

    for sample_link in sample_links:
        sample_name = sample_link.split('/')[-1]
        
        family_path = os.path.join(download_path, family_name)
        if not os.path.exists(family_path):
            os.makedirs(family_path)
        file_path = os.path.join(family_path, sample_name)

        if not os.path.exists(file_path):
            try:
                response = requests.get(sample_link, stream=True)
                with open(file_path, "wb") as f:
                    f.write(response.content)
            except Exception as e:
                print(f"Error downloading {sample_name}: {e}")
                continue

        data.append({"family": family_name, "sample": sample_name})

df = pd.DataFrame(data)
df.to_csv("samples_and_families.csv", index=False)
