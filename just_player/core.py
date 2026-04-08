from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from .settings import MPV_OPTIONS


class MpvEngine:
    _dll_dirs: list[Any] = []

    def __init__(
        self,
        wid: int,
        call_ui: Callable[[Callable[..., Any], Any], None],
        on_end_of_file: Callable[[], None],
        on_path_loaded: Callable[[str], None],
    ) -> None:
        self._call_ui = call_ui
        self._on_end_of_file = on_end_of_file
        self._on_path_loaded = on_path_loaded
        self._mpv = self._create_player(wid)

    def _create_player(self, wid: int) -> Any:
        self._ensure_local_mpv_path()
        # Lazy import keeps startup overhead low when module is imported.
        try:
            import mpv
        except OSError as exc:
            raise RuntimeError(
                "libmpv DLL not found. Put mpv-2.dll next to run.py "
                "or into just_player/bin and restart."
            ) from exc

        options = dict(MPV_OPTIONS)
        options["wid"] = str(wid)
        player = mpv.MPV(**options)

        @player.event_callback("end-file")
        def _on_end(event: Any) -> None:
            reason = self._event_value(event, "reason")
            if self._is_eof_reason(reason):
                self._call_ui(self._on_end_of_file)

        @player.property_observer("path")
        def _on_path(_name: str, value: Any) -> None:
            if value:
                self._call_ui(self._on_path_loaded, str(value))

        return player

    @staticmethod
    def _event_value(event: Any, key: str) -> Any:
        if isinstance(event, dict):
            return event.get(key)
        return getattr(event, key, None)

    @staticmethod
    def _is_eof_reason(reason: Any) -> bool:
        if reason is None:
            return False
        if isinstance(reason, str):
            return reason.lower() == "eof"
        if isinstance(reason, int):
            return reason == 0
        name = getattr(reason, "name", None)
        if isinstance(name, str) and name.lower() == "eof":
            return True
        value = getattr(reason, "value", None)
        if isinstance(value, int) and value == 0:
            return True
        return False

    @staticmethod
    def _ensure_local_mpv_path() -> None:
        package_dir = Path(__file__).resolve().parent
        project_root = package_dir.parent
        extra_dir = os.environ.get("MPV_DLL_DIR", "")
        candidate_dirs = [
            str(project_root),
            str(project_root / "just_player" / "bin"),
            extra_dir,
        ]
        current_path = os.environ.get("PATH", "")
        found_dll_dir: str | None = None
        for path in candidate_dirs:
            if not path:
                continue
            p = Path(path)
            if not p.exists():
                continue
            if path not in current_path:
                current_path = path + os.pathsep + current_path
            if found_dll_dir is None:
                for dll_name in ("mpv-2.dll", "libmpv-2.dll", "mpv-1.dll"):
                    if (p / dll_name).is_file():
                        found_dll_dir = str(p)
                        break
        os.environ["PATH"] = current_path
        if found_dll_dir:
            add_dll_dir = getattr(os, "add_dll_directory", None)
            if callable(add_dll_dir):
                MpvEngine._dll_dirs.append(add_dll_dir(found_dll_dir))

    def load(self, path: str) -> None:
        self._mpv.loadfile(path, "replace")

    def toggle_pause(self) -> None:
        self._mpv.pause = not bool(self._mpv.pause)

    def seek(self, seconds: int) -> None:
        self._mpv.seek(seconds, reference="relative")

    def change_volume(self, delta: int) -> None:
        current = int(self._mpv.volume or 0)
        self._mpv.volume = max(0, min(100, current + delta))

    def toggle_mute(self) -> None:
        self._mpv.mute = not bool(self._mpv.mute)

    def toggle_fullscreen(self) -> bool:
        self._mpv.fullscreen = not bool(self._mpv.fullscreen)
        return bool(self._mpv.fullscreen)

    def stop(self) -> None:
        self._mpv.stop()

    def shutdown(self) -> None:
        self._mpv.terminate()
