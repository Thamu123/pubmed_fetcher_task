# PubMed Fetcher

A Python tool to fetch PubMed articles with pharma/biotech company affiliations.


## 🚀 How to Use (Step-by-Step)

### 🔹 Step 1: Set up environment

Install Poetry (if not already):

curl -sSL https://install.python-poetry.org | python3 -

poetry new pubmed_fetcher_task --src
cd pubmed_fetcher_task

## Intalling requirements
poetry add requests pandas

## Managing Modules and command lines
created core.py file, where defined,
    1.get_pubmed_ids()  ---> Get pubmed_ids from PubMed api by esearch query passed
    2.fetch_details()   ---> Get Article details from pubmed_ids by efetch
    3.parse_articles()  ---> Used XML Tree to parse content 
    4.write_to_csv()    ---> Writing the data to CSV file using Pandas

Then, Created cli.py, here defined the main function and 
    --- Defined the command for console
        -h, --help  --> Display usage instructions
        -d, --debug --> Print debug information during execution.
        -f, --file  --> Specify the filename to save the results.

## added this command in pyproject.toml for executable command named get-papers-list
    [tool.poetry.scripts]
    get-papers-list = "pubmed_fetcher_task.cli:main"

### To Check the Output run the command
poetry install
poetry run get-papers-list "covid vaccine" --file results.csv 


## After Try to create testPypi account
    1. complete the setup
    2. create the api token

### Run the command to build the project
poetry build
 --it will create the dist.

### install twine to upload the repository
poetry add --dev twine

### Run the command for upload the repository to testpypi
poetry run twine upload --repository testpypi dist/*

### If need Pytest run below command it will install the dependency
poetry add --dev pytest

### After run pytest
poetry run pytest

### need to create virtual Environment
python -m venv testenv --- creating virutal environment 
venv/bin/activate
pip install --index-url https://test.pypi.org/simple/ pubmed_fetcher_thamu


### Finally git initialization and Git commit
git init
git remote add origin https://github.com/yourusername/pubmed_fetcher_task.git
git add .
git commit -m "Final version for task-home task"
git push -u origin main


🔗 Link to your GitHub repo
https://github.com/Thamu123/pubmed_fetcher_task

🔗 Link to TestPyPI package 
https://test.pypi.org/project/pubmed-fetcher-task

🤖 Used LLMs (ChatGPT, Copilot)
https://chatgpt.com/share/686ca263-891c-800b-8cea-e53c05d30275



##########################################################################
## 🔧 How to Install and Test This Package from TestPyPI

### Step 1: Create a virtual environment

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Then, run this command
pip install --extra-index-url https://pypi.org/simple/ --index-url https://test.pypi.org/simple/ pubmed_fetcher_thamu

then, 
get-papers-list "covid vaccine" --file results.csv --debug




