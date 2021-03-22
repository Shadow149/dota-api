from xml2img.XMLImage import XMLImage
from xml2img.Constants import Constants
from opendota.OpenDota import OpenDota
import json
import requests
from HeroInfographicSimple import HeroInfographicSimple

IMAGES = "https://cdn.cloudflare.steamstatic.com/"

class HeroBreakdown (XMLImage):
    def __init__(self, width, height, xml_path, css_path, background_colour, constants, player, debug):
        super().__init__(width, height, xml_path, css_path, background_colour, constants, debug)
        self.player = player
        self.background_colour = background_colour
        self.constants = constants

    def initialise_variables(self) -> bool:

        if self.player.get_total_stuns() != None:
            self.set_variable('stun', round(self.player.get_total_stuns(),0))
        else:
            # Limited data version!
            inf = HeroInfographicSimple(600, 770, 'layouts/HeroInfo_simple.xml', 'styles/HeroInfo_simple.css', self.background_colour, self.constants, self.player)
            completed = inf.initialise_variables()
            if completed:
                img = inf.create()
                img.save("info.png","png")
            return False

        self.set_variable('hero_url',IMAGES+self.player.get_hero_image_url())
        
        team = self.player.get_team_name().upper()
        self.set_variable('team',team)

        if team == "DIRE":
            self.set_variable('team_colour',[200, 38, 38])
        else:
            self.set_variable('team_colour',[63, 204, 47])
        
        
        if self.player.get_win():
            self.set_variable('win','WIN')
            self.set_variable('win_colour',[63, 204, 47])
            self.set_variable('win_background_width', 50)
            self.set_variable('win_background_colour', [63, 204, 47])
        else:
            self.set_variable('win','LOSE')
            self.set_variable('win_colour',[200,200,200])
            self.set_variable('win_background_width', 57)
            self.set_variable('win_background_colour', [50,50,50])

        self.set_variable('playerName',self.player.personaname)
        self.set_variable('hero',self.player.hero)
        self.set_variable('kda',' / '.join(map(str,self.player.get_KDA())))

        damage_inflictor_taken = self.player.get_damage_inflictor_taken()
        damage_inflictor_taken = dict(sorted(damage_inflictor_taken.items(), key=lambda item: item[1], reverse=True))
                    
        damage_inflictor_taken = [[key,damage_inflictor_taken[key],round(damage_inflictor_taken[key]/self.player.get_total_damage_taken() * 100,2),damage_inflictor_taken[key]/damage_inflictor_taken[list(damage_inflictor_taken)[0]] * 250] for key in list(damage_inflictor_taken)]
        
        for i, inflictor in enumerate(damage_inflictor_taken):
            if inflictor[0] != "null":
                ability_url = IMAGES+"apps/dota2/images/abilities/"+inflictor[0]+"_hp1.png"
                if requests.get(ability_url, stream=True).status_code == 404:
                    ability_url = IMAGES+"apps/dota2/images/items/"+inflictor[0]+"_lg.png"
                    damage_inflictor_taken[i][0] = ability_url
                else:
                    damage_inflictor_taken[i][0] = ability_url
            else:
                ability_url = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heropedia/overviewicon_attack.png"
                damage_inflictor_taken[i][0] = ability_url
            
        self.set_variable('damage_inflictor_taken',damage_inflictor_taken)
        
        damage_targets = self.player.get_damage_targets()
        damage_targets = [[key,[[nkey,damage_targets[key][nkey]] for nkey in list(damage_targets[key])]] for key in list(damage_targets)]

        grid = []
        damage_inflictors = []
        enemy_heros = [""]
        
        for i in damage_targets:
            dmg_to_heros = i[1]
            for h in dmg_to_heros:
                hero = h[0]
                if hero not in enemy_heros:
                    enemy_heros.append(hero)
        grid.append( enemy_heros)
        for i in damage_targets:
            print("dmg",i[0])
            row = [0] * (len(enemy_heros) + 1)
            row[0] = i[0]
            dmg_to_heros = i[1]
            for h in dmg_to_heros:
                for j, hero in enumerate(enemy_heros):
                    if hero == h[0]:
                        row[j] = h[1]
            row[-1] = sum(row[1:])
            grid.append(row)
        
        for row in grid:
            print(row)
            
        hero_name_json = None
        with open("data/hero_names.json") as hero_file:
            hero_name_json = json.load(hero_file)

    
        for i, row in enumerate(grid):
            if i == 0:
                #heros
                for j, col in enumerate(row):
                    if grid[i][j] != '':
                        grid[i][j] = IMAGES[:-1]+hero_name_json[row[j]]["img"]
                
            if row[0] == None:
                continue
            if row[0] != "null":
                ability_url = IMAGES+"apps/dota2/images/abilities/"+row[0]+"_hp1.png"
                if requests.get(ability_url, stream=True).status_code == 404:
                    ability_url = IMAGES+"apps/dota2/images/items/"+row[0]+"_lg.png"
                    grid[i][0] = ability_url
                else:
                    grid[i][0] = ability_url
            else:
                ability_url = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heropedia/overviewicon_attack.png"
                grid[i][0] = ability_url
                
        totals = [sum(x) for x in list(zip(*grid[1:]))[1:]]
        grid.append(totals)
        
        print("asdasd",len(grid[0]))
        self.set_variable('grid_cols',[i for i in range(0,len(grid))])
        self.set_variable('damage_grid',grid)
        
        phBarLengthTaken = 0
        magBarLengthTaken = 0
        pureBarLengthTaken = 0
        uBarLengthTaken = 0

        physicalTaken = 0
        magicalTaken = 0
        pureTaken = 0
        unknownTaken = 0

        if self.player.get_damage_taken_types() != None:

            physicalTaken, magicalTaken, pureTaken, unknownTaken = self.player.get_damage_taken_types()
            mostDmg = max([physicalTaken, magicalTaken, pureTaken, unknownTaken])
            phBarLengthTaken = int(physicalTaken/mostDmg * 150)
            magBarLengthTaken = int(magicalTaken/mostDmg * 150)
            pureBarLengthTaken = int(pureTaken/mostDmg * 150)
            uBarLengthTaken = int(unknownTaken/mostDmg * 150)

        self.set_variable('phBarLengthTaken', phBarLengthTaken)
        self.set_variable('magBarLengthTaken', magBarLengthTaken)
        self.set_variable('pureBarLengthTaken', pureBarLengthTaken)
        self.set_variable('uBarLengthTaken', uBarLengthTaken)

        self.set_variable('physicalTaken', physicalTaken)
        self.set_variable('magicalTaken', magicalTaken)
        self.set_variable('pureTaken', pureTaken)
        self.set_variable('unknownTaken', unknownTaken)
        
        phBarLengthDone = 0
        magBarLengthDone = 0
        pureBarLengthDone = 0
        uBarLengthDone = 0

        physicalDone = 0
        magicalDone = 0
        pureDone = 0
        unknownDone = 0

        if self.player.get_damage_done_types() != None:

            physicalDone, magicalDone, pureDone, unknownDone = self.player.get_damage_done_types()
            mostDmg = max([physicalDone, magicalDone, pureDone, unknownDone])
            phBarLengthDone = int(physicalDone/mostDmg * 150)
            magBarLengthDone = int(magicalDone/mostDmg * 150)
            pureBarLengthDone = int(pureDone/mostDmg * 150)
            uBarLengthDone = int(unknownDone/mostDmg * 150)

        self.set_variable('phBarLengthDone', phBarLengthDone)
        self.set_variable('magBarLengthDone', magBarLengthDone)
        self.set_variable('pureBarLengthDone', pureBarLengthDone)
        self.set_variable('uBarLengthDone', uBarLengthDone)

        self.set_variable('physicalDone', physicalDone)
        self.set_variable('magicalDone', magicalDone)
        self.set_variable('pureDone', pureDone)
        self.set_variable('unknownDone', unknownDone)
        
        

        return True



if __name__ == "__main__":
    import sys

    od = OpenDota()
    match = od.get_match_from_file('test3.json')
    #match = od.get_match(5845488682)
    players = match.get_players()
    
    consts = Constants()
    
    inf = HeroBreakdown(int(sys.argv[1]),int(sys.argv[2]),
                          sys.argv[3], 
                          sys.argv[4], (32, 39, 50), consts,
                          players[int(sys.argv[5])], bool(int(sys.argv[6])))

    completed = inf.initialise_variables()

    if completed:
        inf.create()