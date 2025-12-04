
from core.commands import Command, PrintCharCommand, VolumeUpCommand, VolumeDownCommand
from core.typing import SerializedCommand
from features.plugins import PluginManager


class ExtensibleCommandSerializer:
    def __init__(self, plugin_manager: PluginManager):
        self.plugin_manager = plugin_manager

    def serialize(self, cmd: Command) -> SerializedCommand:
        if isinstance(cmd, PrintCharCommand):
            return SerializedCommand(type="PrintCharCommand", char=cmd.char)

        elif isinstance(cmd, (VolumeUpCommand, VolumeDownCommand)):
            return SerializedCommand(type=type(cmd).__name__, step=cmd.step)

        else:
            return SerializedCommand(type=type(cmd).__name__)

    def deserialize(self, data: SerializedCommand) -> Command:
        registry = self.plugin_manager.get_command_registry()
        cls = registry.get(data.type)

        if cls is None:
            raise ValueError(f"Unknown command type: {data.type}")

        if data.type == "PrintCharCommand":
            return cls(data.char)

        elif data.type in ["VolumeUpCommand", "VolumeDownCommand"]:
            return cls(data.step or 10)

        else:
            return cls()
