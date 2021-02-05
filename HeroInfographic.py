from XMLImage import XMLImage
from OpenDota import OpenDota
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import json

IMAGES = "https://cdn.cloudflare.steamstatic.com/"

class HeroInfographic (XMLImage):
    def __init__(self, width, height, xml_path, css_path, player):
        super().__init__(width, height, xml_path, css_path)
        self.player = player

    def create_heat_map(self):
        pos = self.player.get_lane_pos()
        
        minimap = Image.open('images/minimap.png')
        img = Image.new('RGBA', (1024, 1024), (255, 0, 0, 0))
        pixels = img.load()

        for x in pos:
            for y in pos[x]:
                x_coord = ((int(x)) * 5 - 310) * 1.6
                y_coord = -(1024 - ((200 - int(y)) * 5 + 330)) * 1.6

                d = int(pos[x][y])
                for i in range(-10,10):
                    for j in range(-10,10):
                        pixels[x_coord + i,y_coord + j] = (50*d,10*d,d)
                
        img1 = img.filter(ImageFilter.GaussianBlur(radius=20))
        minimap.paste(img1 ,(0, 0), img1)
       # minimap.show()
        return minimap 

    def initialise_variables(self):
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

        self.set_variable('lane',self.player.get_lane_text())
        self.set_variable('networth', self.player.get_net_worth())
        self.set_variable('cs', ' / '.join(map(str,self.player.get_cs())))
        self.set_variable('gpm', self.player.get_gpm())
        self.set_variable('xpm', self.player.get_xpm())
        self.set_variable('dmg_done', self.player.get_damage_done())
        self.set_variable('dmg_tkn', self.player.get_total_damage_taken())
        self.set_variable('heal', self.player.get_healing())
        self.set_variable('lane_cs',str(self.player.get_lane_kills()))
        self.set_variable('neutral_cs',str(self.player.get_neutral_kills()))
        
        minimap = self.create_heat_map()
        img_byte_arr = io.BytesIO()
        minimap.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        self.set_variable('heatmap_img', img_byte_arr)

        physical, magical, pure, unknown = self.player.get_damage_taken_types()
        mostDmg = max([physical, magical, pure, unknown])
        phBarLength = int(physical/mostDmg * 150)
        magBarLength = int(magical/mostDmg * 150)
        pureBarLength = int(pure/mostDmg * 150)
        uBarLength = int(unknown/mostDmg * 150)

        self.set_variable('phBarLength', phBarLength)
        self.set_variable('magBarLength', magBarLength)
        self.set_variable('pureBarLength', pureBarLength)
        self.set_variable('uBarLength', uBarLength)

        self.set_variable('physical', physical)
        self.set_variable('magical', magical)
        self.set_variable('pure', pure)
        self.set_variable('unknown', unknown)



if __name__ == "__main__":
    import sys

    od = OpenDota()
    match = od.get_match_from_file("test3.json")
    players = match.get_players()
    
    inf = HeroInfographic(int(sys.argv[1]),int(sys.argv[2]),
                          sys.argv[3], 
                          sys.argv[4], 
                          players[int(sys.argv[5])])

    inf.initialise_variables()

    inf.create()