from core.abstractions import IPlugin
from core.infrastructure.context import ExtensibleContext

from features.status_display import StatusProvider
from features.keybindings import KeyBindingManager


class MediaPlayer(IPlugin):
    def __init__(self):
        self._volume: int = 50
        self._is_playing: bool = False

    def get_name(self) -> str:
        return self.__name__
    
    def setup(self,context: "ExtensibleContext", binding_manager: "KeyBindingManager", 
              status_provider: "StatusProvider") -> None:
        pass

    def teardown(self, context: "ExtensibleContext", binding_manager: "KeyBindingManager",
                 status_provider: "StatusProvider") -> None:
        pass

    @property
    def volume(self) -> int:
        return self._volume
    
    @volume.setter
    def volume(self, value: int) -> None:
        self._volume = max(0, min(100, value))
    
    @property
    def is_playing(self) -> bool:
        return self._is_playing
    
    @is_playing.setter
    def is_playing(self, state: bool) -> None:
        self._is_playing = state
    
    def volume_up(self, step: int = 10) -> int:
        self.volume = self.volume + step
        return self.volume
    
    def volume_down(self, step: int = 10) -> int:
        self.volume = self.volume - step
        return self.volume
