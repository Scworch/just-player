from __future__ import annotations

from os import fspath
from typing import Iterable


class Playlist:
    __slots__ = ("_items", "_index")

    def __init__(self) -> None:
        self._items: list[str] = []
        self._index = -1

    def clear(self) -> None:
        self._items.clear()
        self._index = -1

    def set_items(self, paths: Iterable[str], start_index: int = 0) -> bool:
        items = [fspath(path) for path in paths if path]
        if not items:
            self.clear()
            return False
        self._items = items
        self._index = max(0, min(start_index, len(items) - 1))
        return True

    def append_items(self, paths: Iterable[str]) -> int:
        added = 0
        for path in paths:
            if path:
                self._items.append(fspath(path))
                added += 1
        if self._index < 0 and self._items:
            self._index = 0
        return added

    def current(self) -> str | None:
        if self._index < 0 or self._index >= len(self._items):
            return None
        return self._items[self._index]

    def next(self) -> str | None:
        next_index = self._index + 1
        if next_index >= len(self._items):
            return None
        self._index = next_index
        return self._items[self._index]

    def prev(self) -> str | None:
        prev_index = self._index - 1
        if prev_index < 0:
            return None
        self._index = prev_index
        return self._items[self._index]

    def __len__(self) -> int:
        return len(self._items)
