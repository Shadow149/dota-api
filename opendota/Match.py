from .HTTPRequestHandler import HTTPRequestHandler
from .Player import Player
import json
import io

JSON_CACHE_DIR = "json_cache.json"
MATCH_DATA_QUERY = 'https://api.opendota.com/api/matches/'

class Match:
    def __init__(self, matchId = None, fileLocation = None):
        if matchId != None:
            self.matchId = matchId
            self.data = self._get_json()
        else:
            # Assuming fileLocation is filled
            self.data = self._get_json_from_file(fileLocation)

    def _get_json_from_file(self, fileLocation) -> json:
        """
        Get match data as a json object, from a file location

        Returns:
            json: Json of all the match data
        """
        json_data = None
        with open(fileLocation, 'r', encoding="utf-8") as match_data:
            json_data = json.load(match_data)
        return json_data

    def _save_json_cache(self, json) -> None:
        """
        Saves json string to local json file
        """
        with io.open(JSON_CACHE_DIR, "w+", encoding="utf-8") as f:
            f.write(json)

    def _in_cache(self) -> bool:
        """
        Check the match data associated with the match id is in the cache json

        Returns:
            bool
        """
        json_cache = self._get_json_from_file(JSON_CACHE_DIR)
        cache_match_id = json_cache["match_id"]
        return self.matchId == cache_match_id, json_cache


    def _get_json(self) -> json:
        """
        Get match data as a json object

        Returns:
            json: Json of all the match data
        """
        # Check match is in cache
        inCache, json_cache = self._in_cache()
        if inCache:
            print("In cache!")
            return json_cache
            
        rh = HTTPRequestHandler()
        # Get request url
        rq = MATCH_DATA_QUERY + str(self.matchId)
        # Get request response
        response = rh.get(rq)
        # Return as json object
        if response != None:
            self._save_json_cache(response)
            return json.loads(response, encoding="utf-8")
        return None

    def get_winning_team(self):
        rw = self.data["radiant_win"]
        if rw:
            return "Radiant"
        return "Dire"

    def get_players(self):
        players = []
        for player_data in self.data["players"]:
            players.append(Player(player_data))
        
        return players

    def get_radiant_gold_adv(self):
        radiant_gold_adv = self.data["radiant_gold_adv"]
        return radiant_gold_adv
