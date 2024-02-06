from bs4 import BeautifulSoup
import requests
import pandas as pd
import feedparser
import re


def scrape_securitypatch():
    url_securitypatch = 'https://securitypatch.ro/'
    page_securitypatch = requests.get(url_securitypatch)
    soup_securitypatch = BeautifulSoup(page_securitypatch.text, 'html.parser')
    news_securitypatch = soup_securitypatch.find_all('div', class_='td-block-span12')

    data_securitypatch = {'Title': [], 'Published Date': [], 'Description': [], 'Link': []}

    for new in news_securitypatch:
        title_tag = new.find('a')
        title = title_tag.get('title') if title_tag else 'No title available'
        link = title_tag.get('href') if title_tag else 'No link available'

        published_date_tag = new.find('time')
        published_date = published_date_tag.text if published_date_tag else 'No published date available'

        description_tag = new.findNext('div', class_='td-excerpt')
        description = description_tag.text.replace('\r\n', '').replace('\n',
                                                                       '') if description_tag else 'No description available'

        data_securitypatch['Title'].append(title)
        data_securitypatch['Link'].append(link)
        data_securitypatch['Published Date'].append(published_date)
        data_securitypatch['Description'].append(description)

    return pd.DataFrame(data_securitypatch)



def scrape_dnsc():
    url_dnsc = 'https://dnsc.ro/feed'
    feed_dnsc = feedparser.parse(url_dnsc)

    data_dnsc = {'Title': [], 'Link': [], 'Description': []}

    for entry in feed_dnsc.entries:
        title = entry.title
        link = entry.link
        description = entry.summary if hasattr(entry, 'summary') else 'No description available'

        data_dnsc['Title'].append(title)
        data_dnsc['Link'].append(link)
        data_dnsc['Description'].append(description)

    return pd.DataFrame(data_dnsc)


df_securitypatch = scrape_securitypatch()
df_dnsc = scrape_dnsc()
df_combined = pd.concat([df_securitypatch, df_dnsc], ignore_index=True)

# ...

# ...


df_combined['Link'] = df_combined['Link'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')


html_content_combined = f'''
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <style>
    body {{
      font-family: Arial, sans-serif;
    }}
    .styled-table {{
      width: 100%;
      background-color: #f5f5f5;
      border-collapse: collapse;
      margin: 25px 0;
      font-size: 14px;
      text-align: left;
    }}
    .styled-table th, .styled-table td {{
      padding: 12px 15px;
      border-bottom: 1px solid #ddd;
    }}
    .styled-table th {{
      background-color: #008080;
      color: #ffffff;
    }}
    .styled-table tr:hover {{
      background-color: #e0e0e0;
    }}
    .styled-table td a {{
      color: #008080;
      text-decoration: none;
    }}
    .styled-table td a:hover {{
      color: #004040;
      text-decoration: underline;
    }}
  </style>
</head>
<body>
  {df_combined.to_html(index=False, escape=False, classes='styled-table', render_links=True)}
</body>
</html>
'''


with open('output_combined.html', 'w', encoding='utf-8') as html_file_combined:
    html_file_combined.write(html_content_combined)
