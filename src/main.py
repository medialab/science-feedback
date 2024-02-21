import csv
from datetime import datetime

import casanova
import click
import requests
import yaml
from rich.progress import MofNCompleteColumn, Progress, TextColumn, TimeElapsedColumn
from ural import get_domain_name

API_RESULTS = "appearances.csv"
ENRICHED_RESULTS = "enriched_appearances.csv"
FORMAT = "%Y-%m-%dT%H:%M:%S%Z"


@click.group()
def cli():
    pass


@cli.command("appearances")
@click.option(
    "--config", required=False, type=click.Path(file_okay=True, dir_okay=False)
)
@click.option("--start", required=True)
@click.option("--end", required=True)
@click.option("--outfile", default=API_RESULTS)
@click.option("--token", required=False)
def request_appearances(config, start, end, outfile, token):
    if not token:
        with open(config, "r") as f:
            c = yaml.safe_load(f)
            token = c["token"]
    page_n = 1
    with open(outfile, "w") as of, Progress(
        TextColumn("{task.description}"),
        TimeElapsedColumn(),
        MofNCompleteColumn(),
    ) as p:
        writer = csv.DictWriter(
            of,
            fieldnames=[
                "id",
                "urlContentId",
                "publishedDate",
                "updatedDate",
                "url",
                "domain",
                "normalizedPublishedDate",
                "normalizedUpdatedDate",
            ],
        )
        writer.writeheader()
        t = p.add_task("Paginating appearances", total=1)
        result_length = 1
        completed = 0
        while result_length > 0:
            endpoint = f"https://api.feedback.org/appearances?page={page_n}&paginator=50&startPublishedDate={start}&endPublishedDate={end}"
            p.update(task_id=t, total=page_n)
            response = requests.get(url=endpoint, headers={"X-Access-Tokens": token})
            completed += 1
            p.update(task_id=t, completed=completed, total=page_n)
            page_n += 1
            results = response.json()
            result_length = len(results)
            for result in results:
                domain = get_domain_name(result["url"])
                published_date = datetime.fromisoformat(
                    result["publishedDate"]
                ).isoformat()
                updated_date = datetime.fromisoformat(result["updatedDate"]).isoformat()
                result.update(
                    {
                        "domain": domain,
                        "normalizedPublishedDate": published_date,
                        "normalizedUpdatedDate": updated_date,
                    }
                )
                writer.writerow(result)


@cli.command("metadata")
@click.option(
    "--config", required=False, type=click.Path(file_okay=True, dir_okay=False)
)
@click.option(
    "--outfile",
    default=ENRICHED_RESULTS,
    type=click.Path(file_okay=True, dir_okay=False),
)
@click.option(
    "--infile", required=True, type=click.Path(file_okay=True, dir_okay=False)
)
@click.option("--token", required=False)
def appearance_metadata(config, outfile, infile, token):
    if not token:
        with open(config, "r") as f:
            c = yaml.safe_load(f)
            token = c["token"]
    with open(infile, "r") as f, open(outfile, "w") as of:
        enricher = casanova.enricher(f, of, add=[])


if __name__ == "__main__":
    cli()
