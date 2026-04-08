APP_NAME = "Just Player"

# Minimal defaults tuned for startup and playback responsiveness.
MPV_OPTIONS = {
    "config": False,
    "idle": "yes",
    "keep_open": "always",
    "input_default_bindings": False,
    "input_vo_keyboard": False,
    "osc": False,
    "terminal": False,
    "msg_level": "all=error",
    "hwdec": "auto-safe",
    "vo": "gpu-next",
    "gpu_context": "d3d11",
    "cache": "no",
    "demuxer_max_bytes": "8MiB",
    "demuxer_max_back_bytes": "4MiB",
    "save_position_on_quit": False,
}

SEEK_SMALL_SECONDS = 5
VOLUME_STEP = 5
