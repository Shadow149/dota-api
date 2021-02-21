from XMLImage import XMLImage
from OpenDota import OpenDota
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import io
import json

IMAGES = "https://cdn.cloudflare.steamstatic.com/"

class TeamInfographic (XMLImage):
    def __init__(self, width, height, xml_path, css_path, players, team):
        super().__init__(width, height, xml_path, css_path)
        self.players = players
        self.team = team

    def initialise_variables(self):
        if self.team == 0:
            self.players = self.players[0:5]
            self.set_variable('team_colour',[63, 204, 47])
            self.set_variable('teamName',"RADIANT")      
        else:
            self.players = self.players[5:]
            self.set_variable('team_colour',[200, 38, 38])
            self.set_variable('teamName',"DIRE")      
        
        if self.players[0].get_win():
            self.set_variable('win','WIN')
            self.set_variable('win_colour',[63, 204, 47])
            self.set_variable('win_background_width', 50)
            self.set_variable('win_background_colour', [63, 204, 47])
        else:
            self.set_variable('win','LOSE')
            self.set_variable('win_colour',[200,200,200])
            self.set_variable('win_background_width', 57)
            self.set_variable('win_background_colour', [50,50,50])

        

        hero_url = []
        playerName = []
        kda = []
        networth = []
        cs = []
        gpm = []
        xpm = []
        dmg_done = []
        dmg_tkn = []
        stuns = []

        DEAFULT_COLOUR = [145, 172, 180]
        HIGHLIGHT_COLOUR = [214, 171, 54]

        for i,player in enumerate(self.players):
            hero_url.append([IMAGES+player.get_hero_image_url(),DEAFULT_COLOUR])
            playerName.append([player.personaname,DEAFULT_COLOUR])
            kda.append([' / '.join(map(str,player.get_KDA())),DEAFULT_COLOUR])
            networth.append([ player.get_net_worth(),DEAFULT_COLOUR])
            cs.append([ ' / '.join(map(str,player.get_cs())),DEAFULT_COLOUR])
            gpm.append([ player.get_gpm(),DEAFULT_COLOUR])
            xpm.append([ player.get_xpm(),DEAFULT_COLOUR])
            dmg_done.append([ player.get_damage_done(),DEAFULT_COLOUR])
            dmg_tkn.append([ player.get_total_damage_taken(),DEAFULT_COLOUR])
            if type(player.get_total_stuns()) == int:
                stuns.append([round(player.get_total_stuns(),2),DEAFULT_COLOUR])
            else:
                stuns.append([player.get_total_stuns(),DEAFULT_COLOUR])


            for j, item in enumerate(player.get_items()):
                url = item.get_item_url()
                print(url)
                if url != None:
                    item_url = IMAGES+item.get_item_url()
                    self.set_variable(f"item{i}{j}",item_url)
                else:
                    self.set_variable(f"item{i}{j}","")
        
        # kda[kda.index(max(kda))] = [kda[kda.index(max(kda))][0], HIGHLIGHT_COLOUR]
        # cs[cs.index(max(cs))] = [cs[cs.index(max(cs))][0], HIGHLIGHT_COLOUR]
        networth[networth.index(max(networth))] = [networth[networth.index(max(networth))][0], HIGHLIGHT_COLOUR]
        gpm[gpm.index(max(gpm))] = [gpm[gpm.index(max(gpm))][0], HIGHLIGHT_COLOUR]
        xpm[xpm.index(max(xpm))] = [xpm[xpm.index(max(xpm))][0], HIGHLIGHT_COLOUR]
        dmg_done[dmg_done.index(max(dmg_done))] = [dmg_done[dmg_done.index(max(dmg_done))][0], HIGHLIGHT_COLOUR]
        dmg_tkn[dmg_tkn.index(max(dmg_tkn))] = [dmg_tkn[dmg_tkn.index(max(dmg_tkn))][0], HIGHLIGHT_COLOUR]
        stuns[stuns.index(max(stuns))] = [stuns[stuns.index(max(stuns))][0], HIGHLIGHT_COLOUR]

        self.set_variable('hero_url', hero_url)
        self.set_variable('playerName', playerName)
        self.set_variable('kda', kda)
        self.set_variable('networth', networth)
        self.set_variable('cs', cs)
        self.set_variable('gpm', gpm)
        self.set_variable('xpm', xpm)
        self.set_variable('dmg_done', dmg_done)
        self.set_variable('dmg_tkn', dmg_tkn)
        self.set_variable('stuns', stuns)


if __name__ == "__main__":
    import sys

    od = OpenDota()
    match = od.get_match_from_file("test3.json")
    players = match.get_players()
    
    inf = TeamInfographic(int(sys.argv[1]),int(sys.argv[2]),
                          sys.argv[3], 
                          sys.argv[4], players, 1)

    inf.initialise_variables()

    inf.create()