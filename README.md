# DayZ Server Configuration
Open source configuration and automation primarily for the Carim DayZ Server. This is intended to be used in conjunction with [CFTools](cftools.de).

[Carim Server on Discord](https://discord.gg/kdPnVu4)

## Usage

Most of the configuration generation is handled by the application. There is a sample auth config at `resources/auth.json`.

```bash
python3 -m carim.main -c -d <path to omega deploy directory> -a <path to your auth config> -o <path to output config to>
```

Configuration is generated and output in a folder named `generated-<timestamp>`. The contents of this can be copied into your omega directory.
