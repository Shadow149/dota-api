from PIL import Image, ImageDraw, ImageFont, ImageFilter
import Player
from OpenDota import OpenDota
from XMLHandler import XMLHandler
from CSSHandler import CSSHandler
import requests
import io
import plotly.graph_objects as go

IMAGES = "https://cdn.cloudflare.steamstatic.com/"
DEFAULT_MARGIN = 50

class Infographic:
    def __init__(self, xml_path, css_path, player):
        self.player = player
        self.header_font = ImageFont.truetype("fonts/reaver-black.otf", 40)
        self.sub_header_font = ImageFont.truetype("fonts/reaver-black.otf", 30)
        self.text_font = ImageFont.truetype("fonts/radiance-bold.otf", 24)
        self.big_text_font = ImageFont.truetype("fonts/radiance-bold.otf", 28)
        self.xml_handler = XMLHandler(xml_path) 
        self.css_handler = CSSHandler(css_path)
        self.img = None
        self.draw = None
        
        self.y_off = 0
        self.prev_y_off = 0
        self.prev_x_off = 0
        self.prev_e_y_offset = 0
        self.prev_e_x_offset = 0
        self.x_off = 0
        self.inline = 0

    def initialise_image(self, width, height):
        self.img = Image.new('RGB', (width, height), color = (32, 39, 50))
        self.draw = ImageDraw.Draw(self.img)
    
    def initialise_variables(self):
        global heroName
        heroName = "asdasds"

    def process(self, elements, rules):
        for element in elements:
            if element.parent == None:
                self.inline = 0
                self.prev_x_off = 0

            for id_ in element.id:
                idents = rules[id_]
                #print(idents)
                for ident in idents:
                    if ident == "display":
                        if idents[ident] == "inline":
                            self.inline = 1
                            self.prev_x_off = self.x_off
                        else:
                            self.inline = 0
                    elif ident == "margin-left":
                        self.x_off += idents[ident]
                    elif ident == "margin-right":
                        self.x_off -= idents[ident]
                    elif ident == "margin-bottom":
                        self.y_off -= idents[ident]
                    elif ident == "margin-top":
                        self.y_off += idents[ident]
                    elif ident == "margin":
                        self.y_off += idents[ident]
                        self.x_off += idents[ident]
                        
                    self.prev_y_off = self.y_off

            print(element.element, element.id, element.data, self.inline)
            if element.element != "Section":
                e_y_offset = 0
                e_x_offset = 0
                #print(element.data[0])
                
                if not self.inline:
                    # if not in line
                    if (self.x_off > 0):
                        self.x_off = self.prev_x_off
                        #print("1")
                        self.y_off += self.prev_e_y_offset

                if element.element == "title":
                    text = element.data[0]
                    if text[0] == "{":
                        variable_str = text[1:-1]
                        text = globals()[variable_str]
                    text_size = self.draw.textsize(text, self.header_font)
                    e_x_offset = text_size[0] + 10
                    e_y_offset = text_size[1] + 10
                    x = DEFAULT_MARGIN+(self.x_off)
                    y = DEFAULT_MARGIN+(self.y_off * (1-self.inline))+(self.prev_y_off * self.inline)
                    self.draw.text((x,y), text, font=self.header_font, fill=(255, 255, 255,128))
                
                elif element.element == "label":
                    text = element.data[0]
                    text_size = self.draw.textsize(text, self.text_font)
                    e_x_offset = text_size[0] + 10
                    e_y_offset = text_size[1] + 10
                    x = DEFAULT_MARGIN+(self.x_off)
                    y = DEFAULT_MARGIN+(self.y_off * (1-self.inline))+(self.prev_y_off * self.inline)
                    self.draw.text((x,y), text, font=self.text_font, fill=(255, 255, 255,128))

                elif element.element == "image":
                    url = element.data[0]
                    img = Image.open(requests.get(url, stream=True).raw)
                    image_size = img.size
                    e_x_offset = image_size[0]
                    e_y_offset = image_size[1]
                    x = int(DEFAULT_MARGIN+(self.x_off))
                    y = int(DEFAULT_MARGIN+(self.y_off * (1-self.inline))+(self.prev_y_off * self.inline))
                    self.img.paste(img, (x,y))
                    
                if not self.inline:
                    self.y_off += e_y_offset
                else:
                    self.x_off += e_x_offset

                self.prev_e_y_offset = e_y_offset
                self.prev_y_off = self.y_off

                # self.prev_e_x_offset = e_x_offset
                # self.prev_x_off = self.x_off

            if element.element == "Section":
                self.process(element.children, rules)    

    def create(self):
        self.initialise_image(1500,1350) 
        elements = self.xml_handler.get_xml_elements()
        rules = self.css_handler.get_css()
        self.initialise_variables()
        self.process(elements, rules)

        self.img.save("new_info.png")

if __name__ == "__main__":

    od = OpenDota()
    match = od.get_match_from_file("test3.json")
    players = match.get_players()
    inf = Infographic('layouts/test.xml', 'styles/test.css', players[5])
    inf.create()
    
