import requests
from bs4 import BeautifulSoup
import pandas as pd
from mdutils.mdutils import MdUtils
from duckduckgo_search import DDGS
import duckduckgo_search
import os
import time

def scrape_openings():
    response = requests.get('https://www.thechesswebsite.com/chess-openings/')
    soup = BeautifulSoup(response.text, 'html.parser')
    openings = soup.find_all('div', id = 'cb-container')[1].find_all('a')
    openings_dict = {
        'Name': [],
        'Position': []
    }
    output_folder = 'pages'
    os.makedirs(output_folder, exist_ok=True)
 
        
    for opening in openings:
        name = opening.find('h5').text
        link = opening.get('href')
        img_link = opening.find('img').get('src')
        
        slug = name.replace(" ", "_").lower()
        local_link = f"pages/{slug}.html"
        desc = sub_page(name)
        content = (
            f"---\n"
            f"title: \"{name}\"\n"
            f"layout: default\n"
            f"description: \"{desc}\"\n"
            f"---\n\n"
            f"# {name}\n\n"
            f"![{name} Image]({img_link})\n\n"
            f"{desc}\n\n"
            f"[More]({link})\n"
        )
        
        filename = f"{slug}.md"
        filepath = os.path.join(output_folder, filename)
        with open(filepath, "w", encoding='utf-8') as f:
            f.write(content)
        
        
        openings_dict['Name'].append(f'[{name}]({local_link})')
        openings_dict['Position'].append(f'![]({img_link})')

    openings_df = pd.DataFrame.from_dict(openings_dict)
    
    return openings_df
    
def openings_markdown(openings_df):
    mdFile = MdUtils(file_name='index')

    mdFile.new_header(level=1, title='Chess Openings')
    
    openings_df.index += 1
    markdown_table = openings_df.to_markdown()
    mdFile.new_paragraph(markdown_table)

    mdFile.create_md_file()
    
    

    
def sub_page(opening_name):
    retries = 1
    for attempt in range(retries):
        try:
            return DDGS().chat(
                f"Write a description of a given chess opening: {opening_name}. I want you to write it in one paragraph, include first 5 moves for whites and blacks of this opening.",
                model='claude-3-haiku'
            )
        except duckduckgo_search.exceptions.RatelimitException as e:
            print(f"Rate limit reached for '{opening_name}', attempt {attempt+1}/{retries}. Retrying in 10 seconds...")
            time.sleep(1)
    return f"Description for {opening_name} is not available due to rate limit."

openings_markdown(scrape_openings())
