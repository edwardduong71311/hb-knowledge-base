from dynaconf import Dynaconf

settings = Dynaconf(
    root_path="src/config",
    merge_enabled=True,
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
)
