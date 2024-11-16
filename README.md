# J News

## Usage

`python3 translate.py prompt.txt`

Environment variable OPENAI_API_KEY must be set to a valid key.

## TODO
- Choose a few more news sites to scrape from
- The script should do the following:
  - Pull a couple of the most recent articles from each news site (optionally, the AI can choose the most interesting sounding articles)
  - Extract their main content
  - Send to AI to summarize
  - Save summaries to a file or database
- We then construct a webpage where you choose the publication you want to read.
