import click
import uvicorn


@click.group()
def api():
    pass


@api.command()
@click.option("--host", default="0.0.0.0", help="The API host", show_default=True)
@click.option("--port", default=8000, help="The API port", show_default=True)
@click.option(
    "--reload",
    default=True,
    help="Reload the server when changes are made",
    show_default=True,
)
def start(host, port, reload):
    uvicorn.run(
        "template_project.api.__main__:app",
        host=host,
        port=port,
        reload=reload,
    )
