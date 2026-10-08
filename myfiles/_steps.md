## Populate Knowledge Base

Here we give main or masterCV latex-file `.tex` to Chatgpt and populate different CV sections as separate `.yaml` files in directory `data/knowledge/`; to be later used by claude to generate customised CV with respect to every application.

## Process Job Description  

We define a general schema/template, `schema/jobRequirements.py`, as a placeholder to get all the necessary job requirements. First, the parser `agents/jobScrapper.py` scrapes the raw-text from the provided job-link; later, the `schema/jobAnalyzer` use the parsed raw-text together with **claude** to transforms and generate the job description based on predefined template `jobRequirements.py`. This is the first use of claude.  
 

## CV Customization
