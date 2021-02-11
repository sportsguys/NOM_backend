import click, subprocess
import server.app as app

@click.command()
def start_server():
    subprocess.run(['docker-compose','up','-d'])
    app.start()