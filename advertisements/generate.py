advert = """
**Carim Loot+|Guns+|NPCs+|Airdrops|Trader|SimpleBase|Autorun**
178.63.43.16:2302

{open_name}Full mod list{close_name}{open_link}https://steamcommunity.com/sharedfiles/filedetails/?id=2034121973{close_link}

Come join the Carim, the server dedicated to serving the community through open source contributions. The server's configuration is automatically generated to be fun, fair, and balanced for whatever playstyle suits you. The server is managed by an IT professional, ensuring stability and responsiveness to issues.

Open source tools:

1. {open_name}Carim Discord Bot{close_name}{open_link}https://github.com/schana/carim-discord-bot{close_link} a bot that provides cross chat between the game and discord along with admin RCon commands for server owners
2. {open_name}Carim configuration tool{close_name}{open_link}https://github.com/schana/dayz-server-carim{close_link} tool used to generate the economy and mod configuration

Open source mods:

1. {open_name}SchanaModAutorun{close_name}{open_link}https://steamcommunity.com/sharedfiles/filedetails/?id=2031792120{close_link}
2. {open_name}SchanaModNoVehicleDamage{close_name}{open_link}https://steamcommunity.com/sharedfiles/filedetails/?id=2022423344{close_link}
3. {open_name}SchanaModSurvivorSelect{close_name}{open_link}https://steamcommunity.com/sharedfiles/filedetails/?id=2037681580{close_link}
4. {open_name}SchanaModAdminOmniTool{close_name}{open_link}https://steamcommunity.com/sharedfiles/filedetails/?id=2022600094{close_link}

Come support growing the community through open source!

{open_name}Carim Discord{close_name}{discord_open_link}https://discord.gg/kdPnVu4{discord_close_link}
"""
open_name, close_name, open_link, close_link = '[', ']', '(', ')'
discord_open_link, discord_close_link = open_link, close_link
print('Reddit')
print(advert.format(**locals()))

print()

open_name, close_name, open_link, close_link = '', ': ', '<', '>'
discord_open_link, discord_close_link = '', ''
print('Discord')
print(advert.format(**locals()))
