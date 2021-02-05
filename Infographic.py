from PIL import Image, ImageDraw, ImageFont, ImageFilter
import Player
from OpenDota import OpenDota
import requests
import io
import plotly.graph_objects as go

IMAGES = "https://cdn.cloudflare.steamstatic.com/"

class Infographic:
    def __init__(self, player):
        self.player = player
        self.header_font = ImageFont.truetype("fonts/reaver-black.otf", 40)
        self.sub_header_font = ImageFont.truetype("fonts/reaver-black.otf", 30)
        self.text_font = ImageFont.truetype("fonts/radiance-bold.otf", 24)
        self.big_text_font = ImageFont.truetype("fonts/radiance-bold.otf", 28)

    def _create_hero_background_image(self, width, height):
        img = Image.new('RGB', (width, height), color = (32, 39, 50))
        return img

    def create_hero(self, players):
        img = self._create_hero_background_image(1500,1350)

        hero_url = IMAGES+self.player.get_hero_image_url()
        hero_img = Image.open(requests.get(hero_url, stream=True).raw)
        img.paste(hero_img, (50,230))

        draw = ImageDraw.Draw(img)

        team = self.player.get_team_name().upper()
        if team == "DIRE":
            win_x = 190
            draw.text((50,40), team, font=self.header_font, fill=(191, 38, 38,128))
        else:
            win_x = 290
            draw.text((50,40), team, font=self.header_font, fill=(63, 204, 47,128))
        
        win = self.player.get_win()
        if not win:
            draw.rectangle([(win_x-7,52),(win_x + 64,55 + 30)], fill=(50,50,50,128))
            draw.text((win_x,55), "LOSE", font=self.text_font, fill=(255,255,255,128))
        else:
            draw.rectangle([(win_x-10,52),(win_x + 60,55 + 30)], fill=(63, 204, 47,128))
            draw.text((win_x,55), "WIN", font=self.text_font, fill=(255,255,255,128))


        playerName = self.player.personaname
        draw.text((50,100), playerName, font=self.header_font, fill=(94,186,237,128))
        
        hero = self.player.hero
        draw.text((50,160), hero, font=self.header_font, fill=(255,255,255,128))

        kda = f"{' / '.join(map(str,self.player.get_KDA()))}"
        draw.text((356,160), kda, font=self.header_font, fill=(255,255,255,128))

        for i, item in enumerate(self.player.get_items()):
            url = item.get_item_url()
            if url != None:
                item_url = IMAGES+item.get_item_url()
                item_img = Image.open(requests.get(item_url, stream=True).raw)
                mult_x = i % 3
                mult_y = 0 if i < 3 else 1
                x = 356 + (mult_x*85)
                y = 237 + (mult_y*64)
                img.paste(item_img, (x,y))


        lane = f"{self.player.get_lane_text()} Lane"
        draw.text((50,387), lane, font=self.text_font, fill=(255,255,255,128))
        
        networth = f"Networth: {self.player.get_net_worth()}"
        draw.text((50,424), networth, font=self.text_font, fill=(255,255,255,128))

        cs = f"CS: {''.join(str(self.player.get_cs())[1:-1])}"
        draw.text((50,454), cs, font=self.text_font, fill=(255,255,255,128))

        cs = f"GPM: {self.player.get_gpm()}"
        draw.text((50,484), cs, font=self.text_font, fill=(255,255,255,128))

        cs = f"XPM: {self.player.get_xpm()}"
        draw.text((50,514), cs, font=self.text_font, fill=(255,255,255,128))

        cs = f"Dmg Done: {self.player.get_damage_done()}"
        draw.text((50,544), cs, font=self.text_font, fill=(255,255,255,128))

        cs = f"Dmg Taken: {self.player.get_total_damage_taken()}"
        draw.text((50,574), cs, font=self.text_font, fill=(255,255,255,128))

        cs = f"Healing: {self.player.get_healing()}"
        draw.text((50,604), cs, font=self.text_font, fill=(255,255,255,128))

        minimap = self.create_heat_map()
        minimap = self._resize_image(minimap, 256, 256)
        img.paste(minimap, (356,384), minimap)

        creeps = Image.open("images/lane_creeps.png")
        creeps =  self._resize_image(creeps, 200, 256)
        img.paste(creeps, (40,664), creeps)

        cs = f"Lane Creeps"
        draw.text((336,664), cs, font=self.header_font, fill=(255,255,255,128))

        cs = str(self.player.get_lane_kills())
        draw.text((356,724), cs, font=self.text_font, fill=(255,255,255,128))

        cs = f"Neutral Creeps"
        draw.text((336,764), cs, font=self.header_font, fill=(255,255,255,128))

        cs = str(self.player.get_neutral_kills())
        draw.text((356,824), cs, font=self.text_font, fill=(255,255,255,128))
       
        nw_img = self._get_nw_graph(players)

        img.paste(nw_img,(-10,800),nw_img)

        cs = f"Damage Done"
        draw.text((670,230), cs, font=self.sub_header_font, fill=(255,255,255,128))


        #50,230
        length = 20

        damage_inflictor = self.player.get_damage_inflictor()
        damage_inflictor = dict(sorted(damage_inflictor.items(), key=lambda item: item[1], reverse=True))

        for i, inflictor in enumerate(damage_inflictor):
            # ab_x = (950+ (150 * (i//length)) + 15)
            # ab_y = 280 + ((i%length)*50)
            ab_x = (670+ (150 * (i//length)) + 15)
            ab_y = 280 + ((i%length)*50)

            if inflictor != "null":
                # not Right click
                try:
                    ability_url = IMAGES+"apps/dota2/images/abilities/"+inflictor+"_hp1.png"
                    ability_img = Image.open(requests.get(ability_url, stream=True).raw)
                    ability_img = self._resize_image(ability_img, 45,45)
                    img.paste(ability_img,(ab_x,ab_y))
                except:
                    try:
                        ability_url = IMAGES+"apps/dota2/images/items/"+inflictor+"_lg.png"
                        ability_img = Image.open(requests.get(ability_url, stream=True).raw)
                        ability_img = self._resize_image(ability_img, 45,45)
                        img.paste(ability_img,(ab_x,ab_y+6))
                    except:
                        pass
            else:
                ability_url = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heropedia/overviewicon_attack.png"
                ability_img = Image.open(requests.get(ability_url, stream=True).raw)
                ability_img = self._resize_image(ability_img, 0,45)
                img.paste(ability_img,(ab_x,ab_y+10),ability_img)

            text = f"{damage_inflictor[inflictor]}"
            draw.text((ab_x + 55,ab_y+7), text, font=self.big_text_font, fill=(255,255,255,128))

        cs = f"Damage Taken"
        draw.text((1050,230), cs, font=self.sub_header_font, fill=(255,255,255,128))

        damage_inflictor_taken = self.player.get_damage_inflictor_taken()
        damage_inflictor_taken = dict(sorted(damage_inflictor_taken.items(), key=lambda item: item[1], reverse=True))

        for i, inflictor in enumerate(damage_inflictor_taken):
            
            ab_x = (1050+ (150 * (i//length)) + 15)
            ab_y = 280 + ((i%length)*50)

            if inflictor != "null":
                # not Right click
                try:
                    ability_url = IMAGES+"apps/dota2/images/abilities/"+inflictor+"_hp1.png"
                    ability_img = Image.open(requests.get(ability_url, stream=True).raw)
                    ability_img = self._resize_image(ability_img, 45,45)
                    img.paste(ability_img,(ab_x,ab_y))
                    
                except:
                    try:
                        ability_url = IMAGES+"apps/dota2/images/items/"+inflictor+"_lg.png"
                        ability_img = Image.open(requests.get(ability_url, stream=True).raw)
                        ability_img = self._resize_image(ability_img, 45,45)
                        img.paste(ability_img,(ab_x,ab_y+6))
                    except:
                        pass
            else:
                ability_url = "https://cdn.cloudflare.steamstatic.com/apps/dota2/images/heropedia/overviewicon_attack.png"
                ability_img = Image.open(requests.get(ability_url, stream=True).raw)
                ability_img = self._resize_image(ability_img, 0,45)
                img.paste(ability_img,(ab_x,ab_y+10),ability_img)

            text = f"{damage_inflictor_taken[inflictor]} {round(damage_inflictor_taken[inflictor]/self.player.get_total_damage_taken() * 100, 2)}%"
            draw.text((ab_x + 55,ab_y+7), text, font=self.big_text_font, fill=(255,255,255,128))

        cs = f"Total stuns: {round(self.player.get_total_stuns(),2)}s"
        draw.text((50,1220), cs, font=self.header_font, fill=(255,255,255,128))

        img.save("infographic.png")
        #img.show()
        

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

    def get_bound_info(self, players, start, end):
        bounties = {}
        count = 0
        for p in range(start,end):
            player = players[p]
            runes = player.get_runes_log()
            for rune in runes:
                for i in range(13, -1, -1):
                    time = rune["time"]
                    if rune["key"] == 5:
                        if time > (i*500):
                            print(p,rune,(i*500))
                            count += 1
                            if (i*5) in bounties:
                                bounties[i*5] += 1
                            else:
                                bounties[i*5] = 1
                            break

        print(bounties)
        print(count)
        return bounties

    def create_bound_info(self, players):
        img = Image.new('RGB', (1024, 1024),  color = (32, 39, 50))
        draw = ImageDraw.Draw(img)
        bounty_rune = Image.open("images/bounty_rune.png")

        img.paste(bounty_rune, (-330,-200), bounty_rune)
        b_info_rad = self.get_bound_info(players, 0, 5)
        b_info_dir = self.get_bound_info(players, 6, 10)
        draw.line((360, 140, 1024 - 80,140),width=1, fill=(50,50,50,128))

        draw.text((270,90), "RAD", font=self.text_font, fill=(63, 204, 47,128))
        draw.text((270,170), "DIRE", font=self.text_font, fill=(191, 38, 38,128))
        
        small_bounty = Image.open("images/bounty_rune_mini.png")
        
        for time in sorted(b_info_rad):
            up = b_info_rad[time]

            diff = 1024 - 350
            diff /= len(b_info_rad)
            diff /= 5

            x = int(350 + (time*diff))
            y = 125
            img.paste(small_bounty, (x, y), small_bounty)


            for i in range(up):
                up_arrow = Image.open("images/up_arrow.png")
                up_arrow = self._resize_image(up_arrow,15,30)
                img.paste(up_arrow, (x + 2, y - 30 - (i*15)), up_arrow)
            
            draw.text((x + 43,y+3), str(time), font=self.text_font, fill=(170,170,170,128))
        
        for time in sorted(b_info_dir):
            up = b_info_dir[time]

            small_bounty = Image.open("images/bounty_rune_mini.png")
            diff = 1024 - 350
            diff /= len(b_info_rad)
            diff /= 5

            x = int(350 + (time*diff))
            y = 125
            img.paste(small_bounty, (x, y), small_bounty)


            for i in range(up):
                up_arrow = Image.open("images/up_arrow.png")
                up_arrow = self._resize_image(up_arrow,15,30)
                up_arrow = up_arrow.rotate(180)
                img.paste(up_arrow, (x + 2, y + 45 + (i*15)), up_arrow)

        #img.show()
        img.save("bounty.png")

    def _get_nw_graph(self, players):
        fig = go.Figure()
        for player in players:
            nw = player.get_gold_time()
            time = player.get_times()
            
            if player != self.player:
                fig.add_trace(go.Scatter(x=time, y=nw, mode='lines',name='lines',
                line=dict(color='rgb(50,50,50)')))

        nw = self.player.get_gold_time()
        time = self.player.get_times()
        fig.add_trace(go.Scatter(x=time, y=nw, mode='lines',name='lines',
                line=dict(color='rgb(94,186,237)')))

        fig.update_layout(
            xaxis=dict(
                showline=False,
                showgrid=False,
                showticklabels=False,
                zeroline=False
            ),
            yaxis = dict(
                gridcolor = 'rgb(39,48,61)',
                gridwidth = 10,
                zeroline=False
            ),
            font_color='white',
            plot_bgcolor='rgb(32, 39, 50)',
            paper_bgcolor='rgba(0,0,0,0)',
            height = 450,
            width = 700,
            showlegend=False
            
        )
        
        nw = fig.to_image()
        #fig.write_image("networth.png")
        nw_img = Image.open(io.BytesIO(nw))
        return nw_img

    def _resize_image(self, img, new_h, new_w):
        width, height = img.size

        new_h = int(new_w * height / width )
        new_w  = int(new_h * width / height)

        return img.resize((new_w, new_h), Image.ANTIALIAS)


if __name__ == "__main__":
    

    od = OpenDota()
    match = od.get_match_from_file("test3.json")
    #match = od.get_match(5802886821)
    players = match.get_players()
    inf = Infographic(players[5])
    inf.create_hero(players)
    #inf.create_bound_info(players)
    
