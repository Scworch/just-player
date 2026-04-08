from __future__ import annotations

from collections.abc import Callable
from typing import Any

from .settings import APP_NAME


class PlayerUI:
    def __init__(self) -> None:
        # Lazy import so CLI path parsing remains instant.
        import tkinter as tk

        self._tk = tk
        self.root = tk.Tk(className=APP_NAME)
        self.root.title(APP_NAME)
        self.root.geometry("980x560")
        self.root.configure(bg="black")
        self.root.minsize(480, 270)

        self.video = tk.Frame(self.root, bg="black", borderwidth=0, highlightthickness=0)
        self.video.pack(fill="both", expand=True)

        self.status = tk.Label(
            self.root,
            bg="#111111",
            fg="#bbbbbb",
            borderwidth=0,
            anchor="w",
            padx=8,
            pady=4,
            text="Ctrl+O open | Space pause | N/P next/prev | F fullscreen",
        )
        self.status.pack(fill="x")
        self._is_fullscreen = False

    def attach_shortcuts(
        self,
        on_open: Callable[[], None],
        on_next: Callable[[], None],
        on_prev: Callable[[], None],
        on_pause: Callable[[], None],
        on_seek_back: Callable[[], None],
        on_seek_forward: Callable[[], None],
        on_volume_down: Callable[[], None],
        on_volume_up: Callable[[], None],
        on_fullscreen: Callable[[], None],
        on_mute: Callable[[], None],
        on_stop: Callable[[], None],
        on_quit: Callable[[], None],
    ) -> None:
        bindings: list[tuple[str, Callable[[], None]]] = [
            ("<Control-o>", on_open),
            ("<Control-O>", on_open),
            ("<n>", on_next),
            ("<N>", on_next),
            ("<p>", on_prev),
            ("<P>", on_prev),
            ("<space>", on_pause),
            ("<Left>", on_seek_back),
            ("<Right>", on_seek_forward),
            ("<Down>", on_volume_down),
            ("<Up>", on_volume_up),
            ("<f>", on_fullscreen),
            ("<F>", on_fullscreen),
            ("<m>", on_mute),
            ("<M>", on_mute),
            ("<s>", on_stop),
            ("<S>", on_stop),
            ("<Escape>", on_quit),
        ]
        for sequence, callback in bindings:
            self.root.bind(sequence, self._wrap(callback), add="+")

    def _wrap(self, callback: Callable[[], None]) -> Callable[[Any], str]:
        def _handler(_event: Any) -> str:
            callback()
            return "break"

        return _handler

    def set_title(self, title: str) -> None:
        self.root.title(title)

    def set_status(self, text: str) -> None:
        self.status.configure(text=text)

    def get_video_wid(self) -> int:
        self.root.update_idletasks()
        return int(self.video.winfo_id())

    def on_close(self, callback: Callable[[], None]) -> None:
        self.root.protocol("WM_DELETE_WINDOW", callback)

    def call_soon(self, callback: Callable[..., None], *args: Any) -> None:
        self.root.after(0, callback, *args)

    def run(self) -> None:
        self.root.mainloop()

    def close(self) -> None:
        self.root.destroy()

    def toggle_fullscreen(self) -> bool:
        self._is_fullscreen = not self._is_fullscreen
        self.root.attributes("-fullscreen", self._is_fullscreen)
        return self._is_fullscreen

    def exit_fullscreen(self) -> bool:
        if not self._is_fullscreen:
            return False
        self._is_fullscreen = False
        self.root.attributes("-fullscreen", False)
        return True
