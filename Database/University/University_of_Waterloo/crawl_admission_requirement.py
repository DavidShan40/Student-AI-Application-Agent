import requests
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm
import os

file_path = 'University_of_Waterloo.csv'
new_folder = 'University_of_Waterloo/Academic_Programs'
os.makedirs(new_folder, exist_ok=True)
df = pd.read_csv(file_path)
#program_infos = []

def escape_forward_slashes(path):
    """Escapes forward slashes in a path with backslashes."""
    return path.replace("/", "_")

program_name = df['Program_Name']
url = df['URL']
for i in tqdm(range(len(program_name))):
    response = requests.get(url[i])
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        main_content = soup.find('div', class_='content_node')  # Use the actual class that wraps the main content
        file_name = f"{program_name[i]}.txt"
        text = main_content.get_text()
        file_path = os.path.join(new_folder, escape_forward_slashes(file_name))
        print(file_path)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(text)

# # Add the information as a new column to the DataFrame
# df['Program Information'] = program_infos

# # Save the updated DataFrame to a new CSV file in the same directory
# df.to_csv(file_path, index=False)