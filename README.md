# just-player

Минималистичный видеоплеер под Windows 11:
- UI/управление: Python (`tkinter`)
- декодинг/рендер: `libmpv` (через `python-mpv`)
- один живой инстанс плеера
- быстрый in-memory playlist
- без медиатеки, без лишних метаданных, без тяжелых зависимостей

## Быстрый старт

1. Установите Python 3.11+.
2. Установите `libmpv` (`mpv-2.dll` или `libmpv-2.dll`) и положите DLL:
   - рядом с `run.py`, или
   - в `just_player/bin`, или
   - в папку из `MPV_DLL_DIR` (env var), или
   - в системный `PATH`.
   
Важно: для Windows обычно нужен не только один `mpv-2.dll`, а весь набор DLL из `mpv-dev` архива (зависимости рядом в той же папке).
3. Установите зависимости:

```powershell
python -m pip install -r requirements.txt
```

4. Запуск:

```powershell
python run.py
```

Или сразу открыть файлы:

```powershell
python run.py "D:\video\one.mkv" "D:\video\two.mp4"
```

## Горячие клавиши

- `Ctrl+O` — открыть файлы
- `Space` — play/pause
- `N` / `P` — next / prev
- `Left` / `Right` — seek `-5/+5` сек
- `Up` / `Down` — громкость `+5/-5`
- `M` — mute
- `F` — fullscreen
- `S` — stop
- `Esc` — выйти из fullscreen, затем закрыть приложение

## Архитектура

- `run.py` — ultra-thin entrypoint
- `just_player/main.py` — CLI args + lazy старт app
- `just_player/app.py` — orchestration UI + engine + playlist
- `just_player/ui.py` — минимальное `tkinter` окно и hotkeys
- `just_player/core.py` — обертка над `mpv.MPV`, callbacks, hwdec options
- `just_player/playlist.py` — быстрый playlist в памяти (list + index)
- `just_player/settings.py` — tuning для low-overhead запуска/воспроизведения

## Сборка (Nuitka standalone)

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_nuitka.ps1
```

Onefile-вариант:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build_nuitka.ps1 -OneFile
```

Скрипт автоматически добавит `mpv-2.dll`, если DLL лежит в корне проекта.
