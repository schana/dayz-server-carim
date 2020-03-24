# DayZ Server Configuration
Open source configuration and automation developed for the Carim DayZ Server, but usable by all. This is intended to be used in conjunction with [CFTools](cftools.de).

[Carim Server on Discord](https://discord.gg/kdPnVu4)

## Usage

1. Perform initial setup of [CFTools OmegaManager](https://wiki.cftools.de/display/CFTOOL/OmegaManager)
1. Copy `auth.json` and `preexec.bat` somewhere outside of the repository for security purposes
1. Edit the files with the appropriate values
1. Run `preexec.bat`
1. Your server should now be configured to automatically pull updates and apply them every time your server restarts

## Development usage

```bash
python3 -m carim.main -c -d <path to omega deploy directory> -a <path to your auth config> -o <path to output config to>
```

Configuration is generated and output in a folder named `generated-<timestamp>`. The contents of this can be copied into your omega directory.

![Carim](Carim.png "Carim Logo")
