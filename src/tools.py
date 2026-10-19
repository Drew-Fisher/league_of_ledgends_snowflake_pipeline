import copy

import requests
import pandas as pd

base_url = ""

def get_current_patch():
    url = f'https://ddragon.leagueoflegends.com/api/versions.json'
    respone = requests.get(
        url=url
    ).json()
    return respone[0]

def get_champions(region, patch):
    url = f'https://ddragon.leagueoflegends.com/cdn/{patch}/data/{region}/champion.json'
    response = requests.get(
        url=base_url+url
    )

    data = response.json()

    version = data['version']

    champion_info = []
    info_df = []
    stats_df = []
    tags = []

    for champ in data["data"].values():
        champ_info = {
            "champion_key": champ["key"] + " - " + version,
            "key": champ["key"],
            "id": champ["id"],
            "name": champ["name"],
            "title": champ["title"],
            "blurb": champ["blurb"],
            "partype": champ["partype"],
            "version": version
        }

        info = pd.json_normalize(champ["info"])
        info["champ_key"] = champ["key"] + " - " + version
        info["version"] = version

        stats = pd.json_normalize(champ["stats"])
        stats["champ_key"] = champ["key"] + " - " + version
        stats["version"] = version

        champion_info.append(champ_info)
        info_df.append(info)
        stats_df.append(stats)

        for tag in champ["tags"]:
            tags.append({
                "tag": tag,
                "champ_key": champ["key"] + " - " + version,
                "version": version
            })

    return {
        "champions": pd.DataFrame(champion_info),
        "champion_info": pd.concat(info_df, ignore_index=True),
        "champion_stats": pd.concat(stats_df, ignore_index=True),
        "champion_tags": pd.DataFrame(tags)
    }