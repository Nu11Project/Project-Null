import json
from pathlib import Path
from typing import Dict, NoReturn, Union

from graia.ariadne.model import Group

from library import config


class Switch:
    __switch: dict = Dict[str, Dict[str, bool]]

    def __init__(self):
        self.load()

    def load(self) -> NoReturn:
        """
        Load switch data from storage.

        :return: None.
        """

        if not Path(config.path.data, "switch.json").is_file():
            self.write()
            self.__switch = {}
        with Path(config.path.data, "switch.json").open("r", encoding="utf-8") as f:
            self.__switch = json.loads(f.read())

    def write(self) -> NoReturn:
        """
        Write switch data to storage.

        :return: None.
        """

        with Path(config.path.data, "switch.json").open("w", encoding="utf-8") as f:
            f.write(json.dumps(self.__switch, indent=4, ensure_ascii=False))

    def get(self, pack: str, group: Union[Group, int, str, None]) -> Union[None, bool]:
        """
        Get switch value.

        :param pack: pack name
        :param group: group instance, group id or None
        :return: switch value
        """

        if isinstance(group, Group):
            group = str(group.id)
        elif isinstance(group, int):
            group = str(group)
        elif group is None:
            group = "0"
        if module := self.__switch.get(pack, None):
            return module.get(group, None)
        return None

    def update(self, pack: str, group: Union[Group, int, str], value: bool):
        """
        Update switch value.

        :param pack: pack name
        :param group: group instance, group id or None
        :param value: switch value
        :return: None.
        """

        if isinstance(group, Group):
            group = str(group.id)
        elif isinstance(group, int):
            group = str(group)
        if pack in self.__switch.keys():
            self.__switch[pack][group] = value
            self.write()
            return
        self.__switch[pack] = {group: value}
        self.write()
        return


switch = Switch()