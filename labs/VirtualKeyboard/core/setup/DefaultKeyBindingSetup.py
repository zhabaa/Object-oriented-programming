from string import ascii_lowercase, digits

from core import (
    BackspaceCommand,
    MediaPlayCommand,
    PrintCharCommand,
    ToggleCaseCommand,
    VolumeDownCommand,
    VolumeUpCommand,
)
from features import KeyBindingManager, PluginManager


class DefaultKeyBindingSetup:
    @staticmethod
    def setup(binding_manager: KeyBindingManager, 
              plugin_manager: PluginManager) -> None:

        plugin_manager.register_command_type("PrintCharCommand", PrintCharCommand)
        plugin_manager.register_command_type("BackspaceCommand", BackspaceCommand)
        plugin_manager.register_command_type("ToggleCaseCommand", ToggleCaseCommand)
        plugin_manager.register_command_type("MediaPlayCommand", MediaPlayCommand)
        plugin_manager.register_command_type("VolumeUpCommand", VolumeUpCommand)
        plugin_manager.register_command_type("VolumeDownCommand", VolumeDownCommand)

        for ch in ascii_lowercase:
            binding_manager.bind_key(ch, PrintCharCommand(ch))

        for d in digits:
            binding_manager.bind_key(d, PrintCharCommand(d))

        binding_manager.bind_key("space", PrintCharCommand(" "))
        binding_manager.bind_key("backspace", BackspaceCommand())
        binding_manager.bind_key("caps", ToggleCaseCommand())
        binding_manager.bind_key("volume_up", VolumeUpCommand())
        binding_manager.bind_key("volume_down", VolumeDownCommand())
        binding_manager.bind_key("media_play", MediaPlayCommand())
