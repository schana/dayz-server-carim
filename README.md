# DayZ Server Configuration
Open source configuration and automation primarily for the Carim DayZ Server. This is intended to be used in conjunction with [CFTools](cftools.de).

[Carim Server on Discord](https://discord.gg/kdPnVu4)

## Usage

Most of the configuration generation is handled by the `setup_profiles.py` script. There is a sample auth config at `omega/auth.json`.

```bash
python3 setup_profiles.py -c -d <path to omega deploy directory> -a <path to your auth config>
```

Configuration is generated and output in a folder named `generated-<timestamp>`. The contents of this can be copied into your omega directory.
 