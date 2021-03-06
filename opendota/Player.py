import json
from .Item import Item

VALUE_MISSING = "VNA"

class Player:
    def __init__(self, data):
        self._p_match_data = data
        self.id = self._get_account_id()
        self.personaname = self._get_persona_name()
        self.heroId = self._p_match_data["hero_id"]
        self.hero = self._get_hero()
        self.team = self._get_team()
    
    def handle_missing_value(self, value):
        if value in self._p_match_data:
            return self._p_match_data[value]
        return VALUE_MISSING

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
        return self.handle_missing_value("net_worth")

    def get_cs(self):
        lh = self.handle_missing_value("last_hits")
        dn = self.handle_missing_value("denies")
        return [lh,dn]

    def get_KDA(self):
        k = self.handle_missing_value("kills")
        d = self.handle_missing_value("deaths")
        a = self.handle_missing_value("assists")
        return [k,d,a]

    def get_lane(self):
        # 1: Bot
        # 2: Mid
        # 3: Top
        lane = self.handle_missing_value("lane")
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
        role = self.handle_missing_value("lane_role")
        return role

    def get_items(self):
        items = []
        for i in range(0,6):
            item = self.handle_missing_value(f"item_{i}")
            if item == VALUE_MISSING:
                continue
            items.append(Item(item))
        return items

    def get_win(self):
        return bool(self.handle_missing_value("win"))

    def get_lane_pos(self) -> dict:
        return self.handle_missing_value("lane_pos")

    def get_xpm(self):
        return self.handle_missing_value("xp_per_min")

    def get_gpm(self):
        return self.handle_missing_value("gold_per_min")

    def get_teamfight_participation(self):
        return self.handle_missing_value("teamfight_participation")

    def get_lane_efficiency(self):
        return self.handle_missing_value("lane_efficiency")

    def get_lane_kills(self):
        return self.handle_missing_value("lane_kills")

    def get_neutral_kills(self):
        return self.handle_missing_value("neutral_kills")

    def get_gold_time(self):
        return self.handle_missing_value("gold_t")
    
    def get_times(self):
        return self.handle_missing_value("times")

    def get_obs_killed(self):
        return self.handle_missing_value("obs_left_log")

    def get_obs_placed(self):
        return self.handle_missing_value("obs_log")

    def get_runes_log(self):
        return self.handle_missing_value("runes_log")

    def get_damage_done(self):
        return self.handle_missing_value("hero_damage")

    def get_damage_targets(self):
        return self.handle_missing_value("damage_targets")
    
    def get_damage_taken(self):
        return self.handle_missing_value("damage_taken")

    def get_total_damage_taken(self):
        dmg = self.get_damage_taken()
        if dmg == VALUE_MISSING or dmg == None:
            return VALUE_MISSING
        total = 0
        for d in dmg:
            total += dmg[d]
        return total

    def get_damage_inflictor(self):
        return self.handle_missing_value("damage_inflictor")
        
    def get_damage_inflictor_taken(self):
        return self.handle_missing_value("damage_inflictor_received")

    def get_total_stuns(self):
        return self.handle_missing_value("stuns")

    def get_healing(self):
        return self.handle_missing_value("hero_healing")

    def get_damage_taken_types(self):
        magical = 0
        physical = 0
        pure = 0
        unknown = 0
        abilityJson = None

        with open("data/abilities.json") as dmg_file:
            abilityJson = json.load(dmg_file)

        damageTaken = self.get_damage_inflictor_taken()
        if damageTaken == VALUE_MISSING:
            return VALUE_MISSING
        for dmg in damageTaken:
            if dmg in abilityJson:
                ability = abilityJson[dmg]
                if "dmg_type" in ability:
                    dType = ability["dmg_type"]
                    if dType == "Magical":
                        magical += damageTaken[dmg]
                    elif dType == "Pure":
                        pure += damageTaken[dmg]
                    else:
                        physical += damageTaken[dmg]
                else:
                    print(dmg)
                    unknown += damageTaken[dmg]
            elif dmg == "null":
                physical += damageTaken[dmg]
            else:
                print(dmg)
                unknown += damageTaken[dmg]

        return physical, magical, pure, unknown

    def get_damage_done_types(self):
        magical = 0
        physical = 0
        pure = 0
        unknown = 0
        abilityJson = None

        with open("data/abilities.json") as dmg_file:
            abilityJson = json.load(dmg_file)

        damageTaken = self.get_damage_inflictor()
        if damageTaken == VALUE_MISSING:
            return VALUE_MISSING
        for dmg in damageTaken:
            if dmg in abilityJson:
                ability = abilityJson[dmg]
                if "dmg_type" in ability:
                    dType = ability["dmg_type"]
                    if dType == "Magical":
                        magical += damageTaken[dmg]
                    elif dType == "Pure":
                        pure += damageTaken[dmg]
                    else:
                        physical += damageTaken[dmg]
                else:
                    print(dmg)
                    unknown += damageTaken[dmg]
            elif dmg == "null":
                physical += damageTaken[dmg]
            else:
                print(dmg)
                unknown += damageTaken[dmg]

        return physical, magical, pure, unknown
    
    def get_item_first_purchase_time(self):
        return self.handle_missing_value("first_purchase_time")