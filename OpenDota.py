from Match import Match
from HTTPRequestHandler import HTTPRequestHandler
import json
from PIL import Image, ImageFilter

class OpenDota:
    def __init__(self):
        pass

    def get_match(self, match_id: int) -> Match:
        """
        Get Match object from specified dota match id

        Args:
            match_id (int): dota match id

        Returns:
            Match: Match object holding match data
        """
        return Match(match_id)
    
    def get_match_from_file(self, fileLocation) -> Match:
        """
        Get Match object from specified file, for testing

        Args:
            fileLocation (str): file location of match data

        Returns:
            Match: Match object holding match data
        """
        return Match(fileLocation = fileLocation)

    def _get_recent_matches(self, account_id) -> json:
        rh = HTTPRequestHandler()
        # Get request url
        rq = "https://api.opendota.com/api/players/" + str(account_id) + "/recentMatches"
        # Get request response
        response = rh.get(rq)
        json_data = None
        # Return as json object
        if response != None:
            json_data = json.loads(response)
        return json_data

    def get_last_x_matches_data_simple(self, number, account_id) -> list:
        """
        Get last specified number of matches, and returning simplified data

        Args:
            number: Number of past games
            account_id: steam/dota account number

        Returns:
            list: list of data in format: [match_id,hero_name,kills,deaths,assists]
        """
        # Get recent matches
        json_data = self._get_recent_matches(account_id)
        
        matches = []

        hero_json = None

        # Get hero json to get localised hero name from id
        with open("data/heroes.json") as hero_file:
            hero_json = json.load(hero_file)

        for i in range(number):
            match_id = json_data[i]["match_id"]

            hero_id = json_data[i]["hero_id"]
            hero_name = hero_json[str(hero_id)]["localized_name"]

            kills = json_data[i]["kills"]
            deaths = json_data[i]["deaths"]
            assists = json_data[i]["assists"]
            matches.append([match_id,hero_name,kills,deaths,assists])

        return matches

    def get_latest_match(self, account_id) -> Match:
        json_data = self._get_recent_matches(account_id)
        
        match_id = json_data[0]["match_id"]
        return Match(match_id)


if __name__ == "__main__":
    od = OpenDota()
    matches = od.get_last_x_matches_data_simple(5, 134205395)

    for i, match in enumerate(matches):
        print(f"({i}) Match ID: {match[0]}, Hero: {match[1]} K: {match[2]} D: {match[3]} A: {match[4]}")
    
