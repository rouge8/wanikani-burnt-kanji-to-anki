import csv as _csv
import io

import attrs
import click

from wanikani_burnt_kanji_to_anki.wanikani import WaniKaniAPIClient


@attrs.frozen
class Context:
    api: WaniKaniAPIClient


@click.group()
@click.option("--wanikani-api-key", envvar="WANIKANI_API_KEY", required=True)
@click.version_option()
@click.pass_context
def cli(ctx: click.Context, wanikani_api_key: str) -> None:
    ctx.obj = Context(api=WaniKaniAPIClient(wanikani_api_key))

    ctx.obj.api.load_kanji()


@cli.command()
@click.argument("output", type=click.File("w"), default="-")
@click.pass_context
def csv(ctx: click.Context, output: io.TextIOWrapper) -> None:
    """
    Write your burnt Kanji to a CSV suitable for import by Anki

    Columns are "kanji", "meanings", "readings".
    """
    writer = _csv.writer(output)

    for kanji in ctx.obj.api.burnt_kanji():
        row = (
            kanji.characters,
            ", ".join(kanji.meanings),
            ", ".join(kanji.readings),
        )
        writer.writerow(row)


if __name__ == "__main__":
    cli()
