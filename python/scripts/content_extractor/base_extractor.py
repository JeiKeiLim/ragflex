"""Base content extractor class.

 - Author: Jongkuk Lim
 - Contact: lim.jeikei@gmail.com
"""

from abc import ABC, abstractmethod

from typing import Union


class BaseExtractor(ABC):
    def __init__(self, path: str) -> None:
        self.__path = path
        self.__content = self._extract_content(path)

    @abstractmethod
    def _extract_content(path: Union[str, bytes]) -> str:
        pass

    @property
    def path(self) -> str:
        return self.__path

    @property
    def content(self) -> str:
        return self.__content
