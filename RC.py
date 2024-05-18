import base64
import os

import tkinter as tk
import random
import requests
import urllib3

from PIL import Image, ImageTk


BACKGROUND = 'gray'

icons = []
item_past_labels = []
all_completed_items = []
random_end_items_array = []
keystones = []
rune_tree = []
runes = []
roles = []
rune_ids = {
    "Electrocute": 8112,
    "Predator": 8124,
    "Dark Harvest": 8128,
    "Hail Of Blades": 9923,
    "Cheap Shot": 8126,
    "Taste Of Blood": 8139,
    "Sudden Impact": 8143,
    "Zombie Ward": 8136,
    "Ghost Poro": 8120,
    "Eyeball Collection": 8138,
    "Treasure Hunter": 8135,
    "Ingenious Hunter": 8134,
    "Relentless Hunter": 8105,
    "Ultimate Hunter": 8106,
    "Glacial Augment": 8351,
    "Unsealed Spellbook": 8360,
    "First Strike": 8369,
    "Triple Tonic": 8313,
    "Hextech Flashtraption": 8306,
    "Magical Footwear": 8304,
    "Perfect Timing": 8313,
    "Futures Market": 8321,
    "Minion Dematerializer": 8316,
    "Biscuit Delivery": 8345,
    "Cosmic Insight": 8347,
    "Approach Velocity": 8410,
    "Time Warp Tonic": 8352,
    "Press The Attack": 8005,
    "Lethal Tempo": 8008,
    "Fleet Footwork": 8021,
    "Conqueror": 8010,
    "Overheal": 9101,
    "Triumph": 9111,
    "Presence Of Mind": 8009,
    "Legend Alacrity": 9104,
    "Legend Tenacity": 9105,
    "Legend Bloodline": 9103,
    "Coup De Grace": 8014,
    "Cut Down": 8017,
    "Last Stand": 8299,
    "Grasp Of The Undying": 8437,
    "Aftershock": 8439,
    "Guardian": 8465,
    "Demolish": 8446,
    "Font Of Life": 8463,
    "Shield Bash": 8401,
    "Conditioning": 8429,
    "Second Wind": 8444,
    "Bone Plating": 8473,
    "Overgrowth": 8451,
    "Revitalize": 8453,
    "Unflinching": 8242,
    "Summon Aery": 8214,
    "Arcane Comet": 8229,
    "Phase Rush": 8230,
    "Nullifying Orb": 8224,
    "Manaflow Band": 8226,
    "Nimbus Cloak": 8275,
    "Transcendence": 8210,
    "Celerity": 8234,
    "Absolute Focus": 8233,
    "Scorch": 8237,
    "Waterwalking": 8232,
    "Gathering Storm": 8236,
    "Adaptive Force": 5008,
    "Attack Speed": 5005,
    "Ability Haste": 5007,
    "Movement Speed": 5010,
    "Health Scaling": 5001,
    "Health": 5011,
    "Tenacity And Slow Resist": 5013
}
expensive_starting_items = {
    "Amplifying Tome": 400,
    "Corrupting Potion": 500,
    "Cull": 450,
    "Dark Seal": 350,
    "Dorans Blade": 450,
    "Dorans Ring": 400,
    "Dorans Shield": 450,
    "World Atlas": 450,
    "Boots Of Speed": 300,
    "Long Sword": 350,
    "Ruby Crystal": 400,
    "Sapphire Crystal": 350
}
cheap_starting_items = {
    "Control Ward": 75,
    "Health Potion": 50,
    "Refillable Potion": 150,

}
starting_items_array = []
jungle_items = {
    'Gustwalker Hatchling': 450,
    'Mosstomper Seedling': 450,
    'Scorchclaw Pup': 450
}
past_labels = []
shards = []
past_starting_items = []
past_spells = []
summoner_spells = []
port = ""
auth = ""
encoded_auth = ""
icons_directory = 'lol-icons'
c_items_directory = 'lol-items'
s_items_directory = 'starting-items'
role_directory = 'lol-roles'
runes_directory = 'lol-runes'
spells_directory = 'lol-spells'
limitations = {
    "Annul": ["Banshee's Veil", "Edge of Night"],
    "Blight": ["Blighting Jewel", "Cryptbloom", "Terminus", "Void Staff"],
    "Boots": ["Berserkers Greaves", "Boots Boots", "Boots of Swiftness", "Ionian Boots of Lucidity", "Mercurys Treads", "Mobility Boots", "Plated Steelcaps", "Sorcerer's Shoes"],
    "Fatality": ["Last Whisper", "Black Cleaver", "Lord Dominiks Regards", "Mortal Reminder", "Seryldas Grudge", "Terminus"],
    "Hydra": ["Tiamat", "Profane Hydra", "Ravenous Hydra", "Stridebreaker", "Titanic Hydra"],
    "Immolate": ["Sunfire Aegis", "Hollow Radiance"],
    "Support": ["World Atlas", "Runic Compass", "Bounty of Worlds", "Bloodsong", "Celestial Opposition", "Dream Maker", "Solstice Sleigh", "Zaz Zaks Realmspike"],
    "Lifeline": ["Archangels Staff", "Hexdrinker", "Immortal Shieldbow", "Maw of Malmortius", "Seraphs Embrace", "Steraks Gage"],
    "Manaflow": ["Archangels Staff", "Fimbulwinter", "Manamune", "Muramana", "Seraphs Embrace", "Tear of the Goddess", "Winters Approach"],
    "Momentum": ["Dead Mans Plate", "Trailblazer"],
    "Spellblade": ["Sheen", "Bloodsong", "Essence Reaver", "Iceborn Gauntlet", "Lich Bane", "Trinity Force"],
    "Unbounded": ["Infinity Edge", "Navori Quickblades"]
}
# iterate over files in
# that directory
for icon in os.listdir(icons_directory):
    f = os.path.join(icons_directory, icon)
    icons.append(f)
for role in os.listdir(role_directory):
    f = os.path.join(role_directory, role)
    roles.append(f)
for end_item in os.listdir(c_items_directory):
    f = os.path.join(c_items_directory, end_item)
    all_completed_items.append(f)
for spell in os.listdir(spells_directory):
    f = os.path.join(spells_directory, spell)
    summoner_spells.append(f)
def get_specific_png_files(dir, subdirectories):
    png_files = []
    for subdir in subdirectories:
        subdir_path = os.path.join(dir, subdir)
        if os.path.isdir(subdir_path):
            for root, _, files in os.walk(subdir_path):
                for file in files:
                    if file.lower().endswith(".png"):
                        png_files.append(os.path.join(root, file))
    return png_files

subdirectories = ['domination', 'precision', 'resolve', 'inspiration', 'sorcery']
def primary_runes(runes_directory):
    # Define the order of subfolders
    subfolder_order = ["FirstKeystones", "SecondKeystones", "ThirdKeystones", "ForthKeystones"]

    # Iterate over each subfolder in the defined order
    for subfolder_name in subfolder_order:
        # Construct the full path to the subfolder
        subfolder_path = os.path.join(runes_directory, subfolder_name)
        # Check if the subfolder exists
        if os.path.isdir(subfolder_path):
            # Get a list of files in the subfolder
            files = os.listdir(subfolder_path)
            # Filter out directories (if any)
            files = [file for file in files if os.path.isfile(os.path.join(subfolder_path, file)) and file.endswith('.png')]
            # Check if there are files in the subfolder
            if files:
                # Select a random file from the list
                random_file = random.choice(files)
                rune_name = os.path.splitext(random_file)[0]
                # Append the selected file to the rune_tree list
                rune_tree.append(rune_name)
            else:
                print(f"No files found in folder: {subfolder_path}")
        else:
            print(f"Subfolder does not exist: {subfolder_path}")
def secondary_runes(runes_directory):
    # Define the order of subfolders
    sub_folder_path = ["SecondKeystones", "ThirdKeystones", "ForthKeystones"]
    random_folder = random.choice(sub_folder_path)

    # Iterate twice to select two items
    for _ in range(2):
        # Construct the full path to the randomly selected folder
        random_folder_path = os.path.join(runes_directory, random_folder)

        # Check if the random folder exists
        if os.path.isdir(random_folder_path):
            # Get a list of files in the random folder
            files = os.listdir(random_folder_path)
            # Filter out directories and select only files with the ".png" extension
            files = [file for file in files if
                     os.path.isfile(os.path.join(random_folder_path, file)) and file.endswith('.png')]
            # Check if there are files in the random folder
            if files:
                # Select a random file from the list
                random_file = random.choice(files)
                # Append the selected file to the rune_tree list
                rune_name = os.path.splitext(random_file)[0]
                rune_tree.append(rune_name)

        # Remove the selected folder from sub_folder_path to prevent selecting it again
        sub_folder_path.remove(random_folder)

        # Select a new random folder from the updated sub_folder_path
        if sub_folder_path:
            random_folder = random.choice(sub_folder_path)
        else:
            print("No more folders available to select from.")

def shards():
    shard_dir = "lol-runes\\shards"
    shard_subfolders = ["line1","line2","line3"]
    for subfolder_name in shard_subfolders:
        # Construct the full path to the subfolder
        subfolder_path = os.path.join(shard_dir, subfolder_name)

        # Check if the subfolder exists
        if os.path.isdir(subfolder_path):
            # Get a list of files in the subfolder
            files = os.listdir(subfolder_path)
            # Filter out directories and select only files with the ".png" extension
            png_files = [file for file in files if
                         os.path.isfile(os.path.join(subfolder_path, file)) and file.endswith('.png')]
            # Check if there are PNG files in the subfolder
            if png_files:
                # Select a random PNG file from the list
                random_png_file = random.choice(png_files)
                # Remove the ".png" extension from the filename
                png_item_name = os.path.splitext(random_png_file)[0]
                # Append the selected PNG item to the shard_items list
                rune_tree.append(png_item_name)

def import_runes(payload):
    #GET RUNE ID

    set_rune_url = f"https://127.0.0.1:{port}/lol-perks/v1/pages"
    get_rune_id_url = f"https://127.0.0.1:{port}/lol-perks/v1/currentpage"

    # Define the headers
    headers = {
        "Accept": "application/json",
        "Authorization": f"Basic {encoded_auth}"
    }
    response = requests.get(get_rune_id_url, headers=headers, verify=False)
    response.raise_for_status()
    response = response.json()
    delete_rune_id = f"https://127.0.0.1:{port}/lol-perks/v1/pages/{response['id']}"

    delete = requests.delete(delete_rune_id, headers=headers, verify=False)
    delete.raise_for_status()
    setrune = requests.post(set_rune_url, json=payload, headers=headers, verify=False)
    setrune.raise_for_status()


def get_data():
    global port,auth,encoded_auth

    try:
        file = open("C:/Riot Games/League of Legends/lockfile")
        text = file.readline()

        text = text[18:len(text) - 1 - 5]
        data = text.split(':')
        port = data[0]
        auth = data[1]
        print(auth)
        encoded_auth = base64.b64encode(f"riot:{auth}".encode()).decode()
        print(encoded_auth)

        print(port)
    except (IndentationError,FileNotFoundError,UnboundLocalError) as error:
        print('File dont exist')








def button2_click(payload,rune):
    import_runes(payload)
    rune.clear()
def button_click():
    get_data()
    global past_labels
    gold = 500
    cant_buy = False
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.destroy()

    icon_index = random.randint(0, len(icons) - 1)
    role_index = random.randint(0, len(roles) - 1)
    spell_index = random.randint(0, len(summoner_spells) - 1)
    spell_index2 = random.randint(0, len(summoner_spells) - 1)
    # c_items_index = random.randint(0,len(completed_items) -1)
    # keystones_index = random.randint(0,len(keys) -1)
    # runes_index = random.randint(0,len(icons) -1)

    # Champion icon
    champion_image_path = icons[icon_index]
    champ_image = Image.open(champion_image_path)
    champ_image = champ_image.resize((70, 70))
    champ_image = ImageTk.PhotoImage(champ_image)
    obj = tk.Label(root, image=champ_image, bg=BACKGROUND)
    obj.image = champ_image
    obj.place(x=20, y=35)
    # -----------------------------------------------------------
    # Champion Name
    champ_name_path_split = champion_image_path.split("lol-icons\\")
    champ_filename = champ_name_path_split[-1]
    name = champ_filename.split(".png")[0]
    champion_name_label = tk.Label(root, text=name, bg=BACKGROUND, font=(("Times New Roman"), 16, 'bold'))
    champion_name_label.place(x=25, y=0)

    # ------------------------------------------------------------
    # Role Icon
    role_image_path = roles[role_index]
    role_image = Image.open(role_image_path)
    role_image = role_image.resize((50, 50))
    role_image = ImageTk.PhotoImage(role_image)
    role_image_label = tk.Label(root, image=role_image, bg=BACKGROUND)
    role_image_label.image = role_image
    role_image_label.place(x=25, y=110)
    # ------------------------------------------------------------
    # Role Name
    role_name_path_split = role_image_path.split("lol-roles\\")
    # Extract the name portion from the last part of the path
    role_filename = role_name_path_split[-1]
    # Remove the file extension ()
    role_name = role_filename.split(".")[0]
    role_label = tk.Label(root, text=role_name, bg=BACKGROUND, font=(("Times New Roman"), 16, 'bold'))
    role_label.place(x=25, y=170)

    # ------------------------------------------------------------
    # Summoner Spells
    for past_spell in past_labels:
        past_spell.destroy()
    # Only Jungle-Role Smite
    while role_name != 'Jungle' and (summoner_spells[spell_index] == 'lol-spells\\Smite.png' or summoner_spells[
        spell_index2] == 'lol-spells\\Smite.png'):
        spell_index = random.randint(0, len(summoner_spells) - 1)
        spell_index2 = random.randint(0, len(summoner_spells) - 1)


    # Double Smite Check
    while role_name == "Jungle" and summoner_spells[spell_index] == 'lol-spells\\Smite.png':
        spell_index = random.randint(0, len(summoner_spells) - 1)
        print('in cycle DOUBLE SMITE CHECK')
    spell_image_path = summoner_spells[spell_index]
    spell_image = Image.open(spell_image_path)
    spell_image = spell_image.resize((40, 40))
    spell_image = ImageTk.PhotoImage(spell_image)
    spell_image_label = tk.Label(root, image=spell_image, bg=BACKGROUND)
    spell_image_label.image = spell_image
    spell_image_label.place(x=150, y=35)
    #past_spells.append(spell_image_label)
    # Summoner Spells 2

    if role_name == "Jungle":
        spell_image_path2 = 'lol-spells\\Smite.png'
        spell_image2 = Image.open(spell_image_path2)
        spell_image2 = spell_image2.resize((40, 40))
        spell_image2 = ImageTk.PhotoImage(spell_image2)
        spell_image_label2 = tk.Label(root, image=spell_image2, bg=BACKGROUND)
        spell_image_label.image2 = spell_image2
        spell_image_label2.place(x=190, y=35)
        past_spells.append(spell_image_label2)
    else:
        while summoner_spells[spell_index2] == summoner_spells[spell_index]:
            spell_index2 = random.randint(0, len(summoner_spells) - 1)
            if summoner_spells[spell_index2] == 'lol-spells\\Smite.png':
                print("SMITE AFTER ROLLL")
                continue

        spell_image_path2 = summoner_spells[spell_index2]
        spell_image2 = Image.open(spell_image_path2)
        spell_image2 = spell_image2.resize((40, 40))
        spell_image2 = ImageTk.PhotoImage(spell_image2)
        spell_image_label2 = tk.Label(root, image=spell_image2, bg=BACKGROUND)
        spell_image_label.image2 = spell_image2
        spell_image_label2.place(x=190, y=35)
        past_spells.append(spell_image_label2)


    # Summoner Spell Label
    spell_text_label = tk.Label(root, text="Spells", bg=BACKGROUND, font=(("Times New Roman"), 16, 'bold'))
    spell_text_label.place(x=165, y=5)
    # ------------------------------------------------------------------------
    # Starting Items

    health_pot = 0
    control_wards = 0
    all_starting_items = []
    while gold >= 300:

        if role_name == 'Jungle':
            item = random.choice(list(jungle_items.items()))
        elif role_name == "Support":
            item = ("World Atlas", 450)
        else:
            item = random.choice(list(expensive_starting_items.items()))

        if item[0] == "World Atlas" and role_name != "Support":
            continue
        gold -= item[1]
        all_starting_items.append(item[0])
    while gold != 0:
        item = random.choice(list(cheap_starting_items.items()))

        if (item[0] == "Health Potion") and "Refillable Potion" in all_starting_items:

            break
        elif (item[0] == "Refillable Potion") and "Health Potion" in all_starting_items:

            continue


        if item[0] == "Health Potion" and gold >= 50:
            health_pot += 1

        elif item[0] == "Control Ward" and gold >= 75:
            control_wards += 1

        if gold <= 49:
            break
        if item[1] > gold:
            continue
        gold -= item[1]
        if all_starting_items.__contains__(item[0]):
            continue

        all_starting_items.append(item[0])


    # Item 1
    for past_items in past_starting_items:
        past_items.destroy()
    if len(all_starting_items) == 1:
        for starting_items_loop in all_starting_items:
            starting_items_array.append(f"starting-items\\{starting_items_loop}.png")
        starting_item1 = starting_items_array[0]
        starting_item1_image = Image.open(starting_item1)
        starting_item1_image = starting_item1_image.resize((50, 50))
        starting_item1_image = ImageTk.PhotoImage(starting_item1_image)
        starting_item1_image_label = tk.Label(root, image=starting_item1_image, bg=BACKGROUND)
        starting_item1_image_label.image = starting_item1_image
        starting_item1_image_label.place(x=260, y=30)
        past_starting_items.append(starting_item1_image_label)
        item_count_label = tk.Label(root, text="1", bg="White", font=(("Times New Roman"), 15, 'bold'))
        item_count_label.place(x=300,y=65)

    elif len(all_starting_items) == 2:
        for starting_items_loop in all_starting_items:
            starting_items_array.append(f"starting-items\\{starting_items_loop}.png")
        starting_item1 = starting_items_array[0]
        starting_item1_image = Image.open(starting_item1)
        starting_item1_image = starting_item1_image.resize((50, 50))
        starting_item1_image = ImageTk.PhotoImage(starting_item1_image)
        starting_item1_image_label = tk.Label(root, image=starting_item1_image, bg=BACKGROUND)
        starting_item1_image_label.image = starting_item1_image
        starting_item1_image_label.place(x=260, y=30)
        past_starting_items.append(starting_item1_image_label)
        starting_item2 = starting_items_array[1]  # Assuming starting_items_array contains file paths to images
        starting_item2_image = Image.open(starting_item2)
        starting_item2_image = starting_item2_image.resize((50, 50))
        starting_item2_image = ImageTk.PhotoImage(starting_item2_image)
        starting_item2_image_label = tk.Label(root, image=starting_item2_image, bg=BACKGROUND)
        starting_item2_image_label.image = starting_item2_image
        starting_item2_image_label.place(x=310, y=30)
        past_starting_items.append(starting_item2_image_label)

        # Item Numbers
        if starting_items_array[1] == 'starting-items\\Health Potion.png' and health_pot > 1:
            # Label for Starting Item Count
            item_count_label = tk.Label(root, text=health_pot, bg="White", font=(("Times New Roman"), 15, 'bold'))
            item_count_label.place(x=350, y=65)


        elif starting_items_array[1] == 'starting-items\\Control Ward.png' and control_wards > 1:
            item_count_label = tk.Label(root, text=control_wards, bg="White", font=(("Times New Roman"), 15, 'bold'))

            item_count_label.place(x=350, y=65)
        else:
            item_count_label = tk.Label(root, text="1", bg="White", font=(("Times New Roman"), 15, 'bold'))

            item_count_label.place(x=350, y=65)

    # Item 3
    elif len(all_starting_items) == 3:
        for starting_items_loop in all_starting_items:
            starting_items_array.append(f"starting-items\\{starting_items_loop}.png")
        starting_item1 = starting_items_array[0]
        starting_item1_image = Image.open(starting_item1)
        starting_item1_image = starting_item1_image.resize((50, 50))
        starting_item1_image = ImageTk.PhotoImage(starting_item1_image)
        starting_item1_image_label = tk.Label(root, image=starting_item1_image, bg=BACKGROUND)
        starting_item1_image_label.image = starting_item1_image
        starting_item1_image_label.place(x=260, y=30)
        past_starting_items.append(starting_item1_image_label)
        starting_item2 = starting_items_array[1]  # Assuming starting_items_array contains file paths to images
        starting_item2_image = Image.open(starting_item2)
        starting_item2_image = starting_item2_image.resize((50, 50))
        starting_item2_image = ImageTk.PhotoImage(starting_item2_image)
        starting_item2_image_label = tk.Label(root, image=starting_item2_image, bg=BACKGROUND)
        starting_item2_image_label.image = starting_item2_image
        starting_item2_image_label.place(x=310, y=30)
        past_starting_items.append(starting_item2_image_label)
        starting_item3 = starting_items_array[2]  # Assuming starting_items_array contains file paths to images
        starting_item3_image = Image.open(starting_item3)
        starting_item3_image = starting_item3_image.resize((50, 50))
        starting_item3_image = ImageTk.PhotoImage(starting_item3_image)
        starting_item3_image_label = tk.Label(root, image=starting_item3_image, bg=BACKGROUND)
        starting_item3_image_label.image = starting_item3_image
        starting_item3_image_label.place(x=360, y=30)
        past_starting_items.append(starting_item3_image_label)

        if (starting_items_array[1] == 'starting-items\\Control Ward.png') and (starting_items_array[2] == 'starting-items\\Health Potion.png'):
            item_count_label = tk.Label(root, text=control_wards, bg="White", font=(("Times New Roman"), 15, 'bold'))
            item_count_label.place(x=350,y=65)
            item_count_label2 = tk.Label(root, text=health_pot, bg="White", font=(("Times New Roman"), 15, 'bold'))
            item_count_label2.place(x=400,y=65)
        elif (starting_items_array[1] == 'starting-items\\Health Potion.png') and (starting_items_array[2] == 'starting-items\\Control Ward.png'):
            item_count_label = tk.Label(root, text=control_wards, bg="White", font=(("Times New Roman"), 15, 'bold'))
            item_count_label.place(x=350,y=65)
            item_count_label2 = tk.Label(root, text=health_pot, bg="White", font=(("Times New Roman"), 15, 'bold'))
            item_count_label2.place(x=400,y=65)
        #case 1 -> boots 300 , 2 control wards (150), 1 p (50)
        #case 2 -> boots 300 , 1 control wards (150), 2 p (50)
        #case 3 -> boots 300 , 1 p (50), 2 control wards (150)
        #case 4 -> boots 300 , 2 p (50), 1 control wards (150),
        #ELSE 1 pot, 1 control ward
    all_starting_items.clear()
    starting_items_array.clear()

    past_labels = [champion_name_label, role_label]
# ----------------------------------------------------------------
    # END ITEMS
    annul_counter = 0
    blight_counter = 0
    boots_counter = 0
    fatality_counter = 0
    hydra_counter = 0
    immolate_counter = 0
    lifeline_counter = 0
    manaflow_counter = 0
    momentum_counter = 0
    spellblade_counter = 0
    unbounded_counter = 0
    support_items = ["lol-items\\Solstice Sleigh.png", "lol-items\\Trailblazer.png", "lol-items\\Dream Maker.png", "lol-items\\Bounty of Worlds.png", "lol-items\\Zaz Zaks Realmspike.png"]
    boots = ["lol-items\\Plated Steelcaps.png", "lol-items\\Sorcerers Shoes.png", "lol-items\\Berserkers Greaves.png", "lol-items\\Boots of Swiftness.png", "lol-items\\Mobility Boots.png", "lol-items\\Ionian Boots of Lucidity.png", "lol-items\\Mercurys Treads.png"]
    x = 0
    while len(random_end_items_array) < 6:
        random_end_item = random.randint(0, len(all_completed_items) - 1)
        item = all_completed_items[random_end_item]
        if len(random_end_items_array) == 1:
            item = random.choice(boots)
            random_end_items_array.append(item)
        # Check if it's a support role and the item is a support item
        elif role_name == 'Support' and len(random_end_items_array) ==0:
            item = random.choice(support_items)
            # For support role, append the item directly
            random_end_items_array.append(item)
        elif role_name == 'Support' and len(random_end_items_array) >0:
            item = all_completed_items[random_end_item]
            if item in random_end_items_array:
                continue
            else:
            # For support role, append the item directly
                random_end_items_array.append(item)
        elif role_name != 'Support' and item in ["lol-items\\Solstice Sleigh.png", "lol-items\\Trailblazer.png",
                                                 "lol-items\\Dream Maker.png", "lol-items\\Bounty of Worlds.png",
                                                 "lol-items\\Zaz Zaks Realmspike.png"]:

            # For non-support roles, if a support item is encountered, continue the loop
            continue
        elif item in boots:

            continue

        else:
            # For non-support roles, append the item
            if item not in random_end_items_array:
                if item in ["Banshee's Veil", "Edge of Night"]:
                    if annul_counter < 1:
                        annul_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Blighting Jewel", "Cryptbloom", "Terminus", "Void Staff"]:
                    if blight_counter < 1:
                        blight_counter += 1
                        random_end_items_array.append(item)
                elif item in boots:
                    if boots_counter < 1:
                        boots_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Black Cleaver", "Lord Dominik's Regards", "Mortal Reminder",
                              "Serylda's Grudge"]:
                    if fatality_counter < 1:
                        fatality_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Profane Hydra", "Ravenous Hydra", "Stridebreaker", "Titanic Hydra"]:
                    if hydra_counter < 1:
                        hydra_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Sunfire Aegis", "Hollow Radiance"]:
                    if immolate_counter < 1:
                        immolate_counter += 1
                        random_end_items_array.append(item)
                elif item in ["World Atlas", "Runic Compass", "Bounty of Worlds", "Bloodsong", "Celestial Opposition",
                              "Dream Maker", "Solstice Sleigh", "Zaz Zaks Realmspike"]:
                    if lifeline_counter < 1:
                        lifeline_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Archangel's Staff", "Hexdrinker", "Immortal Shieldbow", "Maw of Malmortius",
                              "Seraph's Embrace", "Sterak's Gage"]:
                    if manaflow_counter < 1:
                        manaflow_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Dead Man's Plate", "Trailblazer"]:
                    if momentum_counter < 1:
                        momentum_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Essence Reaver", "Iceborn Gauntlet", "Lich Bane", "Trinity Force"]:
                    if spellblade_counter < 1:
                        spellblade_counter += 1
                        random_end_items_array.append(item)
                elif item in ["Infinity Edge", "Navori Quickblades"]:
                    if unbounded_counter < 1:
                        unbounded_counter += 1
                        random_end_items_array.append(item)
                else:
                    random_end_items_array.append(item)

        x += 1
        if x >= 100:
            break  # To prevent infinite loop in case of issues

    image_paths = [random_end_items_array[0], random_end_items_array[1], random_end_items_array[2],
                   random_end_items_array[3], random_end_items_array[4], random_end_items_array[5]]

    # Calculate the number of rows and columns
    num_rows = 2
    num_cols = 3

    # Calculate the width and height of each image
    image_width = 50
    image_height = 50

    # Calculate the horizontal and vertical spacing between images
    horizontal_spacing = 3
    vertical_spacing = 3

    # Loop to create labels for each image
    for i in range(len(image_paths)):
        # Open image and resize
        image = Image.open(image_paths[i])
        image = image.resize((image_width, image_height))

        # Convert image to Tkinter PhotoImage
        image_tk = ImageTk.PhotoImage(image)

        # Calculate the row and column indices
        row_index = i // num_cols
        col_index = i % num_cols

        # Calculate the x and y coordinates for placing the label
        x_coord = col_index * (image_width + horizontal_spacing)
        y_coord = row_index * (image_height + vertical_spacing)

        item_name = os.path.splitext(os.path.basename(image_paths[i]))[0]

        # Create label and place it
        label = tk.Label(root, image=image_tk, bg=BACKGROUND)
        label.image = image_tk  # Keep a reference to avoid garbage collection
        label.place(x=x_coord + 440, y=y_coord + 20)

        # Bind click event to display item name
        label.bind("<Button-1>", lambda event, i_name=item_name: display_item_name(i_name))

    random_end_items_array.clear()
    # ---------------------------------------------------------------------
    # RUNES
    dir = "lol-runes"
    primary_id = 0
    secondary_id = 0
    rune_tree_ids =[]
    rune_paths = ["domination","sorcery","inspiration","precision","resolve"]
    primary_path = random.choice(rune_paths)

    secondary_path = random.choice(rune_paths)
    while primary_path == secondary_path:
        secondary_path = random.choice(rune_paths)
    if primary_path == "domination":
        primary_id = 8100
        runes_directory = "lol-runes\\domination"
        primary_runes(runes_directory)

    elif primary_path == "sorcery":
        primary_id = 8200
        runes_directory = "lol-runes\\sorcery"
        primary_runes(runes_directory)

    elif primary_path == "inspiration":
        primary_id = 8300
        runes_directory = "lol-runes\\inspiration"
        primary_runes(runes_directory)

    elif primary_path == "precision":
        primary_id = 8000
        runes_directory = "lol-runes\\precision"
        primary_runes(runes_directory)

    elif primary_path == "resolve":
        primary_id = 8400
        runes_directory = "lol-runes\\resolve"
        primary_runes(runes_directory)

    if secondary_path == "domination":
        secondary_id = 8100
        runes_directory = "lol-runes\\domination"
        secondary_runes(runes_directory)

    elif secondary_path == "precision":
        secondary_id = 8000
        runes_directory = "lol-runes\\precision"
        secondary_runes(runes_directory)

    elif secondary_path == "inspiration":
        secondary_id = 8300
        runes_directory = "lol-runes\\inspiration"
        secondary_runes(runes_directory)

    elif secondary_path == "resolve":
        secondary_id = 8400
        runes_directory = "lol-runes\\resolve"
        secondary_runes(runes_directory)

    elif secondary_path == "sorcery":
        secondary_id = 8200
        runes_directory = "lol-runes\\sorcery"
        secondary_runes(runes_directory)
    shards()
    payload = {
        "selectedPerkIds": rune_tree_ids,
        "primaryStyleId": primary_id,
        "subStyleId": secondary_id,
        "name": f"{rune_tree[0].upper()} : {name.upper()}",
        "current": True
    }
    for i in range(len(rune_tree)):
        for p in rune_ids.keys():
            if rune_tree[i] == p:
                rune_tree_ids.append(rune_ids.get(p))
                break

    urllib3.disable_warnings()

    #RUNE LABELS
    #adding .png to each rune in rune tree to make them as a image label
    for i in range(len(rune_tree)):
        rune_tree[i] = f"{rune_tree[i]}.png"
    png_files = get_specific_png_files(dir, subdirectories)
    rune_tree_pngs = [os.path.basename(png_file) for png_file in png_files]
    increment = 0
    labels = []
    index = 0
    for rune in rune_tree:

        for png_file in png_files:
            basename = os.path.basename(png_file)

            if basename == rune and len(labels) == 0:
                img = Image.open(png_file)
                img = img.resize((100, 100))
                img = ImageTk.PhotoImage(img)
                label = tk.Label(root, image=img,bg=BACKGROUND)
                label.image = img  # Keep a reference to avoid garbage collection
                label.place(x=120+increment, y=180)
                labels.append(label)
                increment += 50  # Increment the y-coordinate for the next label
                break  # Break the loop once the PNG file is found
            elif basename == rune:
                img = Image.open(png_file)
                img = img.resize((50, 50))
                img = ImageTk.PhotoImage(img)
                label = tk.Label(root, image=img, bg=BACKGROUND)
                label.image = img  # Keep a reference to avoid garbage collection
                label.place(x=160 + increment, y=200)
                labels.append(label)
                increment += 50  # Increment the y-coordinate for the next label
                break  # Break the loop once the PNG file is found


    #Button 2 create
    button2 = tk.Button(root, text="IMPORT RUNES TO LOL", command=lambda: button2_click(payload, rune_tree_ids), width=30,
                        height=3)
    button2.place(x=350, y=300)

    rune_tree.clear()

def display_item_name(item_name):

    for x in item_past_labels:
        x.destroy()
    label_item_name = tk.Label(root,text=item_name,bg=BACKGROUND,font=(("Times New Roman"), 13, 'bold'),fg="black")
    label_item_name.place(x=420,y=130)
    item_past_labels.append(label_item_name)

# Root Options
root = tk.Tk()
root.title("Champion Details")
root.geometry('630x400')
root.configure(bg=BACKGROUND)

# GENERATE BUTTON
button = tk.Button(root, text="Generate", command=button_click, width=30, height=3)
button.pack()
button.place(x=100, y=300)

# Run the Tkinter event loop
root.mainloop()
