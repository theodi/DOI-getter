# neil majithia
# 10/04/25
# script to read every pdf within parent directory, read its outbound hyperlinks,
# and get best-match DOIs from crossref. Facilitates updating old outputs to reference
# DOIs, as requested by crossref team.
# note: human validation is required. margin of error is high, although it's only false positives rather than 
# false negatives.
# requires PyPDF2, tqdm, pandas

import PyPDF2
import requests
import os
import urllib.parse
import tqdm
import pandas as pd
import glob


PDF_path_list = glob.glob('*.pdf')
directory_name = 'DOI_spreadsheets'

def doi_from_url(url):
    headers = {
        'User-Agent': 'ODI_ref2doi_script/1.0 (mailto:neil.majithia@theodi.org)'
    }
    
    encoded_url = urllib.parse.quote(url, safe='')
    
    api_url = f'https://api.crossref.org/works?query={encoded_url}&rows=1'
    
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        items = data.get('message', {}).get('items', [])
        
        if items:
            best_match = items[0]
            doi = best_match.get('DOI')
            title = best_match.get('title')
            author = best_match.get('author')[0]['family']
            message = f'Best match DOI: https://www.doi.org/{doi}; title: {title}; author surname: {author}'
            # print(f'URL: {url}')
            # print(message)
            # print()
        else:
            print(f'URL: {url}\n  No matches found.\n')
    else:
        print(f'URL: {url}\n  Request failed with status code {response.status_code}.\n')

    return message

def main(PDF_path):
    current_links = {}
    potential_dois = {}
    with open(PDF_path, 'rb') as file:
        pdf = PyPDF2.PdfReader(file)
        
        for page_num in tqdm.tqdm(range(len(pdf.pages))):
            # print(page_num)
            page = pdf.pages[page_num]
            # print(page)
            current_links[page_num] = []
            potential_dois[page_num] = []
            try:
                annotations = page['/Annots']
                # print(annotations)
                for annot in annotations:
                    # print(annot.get_object()['/A'])
                    hyperlink = annot.get_object()['/A'].get_object()['/URI']
                    # print(hyperlink)
                    current_links[page_num].append(hyperlink)
                    potential_dois[page_num].append(doi_from_url(hyperlink))
            except:
                pass



    col1 = []
    col2 = []
    col3 = []
    for i in current_links:
        for j in range(len(potential_dois[i])):
            col1.append(i)
            col2.append(current_links[i][j])
            col3.append(potential_dois[i][j])

    
    df = pd.DataFrame(data={
    'Page Number': col1,
    'URL in document': col2,
    'Best match DOI information': col3
    })

    df.to_csv(os.path.join(directory_name, f'DOIs_{PDF_path.rstrip(".pdf")}.csv'))
    return df


if __name__ == '__main__':
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
    for PDF_path in PDF_path_list:
        print('Processing: ', PDF_path)
        main(PDF_path)