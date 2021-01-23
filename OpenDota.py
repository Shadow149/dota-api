from Match import Match
from HTTPRequestHandler import HTTPRequestHandler
import json

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

    def get_latest_match(self, account_id) -> int:
        rh = HTTPRequestHandler()
        # Get request url
        rq = "https://api.opendota.com/api/players/" + str(account_id) + "/recentMatches"
        # Get request response
        response = rh.get(rq)
        json_data = None
        # Return as json object
        if response != None:
            json_data = json.loads(response)
        
        match_id = json_data[0]["match_id"]
        return Match(match_id)


if __name__ == "__main__":
    od = OpenDota()
    match = od.get_match_from_file("test_data.txt")
    players = match.get_players()
    for player in players:
        print(player.team, player.personaname, player.hero, player.get_lane(), player.get_lane_role())
