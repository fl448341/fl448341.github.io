import requests
from bs4 import BeautifulSoup
import os
from duckduckgo_search import DDGS

def scrape_openings():
    response = requests.get('https://www.thechesswebsite.com/chess-openings/')
    soup = BeautifulSoup(response.text, 'html.parser')
    openings = soup.find_all('div', id='cb-container')[1].find_all('a')
    
    output_folder = 'pages'
    os.makedirs(output_folder, exist_ok=True)

    openings_list = []

    for opening in openings:
        try:
            name = opening.find('h5').text.strip()
            link = opening.get('href')
            img_link = opening.find('img').get('src')
            
            slug = name.replace("'", "").replace(" ", "-").lower()
            folder_path = os.path.join(output_folder, slug)
            os.makedirs(folder_path, exist_ok=True)

            desc = sub_page(name).replace('"', "'").replace("\n", " ")

            content = f"""---
layout: default
title: "{name}"
permalink: /{slug}/
---

### {name}

![{name}]({img_link})

{desc}

[Original article]({link})
"""
            with open(os.path.join(folder_path, "index.md"), "w", encoding='utf-8') as f:
                f.write(content)
                
            openings_list.append(name)

        except Exception as e:
            print(f"Error processing {name}: {str(e)}")
            continue

    return openings_list

def generate_index(openings_list):
    with open("index.md", "w", encoding="utf-8") as f:
        f.write("""---
layout: default
title: "Chess Openings"
permalink: /
---

<div style="
  column-count: 5;
  column-gap: 1.5em;
  column-fill: balance;
  -webkit-column-count: 5;
  -webkit-column-gap: 1.5em;
  -webkit-column-fill: balance;
  -moz-column-count: 5;
  -moz-column-gap: 1.5em;
  -moz-column-fill: balance;
">
<ul>
""")
        for name in openings_list:
            slug = name.replace("'", "").replace(" ", "-").lower()
            # Generujemy element <li>
            f.write(f"  <li><a href='/{slug}/'>{name}</a></li>\n")

        f.write("""</ul>
</div>
""")

def sub_page(opening_name):
    try:
        result = DDGS().chat(
            f"Briefly describe {opening_name} chess opening (1 paragraph, include first 3-5 moves)",
            model='claude-3-haiku'
        )
        return result
    except Exception as e:
        return f"Description unavailable. Error: {str(e)}"

if __name__ == "__main__":
    openings = scrape_openings()
    generate_index(openings)
    print("Generation completed!")
