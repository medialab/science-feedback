# Science Feedback API

The Science Feedback database stores appearances of fact-checked, science-related claims. Their API allows you to search for appearances within a time range. Secondly, once you have searched for and found the appearances that interest you, you can call the API again to get detailed metadata about each appearance.

This tool helps you call the Science Feedback API and search for appearances. In all cases, you need an API key. You can either provide the API key as an option after the command, or you can store it in a YAML file and provide the path to that file with the option `--config FILE.yml`.

```yaml
---
token: TOKEN
```

## Install

1. Clone this GitHub repository on your computer with `git clone https://github.com/medialab/science-feedback.git`.
2. Create and activate a virtual Python environment (v3.11).
3. Install the requirements with `pip install -r requirements.txt`.
4. Test your install with `src/main.py --help`.

## Search for appearances

To get started, you'll need a set of appearances found in the database. To get these, you'll need to provide a start and end date, written in YYYY-MM-DD format.

```shell
$ python src/main.py appearances --start 2024-01-01 --end 2024-02-01 --outfile 2024_january_appearances.csv --token <TOKEN>
```

From experience calling the database, it seems best to set the end date 1-2 days earlier than the present day.

What does the `appearances` command in the [`src/main.py`](src/main.py) script do?

- Paginates through the database's results
- Parses the appearance URL's domain name
- Reformats the date (`2024-01-18T14:48:03Z` becomes `2024-01-18T14:48:03+00:00`)
- Flattens and writes each appearance to a row in the out-file CSV with the following data fields:
  - `id` : unique ID of the appearance
  - `urlContentId` : ID appearance's content, which can be shared by multiple appearances
  - `publishedDate` : the review's publication date
  - `updatedDate` : the last time the review was updated
  - `url` : the URL of the appearance whose content was fact-checked
  - `domain` : the parsed domian name of the appearance's URL
  - `normalizedPublishedDate` : a normalized version of `publishedDate`
  - `normalizedUpdatedDate` : a normalized version of `updatedDate`

## Collect appearances' metadata

Once you have the appearances' IDs, you can call the API again to get detailed metadata about each one.

```shell
$ python src/main.py metadata --infile appearances.csv --outfile enriched_appearances.csv --token <TOKEN>
```

_# This code isn't written yet_
