from core import ExtensibleContext
from modules import CaseHandler, MediaPlayer, TextBuffer

class DefaultComponentSetup:
    @staticmethod
    def setup(context: ExtensibleContext) -> None:
        context.register_component("text_buffer", TextBuffer())
        context.register_component("media_player", MediaPlayer())
        context.register_component("case_handler", CaseHandler())
