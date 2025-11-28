from core import ExtensibleContext
from typing import List, Callable

class KeyboardStatusProvider:
    """Предоставление статуса клавиатуры"""
    
    def __init__(self, context: ExtensibleContext):
        self.context = context
        self._status_providers: List[Callable[[], str]] = []
        self._setup_default_providers()
    
    def _setup_default_providers(self):
        self.register_status_provider(self._get_text_status)
        self.register_status_provider(self._get_caps_status)
        self.register_status_provider(self._get_volume_status)
        self.register_status_provider(self._get_media_status)
    
    def _get_text_status(self) -> str:
        text_buffer = self.context.get_component("text_buffer")
        return f"TEXT: {text_buffer.get_text()}" if text_buffer else "TEXT: N/A"
    
    def _get_caps_status(self) -> str:
        case_handler = self.context.get_component("case_handler")
        return f"CAPS: {'ON' if case_handler.is_upper else 'OFF'}" if case_handler else "CAPS: N/A"
    
    def _get_volume_status(self) -> str:
        media_player = self.context.get_component("media_player")
        return f"VOLUME: {media_player.volume}" if media_player else "VOLUME: N/A"
    
    def _get_media_status(self) -> str:
        media_player = self.context.get_component("media_player")
        return f"MEDIA: {'PLAYING' if media_player.is_playing else 'STOPPED'}" if media_player else "MEDIA: N/A"
    
    def register_status_provider(self, provider: Callable[[], str]) -> None:
        self._status_providers.append(provider)
    
    def get_status(self) -> str:
        status_lines = []
        for provider in self._status_providers:
            status_lines.append(provider())
        return "\n".join(status_lines)
