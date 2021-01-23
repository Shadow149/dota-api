from PIL import Image, ImageDraw, ImageFont
import Player
from OpenDota import OpenDota
import requests

IMAGES = "https://cdn.cloudflare.steamstatic.com/"

class Infographic:
    def __init__(self, player):
        self.player = player
        self.header_font = ImageFont.truetype("fonts/reaver-black.otf", 40)
        self.text_font = ImageFont.truetype("fonts/reaver-black.otf", 24)

    def _create_hero_background_image(self, width, height):
        img = Image.new('RGB', (width, height), color = (32, 39, 50))
        return img

    def create_hero(self):
        img = self._create_hero_background_image(662,750)

        hero_url = IMAGES+self.player.get_hero_image_url()
        hero_img = Image.open(requests.get(hero_url, stream=True).raw)
        img.paste(hero_img, (50,230))

        # inv = Image.open("images/inventory.png")
        # img.paste(inv, (356, 120))


        draw = ImageDraw.Draw(img)

        team = self.player.get_team_name().upper()
        if team == "DIRE":
            win_x = 190
            draw.text((50,40), team, font=self.header_font, fill=(191, 38, 38,128))
        else:
            win_x = 290
            draw.text((50,40), team, font=self.header_font, fill=(63, 204, 47,128))
        
        win = self.player.get_win()
        if win:
            draw.text((win_x,52), "LOSE", font=self.text_font, fill=(191, 38, 38,128))
        else:
            draw.text((win_x,52), "WIN", font=self.text_font, fill=(63, 204, 47,128))

        playerName = self.player.personaname
        draw.text((50,100), playerName, font=self.header_font, fill=(94,186,237,128))
        
        hero = self.player.hero
        draw.text((50,160), hero, font=self.header_font, fill=(255,255,255,128))

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
        draw.text((50,394), lane, font=self.text_font, fill=(255,255,255,128))
        
        networth = f"Networth: {self.player.get_net_worth()}"
        draw.text((50,444), networth, font=self.text_font, fill=(255,255,255,128))

        kda = f"KDA: {' / '.join(map(str,self.player.get_KDA()))}"
        draw.text((50,494), kda, font=self.text_font, fill=(255,255,255,128))

        cs = f"CS: {''.join(str(self.player.get_cs())[1:-1])}"
        draw.text((50,544), cs, font=self.text_font, fill=(255,255,255,128))
        # draw.text((50,40), header, font=self.header_font, fill=(255,255,255,128))
        # draw.text((50,40), header, font=self.header_font, fill=(255,255,255,128))

        img.show()


if __name__ == "__main__":
    od = OpenDota()
    match = od.get_match_from_file("test_data.txt")
    players = match.get_players()
    inf = Infographic(players[6])
    inf.create_hero()
