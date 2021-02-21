from XMLImage import XMLImage
from OpenDota import OpenDota
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import json

IMAGES = "https://cdn.cloudflare.steamstatic.com/"

class HeroInfographicSimple (XMLImage):
    def __init__(self, width, height, xml_path, css_path, player):
        super().__init__(width, height, xml_path, css_path)
        self.player = player

    def initialise_variables(self) -> bool:

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

        for i, item in enumerate(self.player.get_items()):
            url = item.get_item_url()
            print(item)
            if url != None:
                item_url = IMAGES+item.get_item_url()
                self.set_variable(f"item_{i}",item_url)
            else:
                self.set_variable(f"item_{i}","")

        self.set_variable('networth', self.player.get_net_worth())
        self.set_variable('cs', ' / '.join(map(str,self.player.get_cs())))
        self.set_variable('gpm', self.player.get_gpm())
        self.set_variable('xpm', self.player.get_xpm())
        self.set_variable('dmg_done', self.player.get_damage_done())
        self.set_variable('heal', self.player.get_healing())
    
        return True



if __name__ == "__main__":
    import sys

    od = OpenDota()
    # match = od.get_match_from_file('test3.json')
    match = od.get_match(5833286287)
    players = match.get_players()
    
    inf = HeroInfographic(int(sys.argv[1]),int(sys.argv[2]),
                          sys.argv[3], 
                          sys.argv[4], 
                          players[int(sys.argv[5])])

    # inf = HeroInfographic(int(sys.argv[1]),int(sys.argv[2]),
    #                       sys.argv[3], 
    #                       sys.argv[4], 
    #                       players[0])

    completed = inf.initialise_variables()

    if completed:
        inf.create()