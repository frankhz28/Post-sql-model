import typer

from .service import run_all, run_tags, run_users


app = typer.Typer(help="Seeds: users, tags")

@app.command("users")
def users():
    run_users()
    typer.echo("Usuarios cargados")

@app.command("tags")
def tags():
    run_tags()
    typer.echo("Etiquetas cargadas")


@app.command("all")
def all_():
    run_all()
    typer.echo("Todos los sedds cargadas")