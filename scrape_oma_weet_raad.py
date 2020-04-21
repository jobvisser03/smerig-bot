#%%
from requests import get
from bs4 import BeautifulSoup
import re
import pandas as pd

# %%
base_url = 'https://omaweetraad.nl/vlekken'

r = get(base_url, allow_redirects=True)
soup = BeautifulSoup(r.content)
vlekken_url_list = soup.find_all('a', attrs={'href': re.compile("^https://omaweetraad.nl/vlekken/")})

# %%
df = pd.DataFrame(columns=['topic', 'topic_url_text', 'url', 'answer'])

for i in range(0, 10):
# for i in range(0, len(vlekken_url_list)):
    vlek = vlekken_url_list[i]
    vlek_url_text = vlek.text.replace(' ', '-').lower()
    url = "https://omaweetraad.nl/vlekken/" + vlek_url_text
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    antwoord_container = html_soup.find_all('div', class_ = 'content')
    try:
        antwoord = antwoord_container[0].p.get_text().replace('\n', ' ')
        df = df.append({'topic': vlek.text, 
                    'topic_url_text': vlek_url_text, 
                    'url': url, 
                    'answer': antwoord}
                    , ignore_index=True)
    except:
        pass

# %%
responses_filename = "data/responses.md"
nlu_filename = "data/nlu.md"
base_nlu_filename = "data/base_nlu.md"

base_nlu_file = open(base_nlu_filename, "r")
base_intents = base_nlu_file.read()

#%%

with open(responses_filename, "w") as f_responses:
    with open(nlu_filename, "w") as f_intent:
        f_intent.write(base_intents + "\n\n")
        for index, row in df.iterrows():
            f_responses.write("## ask " + row.topic_url_text + "\n")
            f_responses.write("* faq/ask_" + row.topic_url_text + "\n")
            f_responses.write("  - " + row.answer + "\n\n")
            
            f_intent.write("## intent: faq/ask_" + row.topic_url_text + "\n")
            f_intent.write("- " + row.topic + "\n\n")



# %%
df.to_pickle('data/qna_dataframe.pickle')


# %%
df.loc[df.topic_url_text=='confettivlekken-verwijderen']

# %%
