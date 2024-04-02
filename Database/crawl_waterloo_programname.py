import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL to crawl
url = 'https://uwaterloo.ca/future-students/programs/alpha-list'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the content of the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Look for elements that contain program names - This will depend on the structure of the webpage
    # Below is a hypothetical example and you would need to inspect the actual webpage to use the correct selector
    #print(soup)
    program_links =  soup.find_all('a', href=lambda href: href and ('/future-students/programs/' in href))
    # Extract the program names from the elements
    #program_names = [element.text.strip() for element in program_elements]

    programs_data = []
    for link in program_links:
        program_name = link.get_text()
        program_url = 'https://uwaterloo.ca' + link['href']
        programs_data.append({"Program_Name": program_name, "URL": program_url})
    # use pandas combine above and save to csv

else:
    print(f'Failed to retrieve the web page. Status code: {response.status_code}')

df = pd.DataFrame(programs_data)
csv_file_path = 'University/University_of_Waterloo.csv'
# Find the index for 'Accounting and Financial Management'
start_index = df[df['Program_Name'] == 'Accounting and Financial Management'].index
# Find the index for 'Therapeutic Recreation'
end_index = df[df['Program_Name'] == 'Therapeutic Recreation'].index
if not start_index.empty and not end_index.empty:
    # Slice the DataFrame to only include rows between the two indices
    # Add 1 to end_index because slicing is exclusive on the end
    df = df.loc[start_index[0]:end_index[0]+1]
else:
    print("Start or end program name not found.")
df.to_csv(csv_file_path, index=False)