from __future__ import annotations

from os.path import basename
from typing import Iterable

from .core import MpvEngine
from .playlist import Playlist
from .settings import APP_NAME, SEEK_SMALL_SECONDS, VOLUME_STEP
from .ui import PlayerUI


class JustPlayerApp:
    def __init__(self, startup_paths: Iterable[str]) -> None:
        self.ui = PlayerUI()
        self.playlist = Playlist()
        self._closing = False

        self.ui.attach_shortcuts(
            on_open=self.open_files_dialog,
            on_next=self.next_track,
            on_prev=self.prev_track,
            on_pause=self.toggle_pause,
            on_seek_back=lambda: self.seek(-SEEK_SMALL_SECONDS),
            on_seek_forward=lambda: self.seek(SEEK_SMALL_SECONDS),
            on_volume_down=lambda: self.change_volume(-VOLUME_STEP),
            on_volume_up=lambda: self.change_volume(VOLUME_STEP),
            on_fullscreen=self.toggle_fullscreen,
            on_mute=self.toggle_mute,
            on_stop=self.stop,
            on_quit=self.quit,
        )
        self.ui.on_close(self.quit)

        self.engine = MpvEngine(
            wid=self.ui.get_video_wid(),
            call_ui=self.ui.call_soon,
            on_end_of_file=self._on_end_of_file,
            on_path_loaded=self._on_path_loaded,
        )

        self.ui.set_status("Ready | Ctrl+O open files")
        if startup_paths:
            self.open_paths(startup_paths)

    def run(self) -> None:
        self.ui.run()

    def open_files_dialog(self) -> None:
        from tkinter import filedialog

        paths = filedialog.askopenfilenames(
            title="Open video files",
            filetypes=[
                ("Media files", "*.mkv *.mp4 *.avi *.mov *.webm *.mp3 *.flac *.wav"),
                ("All files", "*.*"),
            ],
        )
        if paths:
            self.open_paths(paths)

    def open_paths(self, paths: Iterable[str]) -> None:
        if self.playlist.set_items(paths):
            self._play_current()
            self.ui.set_status(f"Playlist: {len(self.playlist)} file(s)")

    def _play_current(self) -> None:
        path = self.playlist.current()
        if path:
            self.engine.load(path)

    def next_track(self) -> None:
        if self.playlist.next():
            self._play_current()
        else:
            self.ui.set_status("End of playlist")

    def prev_track(self) -> None:
        if self.playlist.prev():
            self._play_current()
        else:
            self.ui.set_status("Start of playlist")

    def _on_end_of_file(self) -> None:
        self.next_track()

    def _on_path_loaded(self, path: str) -> None:
        short = basename(path)
        self.ui.set_title(f"{APP_NAME} - {short}" if short else APP_NAME)

    def toggle_pause(self) -> None:
        self.engine.toggle_pause()

    def seek(self, seconds: int) -> None:
        self.engine.seek(seconds)

    def change_volume(self, delta: int) -> None:
        self.engine.change_volume(delta)

    def toggle_mute(self) -> None:
        self.engine.toggle_mute()

    def toggle_fullscreen(self) -> None:
        enabled = self.ui.toggle_fullscreen()
        self.ui.set_status("Fullscreen" if enabled else "Windowed")

    def stop(self) -> None:
        self.engine.stop()

    def quit(self) -> None:
        if self._closing:
            return
        if self.ui.exit_fullscreen():
            self.ui.set_status("Windowed")
            return
        self._closing = True
        try:
            self.engine.shutdown()
        finally:
            self.ui.close()
