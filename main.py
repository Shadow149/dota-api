from OpenDota import OpenDota
import plotly.graph_objects as go

od = OpenDota()
match = od.get_match_from_file("test_data.txt")
#players = match.get_players()
print(match.get_radiant_gold_adv())
gold = match.get_radiant_gold_adv()
x = [0,
                60,
                120,
                180,
                240,
                300,
                360,
                420,
                480,
                540,
                600,
                660,
                720,
                780,
                840,
                900,
                960,
                1020,
                1080,
                1140,
                1200,
                1260,
                1320,
                1380,
                1440,
                1500,
                1560,
                1620,
                1680,
                1740,
                1800,
                1860,
                1920,
                1980,
                2040,
                2100,
                2160,
                2220,
                2280,
                2340,
                2400,
                2460,
                2520,
                2580,
                2640,
                2700,
                2760,
                2820,
                2880,
                2940,
                3000,
                3060,
                3120,
                3180,
                3240]
fig = go.Figure()
fig.add_trace(go.Scatter( y=gold, x = x,
                    mode='lines',
                    name='lines'))
fig.write_image("networth.png")
# for player in players:
#     print(player.team, player.personaname, player.hero, player.get_lane(), player.get_lane_role())