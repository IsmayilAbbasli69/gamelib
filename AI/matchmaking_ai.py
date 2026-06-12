import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# 1. 15 NƏFƏRLİK ZƏNGİN SİNTETİK OYUNÇU BAZASI (DATASET)
# ID-lər: 730 (CS2), 570 (Dota 2), 578080 (PUBG), 105600 (Terraria)
RAW_PLAYER_DATA = [
    {"steamid": "701", "username": "Elnur_FPS", "games": {730: 50000, 570: 2000, 578080: 35000, 105600: 0}, "preferred_genre": "Action/FPS"},
    {"steamid": "702", "username": "Aysel_MOBA", "games": {730: 500, 570: 80000, 578080: 1200, 105600: 4000}, "preferred_genre": "MOBA"},
    {"steamid": "703", "username": "Tural_Tactical", "games": {730: 45000, 570: 0, 578080: 40000, 105600: 500}, "preferred_genre": "Action/FPS"},
    {"steamid": "704", "username": "Samir_Indie", "games": {730: 0, 570: 1500, 578080: 0, 105600: 12000}, "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "705", "username": "Leyla_Hardcore_MOBA", "games": {730: 0, 570: 120000, 578080: 0, 105600: 300}, "preferred_genre": "MOBA"},
    {"steamid": "706", "username": "Rauf_GlobalElite", "games": {730: 180000, 570: 4000, 578080: 15000, 105600: 0}, "preferred_genre": "Action/FPS"},
    {"steamid": "707", "username": "Nigar_Casual", "games": {730: 1200, 570: 3000, 578080: 2500, 105600: 4500}, "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "708", "username": "Farid_PUBG_King", "games": {730: 15000, 570: 500, 578080: 95000, 105600: 1000}, "preferred_genre": "Action/FPS"},
    {"steamid": "709", "username": "Ilkin_Sandbox", "games": {730: 0, 570: 0, 578080: 5000, 105600: 65000}, "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "710", "username": "Gunel_Hybrid", "games": {730: 25000, 570: 30000, 578080: 10000, 105600: 5000}, "preferred_genre": "MOBA"},
    {"steamid": "711", "username": "Anar_Noob", "games": {730: 100, 570: 200, 578080: 50, 105600: 150}, "preferred_genre": "Action/FPS"},
    {"steamid": "712", "username": "Rashad_Pro", "games": {730: 90000, 570: 10000, 578080: 55000, 105600: 0}, "preferred_genre": "Action/FPS"},
    {"steamid": "713", "username": "Zahra_Dota_Queen", "games": {730: 2000, 570: 150000, 578080: 0, 105600: 1200}, "preferred_genre": "MOBA"},
    {"steamid": "714", "username": "Emin_Crafter", "games": {730: 500, 570: 0, 578080: 800, 105600: 88000}, "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "715", "username": "Murad_Chiller", "games": {730: 12000, 570: 8000, 578080: 14000, 105600: 9000}, "preferred_genre": "Strategy/Co-Op"}
    {"steamid": "76561198000000001", "username": "Elnur_Gamer", "role": "Entry Fragger", "hours": [540, 210, 0, 12, 0, 85, 0, 45], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000002", "username": "Tural_Pro", "role": "In-Game Leader (IGL)", "hours": [820, 640, 15, 0, 0, 310, 0, 155], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000003", "username": "Rashad_AimBot", "role": "AWPer / Sniper", "hours": [1450, 45, 0, 0, 5, 110, 0, 12], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000004", "username": "Gunel_Carry", "role": "Hard Carry (Pos 1)", "hours": [120, 980, 10, 0, 0, 35, 15, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000005", "username": "Xayal_Global", "role": "Entry Fragger", "hours": [1900, 150, 5, 0, 0, 90, 0, 30], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000006", "username": "Farid_MidOrFeed", "role": "Midlaner (Pos 2)", "hours": [300, 1200, 0, 10, 0, 50, 0, 5], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000007", "username": "Nijat_Clutch", "role": "Lurker", "hours": [750, 180, 20, 15, 0, 140, 0, 60], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000008", "username": "Samira_Support", "role": "Hard Support (Pos 5)", "hours": [80, 850, 30, 0, 0, 65, 25, 10], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000009", "username": "Anar_OneTap", "role": "AWPer / Sniper", "hours": [1150, 90, 0, 0, 10, 130, 5, 20], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000010", "username": "Zaur_Radiant", "role": "Offlaner (Pos 3)", "hours": [450, 710, 0, 5, 0, 80, 0, 15], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000011", "username": "Kamran_FPS", "role": "Entry Fragger", "hours": [1300, 200, 15, 0, 0, 160, 0, 40], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000012", "username": "Leyla_Wards", "role": "Soft Support (Pos 4)", "hours": [50, 1100, 40, 10, 5, 30, 20, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000013", "username": "Orxan_Axe", "role": "Offlaner (Pos 3)", "hours": [920, 430, 0, 0, 0, 210, 0, 70], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000014", "username": "Fuad_Headshot", "role": "Lurker", "hours": [1650, 30, 0, 0, 0, 95, 0, 10], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000015", "username": "Sabina_Invoker", "role": "Midlaner (Pos 2)", "hours": [110, 1340, 25, 5, 0, 45, 15, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000016", "username": "Vusal_AWP", "role": "AWPer / Sniper", "hours": [1050, 140, 10, 0, 0, 115, 0, 25], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000017", "username": "Ilkin_Rampage", "role": "Hard Carry (Pos 1)", "hours": [380, 890, 0, 0, 10, 75, 0, 5], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000018", "username": "Rauf_Tactical", "role": "In-Game Leader (IGL)", "hours": [880, 250, 35, 20, 0, 180, 10, 50], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000019", "username": "Narmin_Duo", "role": "Hard Support (Pos 5)", "hours": [210, 780, 15, 0, 0, 55, 30, 15], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000020", "username": "Elvin_Scream", "role": "Entry Fragger", "hours": [1550, 80, 0, 0, 0, 105, 0, 8], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000021", "username": "Rustam_Pudge", "role": "Soft Support (Pos 4)", "hours": [140, 1020, 5, 10, 0, 40, 0, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000022", "username": "Asif_Deagle", "role": "Lurker", "hours": [970, 160, 15, 0, 5, 125, 0, 35], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000023", "username": "Gulten_Mid", "role": "Midlaner (Pos 2)", "hours": [90, 910, 20, 0, 0, 50, 10, 10], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000024", "username": "Manaf_Smurf", "role": "Hard Carry (Pos 1)", "hours": [1750, 310, 0, 0, 0, 150, 0, 20], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000025", "username": "Taleh_Techies", "role": "Offlaner (Pos 3)", "hours": [60, 1450, 10, 0, 0, 30, 5, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000026", "username": "Emin_CS", "role": "AWPer / Sniper", "hours": [1100, 50, 0, 0, 10, 90, 0, 30], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000027", "username": "Aylin_Dota", "role": "Hard Support (Pos 5)", "hours": [90, 1250, 20, 0, 0, 40, 15, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000028", "username": "Riyad_Aim", "role": "Entry Fragger", "hours": [1400, 100, 0, 0, 0, 110, 0, 15], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000029", "username": "Sevinc_Carry", "role": "Hard Carry (Pos 1)", "hours": [200, 990, 5, 0, 0, 30, 0, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000030", "username": "Nurlan_IGL", "role": "In-Game Leader (IGL)", "hours": [950, 300, 40, 10, 0, 200, 10, 80], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000031", "username": "Ogtay_Mid", "role": "Midlaner (Pos 2)", "hours": [150, 1150, 0, 5, 0, 60, 0, 10], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000032", "username": "Zari_Lurk", "role": "Lurker", "hours": [680, 140, 15, 10, 0, 120, 0, 50], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000033", "username": "Kenan_Pos4", "role": "Soft Support (Pos 4)", "hours": [70, 890, 30, 0, 0, 50, 20, 5], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000034", "username": "Camil_Sniper", "role": "AWPer / Sniper", "hours": [1250, 80, 0, 0, 5, 140, 0, 25], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000035", "username": "Elmir_Off", "role": "Offlaner (Pos 3)", "hours": [490, 780, 0, 0, 0, 85, 5, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000036", "username": "Nadir_FPS", "role": "Entry Fragger", "hours": [1350, 180, 10, 0, 0, 150, 0, 35], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000037", "username": "Arzu_Dota", "role": "Hard Support (Pos 5)", "hours": [40, 1050, 35, 15, 0, 25, 30, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000038", "username": "Vasif_Lurk", "role": "Lurker", "hours": [890, 210, 0, 0, 0, 135, 0, 45], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000039", "username": "Lala_Mid", "role": "Midlaner (Pos 2)", "hours": [250, 1210, 20, 0, 0, 40, 10, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000040", "username": "Shamil_IGL", "role": "In-Game Leader (IGL)", "hours": [790, 400, 30, 20, 0, 190, 0, 65], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000041", "username": "Adil_Carry", "role": "Hard Carry (Pos 1)", "hours": [180, 1020, 0, 0, 0, 55, 0, 10], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000042", "username": "Fidan_Pos4", "role": "Soft Support (Pos 4)", "hours": [110, 930, 15, 5, 0, 45, 15, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000043", "username": "Tahir_Global", "role": "Entry Fragger", "hours": [1600, 120, 0, 0, 0, 100, 0, 20], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000044", "username": "Rena_Support", "role": "Hard Support (Pos 5)", "hours": [60, 880, 25, 0, 0, 50, 25, 15], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000045", "username": "Rovshan_AWP", "role": "AWPer / Sniper", "hours": [1180, 70, 0, 0, 10, 125, 0, 15], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000046", "username": "Hasan_Pos3", "role": "Offlaner (Pos 3)", "hours": [400, 690, 10, 0, 0, 70, 0, 5], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000047", "username": "Nigar_Mid", "role": "Midlaner (Pos 2)", "hours": [130, 1100, 15, 10, 0, 35, 5, 0], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000048", "username": "Eldar_Carry", "role": "Hard Carry (Pos 1)", "hours": [310, 950, 0, 0, 0, 70, 0, 10], "preferred_genre": "MOBA"},
    {"steamid": "76561198000000049", "username": "Perviz_Lurk", "role": "Lurker", "hours": [920, 170, 25, 15, 5, 140, 0, 40], "preferred_genre": "Action/FPS"},
    {"steamid": "76561198000000050", "username": "Umid_IGL", "role": "In-Game Leader (IGL)", "hours": [840, 310, 20, 0, 0, 220, 10, 75], "preferred_genre": "Action/FPS"},

    # 51-100: RPG & Souls-like
    {"steamid": "76561198000000051", "username": "Aysel_RPG", "role": "Mage / Spellcaster", "hours": [0, 0, 155, 125, 95, 15, 210, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000052", "username": "Leyla_Cyber", "role": "Stealth / Assassin", "hours": [12, 0, 185, 255, 45, 0, 115, 5], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000053", "username": "Emin_Tarnished", "role": "Melee Warrior (Tank)", "hours": [45, 15, 95, 65, 315, 25, 145, 10], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000054", "username": "Murad_Lore", "role": "Tactician / Healer", "hours": [0, 0, 225, 45, 155, 0, 415, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000055", "username": "Jale_Witcher", "role": "Melee Warrior (Tank)", "hours": [5, 0, 340, 140, 80, 20, 160, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000056", "username": "Ramil_Souls", "role": "Melee Warrior (Tank)", "hours": [20, 10, 70, 50, 420, 30, 90, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000057", "username": "Nigar_Faerun", "role": "Tactician / Healer", "hours": [0, 0, 190, 90, 110, 10, 350, 5], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000058", "username": "Kanan_NightCity", "role": "Stealth / Assassin", "hours": [30, 0, 130, 310, 60, 40, 120, 15], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000059", "username": "Babek_Hunter", "role": "Archer / Ranger", "hours": [15, 5, 260, 80, 210, 15, 180, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000060", "username": "Arzu_Druid", "role": "Tactician / Healer", "hours": [0, 0, 140, 75, 130, 5, 290, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000061", "username": "Shahin_V", "role": "Stealth / Assassin", "hours": [40, 0, 165, 280, 50, 50, 100, 10], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000062", "username": "Deniz_Malenia", "role": "Melee Warrior (Tank)", "hours": [10, 0, 85, 40, 380, 20, 130, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000063", "username": "Yusif_Geralt", "role": "Melee Warrior (Tank)", "hours": [0, 0, 410, 110, 70, 15, 140, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000064", "username": "Fidan_Tadpole", "role": "Mage / Spellcaster", "hours": [5, 5, 115, 60, 95, 10, 380, 15], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000065", "username": "Rovshan_Dex", "role": "Archer / Ranger", "hours": [55, 20, 100, 95, 260, 45, 150, 20], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000066", "username": "Nurlan_Silverhand", "role": "Stealth / Assassin", "hours": [25, 0, 210, 340, 40, 35, 80, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000067", "username": "Gunay_Paladin", "role": "Tactician / Healer", "hours": [0, 0, 135, 50, 120, 0, 310, 5], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000068", "username": "Agil_AshenOne", "role": "Melee Warrior (Tank)", "hours": [15, 10, 90, 30, 450, 15, 70, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000069", "username": "Turkan_Yennefer", "role": "Mage / Spellcaster", "hours": [0, 0, 380, 160, 55, 25, 175, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000070", "username": "Musa_Shadowheart", "role": "Tactician / Healer", "hours": [10, 0, 150, 85, 140, 10, 330, 10], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000071", "username": "Sevda_Chomba", "role": "Mage / Spellcaster", "hours": [35, 15, 120, 210, 75, 60, 115, 15], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000072", "username": "Hasan_Rivia", "role": "Melee Warrior (Tank)", "hours": [0, 0, 450, 105, 65, 20, 125, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000073", "username": "Pervin_Mage", "role": "Mage / Spellcaster", "hours": [0, 0, 175, 70, 165, 0, 270, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000074", "username": "Rasim_Samurai", "role": "Stealth / Assassin", "hours": [60, 25, 140, 295, 90, 70, 95, 25], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000075", "username": "Aynur_Ciri", "role": "Archer / Ranger", "hours": [0, 0, 395, 135, 45, 15, 190, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000076", "username": "Fuad_RPG", "role": "Melee Warrior (Tank)", "hours": [0, 0, 210, 90, 130, 10, 180, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000077", "username": "Zahra_Lore", "role": "Tactician / Healer", "hours": [5, 0, 170, 60, 80, 0, 390, 5], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000078", "username": "Toghrul_Souls", "role": "Melee Warrior (Tank)", "hours": [30, 10, 80, 40, 490, 20, 60, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000079", "username": "Nigar_V", "role": "Stealth / Assassin", "hours": [0, 0, 140, 320, 50, 30, 110, 10], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000080", "username": "Elvin_Hunter", "role": "Archer / Ranger", "hours": [20, 0, 240, 70, 190, 15, 160, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000081", "username": "Arzu_Mage", "role": "Mage / Spellcaster", "hours": [0, 0, 150, 80, 110, 0, 280, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000082", "username": "Sabuhi_Souls", "role": "Melee Warrior (Tank)", "hours": [50, 0, 100, 50, 390, 40, 120, 15], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000083", "username": "Laman_BG3", "role": "Tactician / Healer", "hours": [0, 0, 180, 50, 140, 10, 360, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000084", "username": "Vusal_Cyber", "role": "Stealth / Assassin", "hours": [40, 0, 130, 290, 70, 50, 90, 20], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000085", "username": "Narmin_RPG", "role": "Archer / Ranger", "hours": [10, 5, 290, 100, 150, 20, 140, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000086", "username": "Kamran_Lore", "role": "Tactician / Healer", "hours": [0, 0, 160, 70, 120, 5, 310, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000087", "username": "Aydan_Ciri", "role": "Stealth / Assassin", "hours": [15, 0, 350, 120, 60, 40, 150, 10], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000088", "username": "Samir_Souls", "role": "Melee Warrior (Tank)", "hours": [25, 0, 95, 35, 410, 25, 110, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000089", "username": "Chinara_Mage", "role": "Mage / Spellcaster", "hours": [0, 0, 125, 95, 85, 10, 340, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000090", "username": "Nijat_RPG", "role": "Melee Warrior (Tank)", "hours": [45, 10, 115, 75, 280, 35, 130, 15], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000091", "username": "Ayla_Lore", "role": "Tactician / Healer", "hours": [0, 0, 200, 55, 160, 0, 400, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000092", "username": "Kanan_Witcher", "role": "Melee Warrior (Tank)", "hours": [5, 0, 430, 100, 50, 20, 120, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000093", "username": "Sabina_V", "role": "Stealth / Assassin", "hours": [30, 0, 155, 330, 40, 45, 85, 5], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000094", "username": "Tural_Ranger", "role": "Archer / Ranger", "hours": [20, 10, 220, 85, 175, 15, 195, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000095", "username": "Leyla_Druid", "role": "Tactician / Healer", "hours": [0, 0, 145, 65, 135, 0, 320, 5], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000096", "username": "Ismail_Souls", "role": "Melee Warrior (Tank)", "hours": [10, 5, 85, 25, 460, 15, 80, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000097", "username": "Gulten_Mage", "role": "Mage / Spellcaster", "hours": [0, 0, 185, 80, 155, 0, 260, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000098", "username": "Rauf_Cyber", "role": "Stealth / Assassin", "hours": [50, 20, 130, 280, 80, 65, 105, 20], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000099", "username": "Fidan_Ciri", "role": "Stealth / Assassin", "hours": [0, 0, 380, 145, 40, 20, 175, 0], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000100", "username": "Zaur_BG3", "role": "Tactician / Healer", "hours": [15, 0, 160, 70, 145, 15, 300, 10], "preferred_genre": "Strategy/Co-Op"},

    # 101-150: Casual, Co-Op & Open World
    {"steamid": "76561198000000101", "username": "Samir_Retro", "role": "Co-Op Survivor", "hours": [55, 0, 15, 25, 0, 45, 15, 305], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000102", "username": "Farid_LosSantos", "role": "Driver / Heist Crew", "hours": [155, 85, 35, 15, 0, 655, 5, 185], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000103", "username": "Nigar_CoOp", "role": "Co-Op Survivor", "hours": [25, 0, 0, 10, 0, 145, 10, 455], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000104", "username": "Eyyub_Trevor", "role": "Gunman / Chaos Maker", "hours": [110, 40, 20, 5, 0, 890, 0, 120], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000105", "username": "Vahid_Zombie", "role": "Co-Op Survivor", "hours": [40, 10, 5, 15, 10, 110, 0, 520], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000106", "username": "Natavan_Fun", "role": "Co-Op Survivor", "hours": [95, 60, 40, 30, 0, 420, 25, 260], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000107", "username": "Elshad_Heist", "role": "Driver / Heist Crew", "hours": [200, 120, 15, 0, 0, 780, 0, 140], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000108", "username": "Lala_Survivor", "role": "Co-Op Survivor", "hours": [15, 0, 10, 25, 5, 90, 15, 490], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000109", "username": "Rufat_Modder", "role": "Driver / Heist Crew", "hours": [130, 70, 50, 40, 15, 610, 30, 210], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000110", "username": "Zahra_Safehouse", "role": "Co-Op Survivor", "hours": [60, 20, 0, 10, 0, 130, 0, 580], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000111", "username": "Seymur_Franklin", "role": "Gunman / Chaos Maker", "hours": [180, 95, 25, 5, 0, 710, 10, 165], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000112", "username": "Rena_Left4Ever", "role": "Co-Op Survivor", "hours": [30, 0, 0, 20, 0, 105, 5, 610], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000113", "username": "Tofig_Online", "role": "Driver / Heist Crew", "hours": [220, 150, 45, 15, 10, 840, 0, 135], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000114", "username": "Konul_Casual", "role": "Co-Op Survivor", "hours": [85, 50, 30, 35, 0, 390, 40, 290], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000115", "username": "Mikayil_Rush", "role": "Co-Op Survivor", "hours": [140, 30, 10, 0, 0, 230, 0, 410], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000116", "username": "Bahar_Green", "role": "Driver / Heist Crew", "hours": [50, 10, 20, 15, 5, 480, 20, 310], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000117", "username": "Riyad_CEO", "role": "Gunman / Chaos Maker", "hours": [250, 110, 0, 10, 0, 950, 0, 90], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000118", "username": "Aftandil_Old", "role": "Co-Op Survivor", "hours": [70, 0, 5, 5, 0, 160, 0, 540], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000119", "username": "Aysel_Fun", "role": "Co-Op Survivor", "hours": [105, 75, 35, 45, 10, 440, 35, 240], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000120", "username": "Ismail_Biker", "role": "Driver / Heist Crew", "hours": [160, 60, 15, 0, 0, 730, 0, 175], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000121", "username": "Nezrin_Witch", "role": "Co-Op Survivor", "hours": [20, 0, 10, 15, 0, 115, 15, 470], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000122", "username": "Tahir_Sniper", "role": "Driver / Heist Crew", "hours": [210, 130, 40, 20, 5, 590, 10, 225], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000123", "username": "Medina_Gamer", "role": "Co-Op Survivor", "hours": [45, 15, 0, 10, 0, 150, 5, 500], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000124", "username": "Polad_Chop", "role": "Gunman / Chaos Maker", "hours": [195, 85, 30, 0, 0, 810, 0, 150], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000125", "username": "Valida_Coop", "role": "Co-Op Survivor", "hours": [80, 40, 25, 30, 0, 360, 25, 330], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000126", "username": "Anar_Casual", "role": "Co-Op Survivor", "hours": [60, 0, 10, 20, 0, 50, 20, 310], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000127", "username": "Tural_GTA", "role": "Driver / Heist Crew", "hours": [160, 90, 30, 20, 0, 660, 10, 190], "preferred_genre": "Strategy/Co-Op"},
    {"steamid": "76561198000000128", "username": "Gunel_L4D", "role": "Co-Op Survivor", "hours": [30, 0, 0, 15, 0, 150, 15, 460], "preferred_genre": "Strategy/Co-Op"}
]

class SteamMatchmakerAI:
    def __init__(self, tracked_games):
        """AI Modelini başladır və izləniləcək oyun vektorunu müəyyən edir."""
        self.tracked_games = tracked_games
        self.players_metadata = []
        self.feature_matrix = None  # Model təlim olunduqdan sonra matris bura yığılacaq

    def train(self, database):
        """
        MODELİN TƏLİM OLUNMASI (TRAINING PROCESS)
        Verilənlər bazasındakı bütün istifadəçilərin oyun saatlarını riyazi matrisə (vektora) yığır.
        """
        matrix_list = []
        self.players_metadata = []
        
        for player in database:
            # Hər oyunçu üçün saat vektorunu qurur: [Oyun1_saat, Oyun2_saat, ...]
            vector = [player["games"].get(appid, 0) for appid in self.tracked_games]
            matrix_list.append(vector)
            
            # ML proqnoz verəndə istifadəçi adlarını tapmaq üçün metadatnı saxlayır
            self.players_metadata.append({
                "steamid": player["steamid"],
                "username": player["username"],
                "preferred_genre": player["preferred_genre"]
            })
            
        # Listi rəsmi NumPy Matrisinə çeviririk (AI modeli hazır vəziyyətə gəlir)
        self.feature_matrix = np.array(matrix_list)
        print(f"🤖 [AI MODEL]: Model {len(database)} oyunçu üzərində uğurla təlim olundu (Matrix Shape: {self.feature_matrix.shape})")

    def _parse_steam_api(self, api_response):
        """Steam API-dən gələn JSON-u oxuyub təmiz lüğətə çevirən daxili metod."""
        if not api_response or "response" not in api_response or "games" not in api_response["response"]:
            return None
        return {g["appid"]: g.get("playtime_forever", 0) for g in api_response["response"]["games"]}

    def predict_best_matches(self, current_user_api_data, fallback_genre=None, top_n=3):
        """
        MAŞIN ÖYRENMƏSİ PROQNOZU (INFERENCE)
        Kosinus Oxşarlığı ilə ən uyğun oyun yoldaşlarını tapır.
        """
        user_games = self._parse_steam_api(current_user_api_data)
        
        # --- COLD START / GİZLİ PROFİL SSENARİSİ ---
        if user_games is None or sum(user_games.values()) == 0:
            print("⚠️ [AI FALLBACK]: İstifadəçi datası tapılmadı (Cold Start). Janr əsaslı tövsiyə edilir...")
            fallback_results = []
            for peer in self.players_metadata:
                score = 85.0 if fallback_genre and fallback_genre.lower() == peer["preferred_genre"].lower() else 40.0
                fallback_results.append({
                    "username": peer["username"],
                    "steamid": peer["steamid"],
                    "match_score": score,
                    "method": "Rule-Based (Genre Fallback)"
                })
            return sorted(fallback_results, key=lambda x: x["match_score"], reverse=True)[:top_n]

        # --- REALLIQA AKTİV KOSİNUS OXŞARLIĞI (ML MODEL PROQNOZU) ---
        user_vector = [user_games.get(appid, 0) for appid in self.tracked_games]
        user_matrix = np.array([user_vector]) # Ölçü: (1, oyun_sayı)
        
        # Sistemdə təlim olunmuş bütöv Feature Matrix ilə cari istifadəçinin oxşarlığını bir saniyədə hesablayır
        similarities = cosine_similarity(user_matrix, self.feature_matrix)[0]
        
        ml_results = []
        for index, score in enumerate(similarities):
            ml_results.append({
                "username": self.players_metadata[index]["username"],
                "steamid": self.players_metadata[index]["steamid"],
                "match_score": round(float(score) * 100, 1),
                "method": "Machine Learning (Cosine Similarity)"
            })
            
        # Skorları ən yüksəkdən aşağıya sıralayıb ən yaxşı N nəfəri qaytarır
        return sorted(ml_results, key=lambda x: x["match_score"], reverse=True)[:top_n]


# --- 🧪 MODELİN İŞƏ SALINMASI VƏ SINAQDAN KEÇİRİLMƏSİ ---
if __name__ == "__main__":
    # Əsas oyun siyahımız
    TRACKED_APPS = [730, 570, 578080, 105600]
    
    # 1. AI Modelimizi yaradırıq
    matchmaker_model = SteamMatchmakerAI(tracked_games=TRACKED_APPS)
    
    # 2. Modeli mövcud verilənlər bazamızla TƏLİM (TRAIN) edirik
    matchmaker_model.train(RAW_PLAYER_DATA)
    
    print("\n" + "="*50)
    print("SINAQ 1: Çoxlu Dota 2 saatı olan yeni istifadəçi qeydiyyatdan keçdikdə:")
    print("="*50)
    
    dota_player_json = {
        "response": {
            "game_count": 1,
            "games": [
                {"appid": 570, "playtime_forever": 95000} # Dota 2 aşiqi (Aysel_MOBA və Zahra_Dota_Queen-ə bənzəməlidir)
            ]
        }
    }
    
    predictions_1 = matchmaker_model.predict_best_matches(dota_player_json, top_n=3)
    for idx, match in enumerate(predictions_1, 1):
        print(f"{idx}. {match['username']} | Uyğunluq: %{match['match_score']} | Metod: {match['method']}")

    print("\n" + "="*50)
    print("SINAQ 2: Profili gizli olan və janr olaraq 'Strategy/Co-Op' seçən istifadəçi:")
    print("="*50)
    
    private_user_json = {} # Boş gələn API datası
    predictions_2 = matchmaker_model.predict_best_matches(private_user_json, fallback_genre="Strategy/Co-Op", top_n=2)
    for idx, match in enumerate(predictions_2, 1):
        print(f"{idx}. {match['username']} | Uyğunluq: %{match['match_score']} | Metod: {match['method']}")
