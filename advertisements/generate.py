advert = """\
{bold_open}Carim{bold_close} Loot+|Guns+|NPCs+|Airdrops|Trader|SimpleBase|Autorun
`178.63.43.16:2302`
Classic PvP with bases, airdrops, traders, increased loot, and more

{bold_open}Carim{bold_close} Survival
`178.63.43.16:2502`
Difficult survival with some quality of life improvements like autorun, compass, and party system

{bold_open}Carim{bold_close} Deathmatch NWAF
`178.63.43.16:2402`
Spawn fully equipped with assault rifle and sniper around NWAF

Come join Carim, the servers dedicated to serving the community through open source contributions. The servers' configurations are automatically generated to be fun, fair, and balanced for whatever playstyle suits you. The servers are managed by an IT professional, ensuring stability and responsiveness to issues.

Come support growing the community through open source! More info can be found on {open_name}the website{close_name}{open_link}https://schana.github.io/carim/{close_link}.

{open_name}Carim Discord{close_name}{discord_open_link}https://discord.gg/kdPnVu4{discord_close_link}
"""
bold_open, bold_close = '**', '**'
open_name, close_name, open_link, close_link = '[', ']', '(', ')'
discord_open_link, discord_close_link = open_link, close_link
print('Reddit')
print(advert.format(**locals()))

print()

open_name, close_name, open_link, close_link = '', ': ', '<', '>'
discord_open_link, discord_close_link = '', ''
print('Discord')
print(advert.format(**locals()))

bold_open, bold_close = '[h1]', '[/h1]'
open_name, close_name, open_link, close_link = '', '', '[url=', '][/url]'
discord_open_link, discord_close_link = open_link, close_link
print('Steam')
print(advert.format(**locals()))
# Still need to move the link title inside the url block manually
