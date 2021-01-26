import json
from Item import Item

class Player:
    def __init__(self, data):
        self._p_match_data = data
        self.id = self._get_account_id()
        self.personaname = self._get_persona_name()
        self.heroId = self._p_match_data["hero_id"]
        self.hero = self._get_hero()
        self.team = self._get_team()

    def _get_account_id(self):
        a_id = self._p_match_data["account_id"]
        if a_id != None:
            # TODO get account name
            return a_id
        return "Anonymous"

    def _get_persona_name(self):
        if "personaname" in self._p_match_data:
            return self._p_match_data["personaname"]
        return "Anonymous"

    def _get_hero(self):
        hero_json = None
        with open("data/heroes.json") as hero_file:
            hero_json = json.load(hero_file)

        return hero_json[str(self.heroId)]["localized_name"]
    
    def _get_team(self):
        radiant = self._p_match_data["isRadiant"]
        return 1 if radiant else 0

    def get_hero_image_url(self):
        hero_json = None
        with open("data/heroes.json") as hero_file:
            hero_json = json.load(hero_file)

        return hero_json[str(self.heroId)]["img"]
    
    def get_team_name(self):
        if self.team == 0:
            return "Dire"
        return "Radiant"

    def get_net_worth(self):
        return self._p_match_data["net_worth"]

    def get_cs(self):
        lh = self._p_match_data["last_hits"]
        dn = self._p_match_data["denies"]
        return [lh,dn]

    def get_KDA(self):
        k = self._p_match_data["kills"]
        d = self._p_match_data["deaths"]
        a = self._p_match_data["assists"]
        return [k,d,a]

    def get_lane(self):
        # 1: Bot
        # 2: Mid
        # 3: Top
        lane = self._p_match_data["lane"]
        return lane
    
    def get_lane_text(self):
        lane = self.get_lane()
        if lane == 1:
            return "Bottom"
        elif lane == 2:
            return "Mid"
        return "Top"
    
    def get_lane_role(self):
        # ?????
        role = self._p_match_data["lane_role"]
        return role

    def get_items(self):
        items = []
        for i in range(0,6):
            items.append(Item(self._p_match_data[f"item_{i}"]))
        return items

    def get_win(self):
        return bool(self._p_match_data["win"])

    def get_lane_pos(self) -> dict:
        pos = self._p_match_data["lane_pos"]
        return pos

    def get_xpm(self):
        return self._p_match_data["xp_per_min"]

    def get_gpm(self):
        return self._p_match_data["gold_per_min"]

    def get_teamfight_participation(self):
        return self._p_match_data["teamfight_participation"]

    def get_lane_efficiency(self):
        return self._p_match_data["lane_efficiency"]

    def get_lane_kills(self):
        return self._p_match_data["lane_kills"]

    def get_neutral_kills(self):
        return self._p_match_data["neutral_kills"]

    def get_gold_time(self):
        return self._p_match_data["gold_t"]
    
    def get_times(self):
        return self._p_match_data["times"]

    def get_obs_killed(self):
        return self._p_match_data["obs_left_log"]

    def get_obs_placed(self):
        return self._p_match_data["obs_log"]

    def get_runes_log(self):
        return self._p_match_data["runes_log"]

    def get_damage_done(self):
        return self._p_match_data["hero_damage"]

    def get_damage_taken(self):
        return self._p_match_data["damage_taken"]

    def get_total_damage_taken(self):
        dmg = self.get_damage_taken()
        total = 0
        for d in dmg:
            total += dmg[d]
        return total

    def get_damage_inflictor(self):
        return self._p_match_data["damage_inflictor"]
        
    def get_damage_inflictor_taken(self):
        return self._p_match_data["damage_inflictor_received"]

    def get_total_stuns(self):
        return self._p_match_data["stuns"]

    def get_healing(self):
        return self._p_match_data["hero_healing"]