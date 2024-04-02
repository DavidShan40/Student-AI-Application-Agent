import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm


# program
programs = []
num_sub_page = 23
# URL to crawl
url = 'https://future.utoronto.ca/academics/undergraduate-programs/'

# Send a GET request to the URL
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

for i in tqdm(range(1,num_sub_page+1)):
    if i == 1:
        response = requests.get(url, headers=headers)
    else:
        response = requests.get(url+"?sf_paged="+str(i), headers=headers)
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the content of the page with BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # print(soup)
        # with open('soup_content.txt', 'w', encoding='utf-8') as file:
        #     file.write(str(soup))
        program_links = soup.find_all('a', class_='program-link')
        for link in program_links:
            program_name = link.text
            program_url = link['href']
            programs.append((program_name, program_url))
    else:
        print(f'Failed to retrieve the web page. Status code: {response.status_code}')

df = pd.DataFrame(programs)
df.columns = ['Program_Name','URL']
csv_file_path = 'University_of_Toronto.csv'
df.to_csv(csv_file_path, index=False)
print(df)
# csv_file_path = 'University_of_Waterloo.csv'
# # Find the index for 'Accounting and Financial Management'
# start_index = df[df['Program_Name'] == 'Accounting and Financial Management'].index
# # Find the index for 'Therapeutic Recreation'
# end_index = df[df['Program_Name'] == 'Therapeutic Recreation'].index
# if not start_index.empty and not end_index.empty:
#     # Slice the DataFrame to only include rows between the two indices
#     # Add 1 to end_index because slicing is exclusive on the end
#     df = df.loc[start_index[0]:end_index[0]+1]
# else:
#     print("Start or end program name not found.")
# df.to_csv(csv_file_path, index=False)
# for name, url in programs:
#     print(f"Program: {name}, URL: {url}")