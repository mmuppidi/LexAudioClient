
import os
import logging
import tempfile
import yaml
import click
from api.session import AudioBotSession
from api.base import Context
from api.authenticator import CognitoAuthenticator

logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s')
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel('DEBUG')

@click.group()
@click.pass_context
def audiobot(ctx):
    config = yaml.load(open('config.yaml'))
    ctx.obj = Context(config=config, logger=LOGGER)
    ctx.obj.tmp_dir = tempfile.mkdtemp()
    ctx.obj.request_audio_file = os.path.join(ctx.obj.tmp_dir, 'request.wav')
    ctx.obj.response_audio_file = os.path.join(ctx.obj.tmp_dir, 'response.mpeg')
    ctx.obj.authenticator = CognitoAuthenticator(ctx.obj)

@audiobot.command()
@click.pass_obj
def start(ctx):
    bot_session = AudioBotSession(ctx)
    bot_session.start()

cli = click.CommandCollection(sources=[audiobot])

if __name__ == '__main__':
    cli()