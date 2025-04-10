# DOI-getter
For us to have DOIs for our work, Crossref requires us to reference other people's work via their DOIs rather than the typical ODI format, which is simple hyperlinking. For all of the >100 ODI published outputs, this is a big task which involves finding each reference, finding its corresponding DOI, and rewriting the reference to point to that DOI.

The script in this repo does the first two steps of that process. Download it and move it into a directory with a list of PDFs and run the script to, per PDF,:
1. Read each link's corresponding URL
2. Query the crossref API to find the link's best-match corresponding DOI
3. Create a .csv file with each link, its corresponding DOI, and the page it is on. This csv can be used as a basis to update the references in that PDF.

NOTE: it doesn't edit the PDFs - a person has to do that via a google doc
NOTE: false positive rate = 25% ; false negative rate = 0%. human validation of each DOI required.
NOTE: Python

## Usage Instructions
1. Download/clone this repo to your local machine
2. pip install requirements
3. Move all target PDFs into the repo on your local machine
4. Run the script, which will create a subdirectory "DOI_spreadsheets" that contains a .csv per PDF





