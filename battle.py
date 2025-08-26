import ndspy.narc
import struct

speciesNamesList = [
    # Gen 1
    "Bulbasaur", "Ivysaur", "Venusaur", "Charmander", "Charmeleon", "Charizard", "Squirtle", "Wartortle", "Blastoise",
    "Caterpie", "Metapod", "Butterfree", "Weedle", "Kakuna", "Beedrill", "Pidgey", "Pidgeotto", "Pidgeot", "Rattata",
    "Raticate", "Spearow", "Fearow", "Ekans", "Arbok", "Pikachu", "Raichu", "Sandshrew", "Sandslash", "Nidoran♀",
    "Nidorina", "Nidoqueen", "Nidoran♂", "Nidorino", "Nidoking", "Clefairy", "Clefable", "Vulpix", "Ninetales",
    "Jigglypuff", "Wigglytuff", "Zubat", "Golbat", "Oddish", "Gloom", "Vileplume", "Paras", "Parasect", "Venonat",
    "Venomoth", "Diglett", "Dugtrio", "Meowth", "Persian", "Psyduck", "Golduck", "Mankey", "Primeape", "Growlithe",
    "Arcanine", "Poliwag", "Poliwhirl", "Poliwrath", "Abra", "Kadabra", "Alakazam", "Machop", "Machoke", "Machamp",
    "Bellsprout", "Weepinbell", "Victreebel", "Tentacool", "Tentacruel", "Geodude", "Graveler", "Golem", "Ponyta",
    "Rapidash", "Slowpoke", "Slowbro", "Magnemite", "Magneton", "Farfetch'd", "Doduo", "Dodrio", "Seel", "Dewgong",
    "Grimer", "Muk", "Shellder", "Cloyster", "Gastly", "Haunter", "Gengar", "Onix", "Drowzee", "Hypno", "Krabby",
    "Kingler", "Voltorb", "Electrode", "Exeggcute", "Exeggutor", "Cubone", "Marowak", "Hitmonlee", "Hitmonchan",
    "Lickitung", "Koffing", "Weezing", "Rhyhorn", "Rhydon", "Chansey", "Tangela", "Kangaskhan", "Horsea", "Seadra",
    "Goldeen", "Seaking", "Staryu", "Starmie", "Mr. Mime", "Scyther", "Jynx", "Electabuzz", "Magmar", "Pinsir",
    "Tauros", "Magikarp", "Gyarados", "Lapras", "Ditto", "Eevee", "Vaporeon", "Jolteon", "Flareon", "Porygon",
    "Omanyte", "Omastar", "Kabuto", "Kabutops", "Aerodactyl", "Snorlax", "Articuno", "Zapdos", "Moltres", "Dratini",
    "Dragonair", "Dragonite", "Mewtwo", "Mew",
    # Gen 2
    "Chikorita", "Bayleef", "Meganium", "Cyndaquil", "Quilava", "Typhlosion", "Totodile", "Croconaw", "Feraligatr",
    "Sentret", "Furret", "Hoothoot", "Noctowl", "Ledyba", "Ledian", "Spinarak", "Ariados", "Crobat", "Chinchou",
    "Lanturn", "Pichu", "Cleffa", "Igglybuff", "Togepi", "Togetic", "Natu", "Xatu", "Mareep", "Flaaffy", "Ampharos",
    "Bellossom", "Marill", "Azumarill", "Sudowoodo", "Politoed", "Hoppip", "Skiploom", "Jumpluff", "Aipom", "Sunkern",
    "Sunflora", "Yanma", "Wooper", "Quagsire", "Espeon", "Umbreon", "Murkrow", "Slowking", "Misdreavus", "Unown",
    "Wobbuffet", "Girafarig", "Pineco", "Forretress", "Dunsparce", "Gligar", "Steelix", "Snubbull", "Granbull",
    "Qwilfish", "Scizor", "Shuckle", "Heracross", "Sneasel", "Teddiursa", "Ursaring", "Slugma", "Magcargo", "Swinub",
    "Piloswine", "Corsola", "Remoraid", "Octillery", "Delibird", "Mantine", "Skarmory", "Houndour", "Houndoom",
    "Kingdra", "Phanpy", "Donphan", "Porygon2", "Stantler", "Smeargle", "Tyrogue", "Hitmontop", "Smoochum", "Elekid",
    "Magby", "Miltank", "Blissey", "Raikou", "Entei", "Suicune", "Larvitar", "Pupitar", "Tyranitar", "Lugia", "Ho-Oh",
    "Celebi",
    # Gen 3
    "Treecko", "Grovyle", "Sceptile", "Torchic", "Combusken", "Blaziken", "Mudkip", "Marshtomp", "Swampert",
    "Poochyena", "Mightyena", "Zigzagoon", "Linoone", "Wurmple", "Silcoon", "Beautifly", "Cascoon", "Dustox", "Lotad",
    "Lombre", "Ludicolo", "Seedot", "Nuzleaf", "Shiftry", "Taillow", "Swellow", "Wingull", "Pelipper", "Ralts",
    "Kirlia", "Gardevoir", "Surskit", "Masquerain", "Shroomish", "Breloom", "Slakoth", "Vigoroth", "Slaking",
    "Nincada", "Ninjask", "Shedinja", "Whismur", "Loudred", "Exploud", "Makuhita", "Hariyama", "Azurill", "Nosepass",
    "Skitty", "Delcatty", "Sableye", "Mawile", "Aron", "Lairon", "Aggron", "Meditite", "Medicham", "Electrike",
    "Manectric", "Plusle", "Minun", "Volbeat", "Illumise", "Roselia", "Gulpin", "Swalot", "Carvanha", "Sharpedo",
    "Wailmer", "Wailord", "Numel", "Camerupt", "Torkoal", "Spoink", "Grumpig", "Spinda", "Trapinch", "Vibrava",
    "Flygon", "Cacnea", "Cacturne", "Swablu", "Altaria", "Zangoose", "Seviper", "Lunatone", "Solrock", "Barboach",
    "Whiscash", "Corphish", "Crawdaunt", "Baltoy", "Claydol", "Lileep", "Cradily", "Anorith", "Armaldo", "Feebas",
    "Milotic", "Castform", "Kecleon", "Shuppet", "Banette", "Duskull", "Dusclops", "Tropius", "Chimecho", "Absol",
    "Wynaut", "Snorunt", "Glalie", "Spheal", "Sealeo", "Walrein", "Clamperl", "Huntail", "Gorebyss", "Relicanth",
    "Luvdisc", "Bagon", "Shelgon", "Salamence", "Beldum", "Metang", "Metagross", "Regirock", "Regice", "Registeel",
    "Latias", "Latios",  "Kyogre", "Groudon", "Rayquaza", "Jirachi", "Deoxys",
    # Gen 4
    "Turtwig", "Grotle", "Torterra", "Chimchar", "Monferno", "Infernape", "Piplup", "Prinplup", "Empoleon", "Starly",
    "Staravia", "Staraptor", "Bidoof", "Bibarel", "Kricketot", "Kricketune", "Shinx", "Luxio", "Luxray", "Budew",
    "Roserade", "Cranidos", "Rampardos", "Shieldon", "Bastiodon", "Burmy", "Wormadam", "Mothim", "Combee", "Vespiquen",
    "Pachirisu", "Buizel", "Floatzel", "Cherubi", "Cherrim", "Shellos", "Gastrodon", "Ambipom", "Drifloon", "Drifblim",
    "Buneary", "Lopunny", "Mismagius", "Honchkrow", "Glameow", "Purugly", "Chingling", "Stunky", "Skuntank", "Bronzor",
    "Bronzong", "Bonsly", "Mime Jr.", "Happiny", "Chatot", "Spiritomb", "Gible", "Gabite", "Garchomp", "Munchlax",
    "Riolu", "Lucario", "Hippopotas", "Hippowdon", "Skorupi", "Drapion", "Croagunk", "Toxicroak", "Carnivine", "Finneon",
    "Lumineon", "Mantyke", "Snover", "Abomasnow", "Weavile", "Magnezone", "Lickilicky", "Rhyperior", "Tangrowth",
    "Electivire", "Magmortar", "Togekiss", "Yanmega", "Leafeon", "Glaceon", "Gliscor", "Mamoswine", "Porygon-Z",
    "Gallade", "Probopass", "Dusknoir", "Froslass", "Rotom", "Uxie", "Mesprit", "Azelf", "Dialga", "Palkia", "Heatran",
    "Regigigas", "Giratina", "Cresselia", "Phione", "Manaphy", "Darkrai", "Shaymin", "Arceus",
    # Gen 5
    "Victini", "Snivy", "Servine", "Serperior", "Tepig", "Pignite", "Emboar", "Oshawott", "Dewott", "Samurott", "Patrat",
    "Watchog", "Lillipup", "Herdier", "Stoutland", "Purrloin", "Liepard", "Pansage", "Simisage", "Pansear", "Simisear",
    "Panpour", "Simipour", "Munna", "Musharna", "Pidove", "Tranquill", "Unfezant", "Blitzle", "Zebstrika", "Roggenrola",
    "Boldore", "Gigalith", "Woobat", "Swoobat", "Drilbur", "Excadrill", "Audino", "Timburr", "Gurdurr", "Conkeldurr",
    "Tympole", "Palpitoad", "Seismitoad", "Throh", "Sawk", "Sewaddle", "Swadloon", "Leavanny", "Venipede", "Whirlipede",
    "Scolipede", "Cottonee", "Whimsicott", "Petilil", "Lilligant", "Basculin", "Sandile", "Krokorok", "Krookodile",
    "Darumaka", "Darmanitan", "Maractus", "Dwebble", "Crustle", "Scraggy", "Scrafty", "Sigilyph", "Yamask", "Cofagrigus",
    "Tirtouga", "Carracosta", "Archen", "Archeops", "Trubbish", "Garbodor", "Zorua", "Zoroark", "Minccino", "Cinccino",
    "Gothita", "Gothorita", "Gothitelle", "Solosis", "Duosion", "Reuniclus", "Ducklett", "Swanna", "Vanillite", "Vanillish",
    "Vanilluxe", "Deerling", "Sawsbuck", "Emolga", "Karrablast", "Escavalier", "Foongus", "Amoonguss", "Frillish", "Jellicent",
    "Alomomola", "Joltik", "Galvantula", "Ferroseed", "Ferrothorn", "Klink", "Klang", "Klinklang", "Tynamo", "Eelektrik",
    "Eelektross", "Elgyem", "Beheeyem", "Litwick", "Lampent", "Chandelure", "Axew", "Fraxure", "Haxorus", "Cubchoo", "Beartic",
    "Cryogonal", "Shelmet", "Accelgor", "Stunfisk", "Mienfoo", "Mienshao", "Druddigon", "Golett", "Golurk", "Pawniard",
    "Bisharp", "Bouffalant", "Rufflet", "Braviary", "Vullaby", "Mandibuzz", "Heatmor", "Durant", "Deino", "Zweilous",
    "Hydreigon", "Larvesta", "Volcarona", "Cobalion", "Terrakion", "Virizion", "Tornadus", "Thundurus", "Reshiram", "Zekrom",
    "Landorus", "Kyurem", "Keldeo", "Meloetta", "Genesect"
 ]

move_names = [
    # Gen 1
    "--", "Pound", "Karate Chop", "Double Slap", "Comet Punch", "Mega Punch", "Pay Day", "Fire Punch", "Ice Punch",
    "Thunder Punch", "Scratch", "Vice Grip", "Guillotine", "Razor Wind", "Swords Dance", "Cut", "Gust", "Wing Attack",
    "Whirlwind", "Fly", "Bind", "Slam", "Vine Whip", "Stomp", "Double Kick", "Mega Kick", "Jump Kick", "Rolling Kick",
    "Sand Attack", "Headbutt", "Horn Attack", "Fury Attack", "Horn Drill", "Tackle", "Body Slam", "Wrap", "Take Down",
    "Thrash", "Double-Edge", "Tail Whip", "Poison Sting", "Twineedle", "Pin Missile", "Leer", "Bite", "Growl", "Roar",
    "Sing", "Supersonic", "Sonic Boom", "Disable", "Acid", "Ember", "Flamethrower", "Mist", "Water Gun", "Hydro Pump",
    "Surf", "Ice Beam", "Blizzard", "Psybeam", "Bubble Beam", "Aurora Beam", "Hyper Beam", "Peck", "Drill Peck",
    "Submission", "Low Kick", "Counter", "Seismic Toss", "Strength", "Absorb", "Mega Drain", "Leech Seed", "Growth",
    "Razor Leaf", "Solar Beam", "Poison Powder", "Stun Spore", "Sleep Powder", "Petal Dance", "String Shot",
    "Dragon Rage", "Fire Spin", "Thunder Shock", "Thunderbolt", "Thunder Wave", "Thunder", "Rock Throw", "Earthquake",
    "Fissure", "Dig", "Toxic", "Confusion", "Psychic", "Hypnosis", "Meditate", "Agility", "Quick Attack", "Rage",
    "Teleport", "Night Shade", "Mimic", "Screech", "Double Team", "Recover", "Harden", "Minimize", "Smokescreen",
    "Confuse Ray", "Withdraw", "Defense Curl", "Barrier", "Light Screen", "Haze", "Reflect", "Focus Energy", "Bide",
    "Metronome", "Mirror Move", "Self-Destruct", "Egg Bomb", "Lick", "Smog", "Sludge", "Bone Club", "Fire Blast",
    "Waterfall", "Clamp", "Swift", "Skull Bash", "Spike Cannon", "Constrict", "Amnesia", "Kinesis", "Soft-Boiled",
    "High Jump Kick", "Glare", "Dream Eater", "Poison Gas", "Barrage", "Leech Life", "Lovely Kiss", "Sky Attack",
    "Transform", "Bubble", "Dizzy Punch", "Spore", "Flash", "Psywave", "Splash", "Acid Armor", "Crabhammer",
    "Explosion", "Fury Swipes", "Bonemerang", "Rest", "Rock Slide", "Hyper Fang", "Sharpen", "Conversion", "Tri Attack",
    "Super Fang", "Slash", "Substitute", "Struggle",
    # Gen 2
    "Sketch", "Triple Kick", "Thief", "Spider Web", "Mind Reader",
    "Nightmare", "Flame Wheel", "Snore", "Curse", "Flail", "Conversion 2", "Aeroblast", "Cotton Spore", "Reversal",
    "Spite", "Powder Snow", "Protect", "Mach Punch", "Scary Face", "Feint Attack", "Sweet Kiss", "Belly Drum",
    "Sludge Bomb", "Mud-Slap", "Octazooka", "Spikes", "Zap Cannon", "Foresight", "Destiny Bond", "Perish Song",
    "Icy Wind", "Detect", "Bone Rush", "Lock-On", "Outrage", "Sandstorm", "Giga Drain", "Endure", "Charm", "Rollout",
    "False Swipe", "Swagger", "Milk Drink", "Spark", "Fury Cutter", "Steel Wing", "Mean Look", "Attract", "Sleep Talk",
    "Heal Bell", "Return", "Present", "Frustration", "Safeguard", "Pain Split", "Sacred Fire", "Magnitude",
    "Dynamic Punch", "Megahorn", "Dragon Breath", "Baton Pass", "Encore", "Pursuit", "Rapid Spin", "Sweet Scent",
    "Iron Tail", "Metal Claw", "Vital Throw", "Morning Sun", "Synthesis", "Moonlight", "Hidden Power", "Cross Chop",
    "Twister", "Rain Dance", "Sunny Day", "Crunch", "Mirror Coat", "Psych Up", "Extreme Speed", "Ancient Power",
    "Shadow Ball", "Future Sight", "Rock Smash", "Whirlpool", "Beat Up",
    # Gen 3
    "Fake Out", "Uproar", "Stockpile", "Spit Up", "Swallow", "Heat Wave", "Hail", "Torment", "Flatter", "Will-O-Wisp",
    "Memento", "Facade", "Focus Punch", "Smelling Salts", "Follow Me", "Nature Power", "Charge", "Taunt", "Helping Hand",
    "Trick", "Role Play", "Wish", "Assist", "Ingrain", "Superpower", "Magic Coat", "Recycle", "Revenge", "Brick Break",
    "Yawn", "Knock Off", "Endeavor", "Eruption", "Skill Swap", "Imprison", "Refresh", "Grudge", "Snatch", "Secret Power",
    "Dive", "Arm Thrust", "Camouflage", "Tail Glow", "Luster Purge", "Mist Ball", "Feather Dance", "Teeter Dance",
    "Blaze Kick", "Mud Sport", "Ice Ball", "Needle Arm", "Slack Off", "Hyper Voice", "Poison Fang", "Crush Claw",
    "Blast Burn", "Hydro Cannon", "Meteor Mash", "Astonish", "Weather Ball", "Aromatherapy", "Fake Tears", "Air Cutter",
    "Overheat", "Odor Sleuth", "Rock Tomb", "Silver Wind", "Metal Sound", "Grass Whistle", "Tickle", "Cosmic Power",
    "Water Spout", "Signal Beam", "Shadow Punch", "Extrasensory", "Sky Uppercut", "Sand Tomb", "Sheer Cold", "Muddy Water",
    "Bullet Seed", "Aerial Ace", "Icicle Spear", "Iron Defense", "Block", "Howl", "Dragon Claw", "Frenzy Plant", "Bulk Up",
    "Bounce", "Mud Shot", "Poison Tail", "Covet", "Volt Tackle", "Magical Leaf", "Water Sport", "Calm Mind", "Leaf Blade",
    "Dragon Dance", "Rock Blast", "Shock Wave", "Water Pulse", "Doom Desire", "Psycho Boost",
    # Gen 4
    "Roost", "Gravity", "Miracle Eye", "Wake-Up Slap", "Hammer Arm", "Gyro Ball", "Healing Wish", "Brine", "Natural Gift",
    "Feint", "Pluck", "Tailwind", "Acupressure", "Metal Burst", "U-turn", "Close Combat", "Payback", "Assurance", "Embargo",
    "Fling", "Psycho Shift", "Trump Card", "Heal Block", "Wring Out", "Power Trick", "Gastro Acid", "Lucky Chant", "Me First",
    "Copycat", "Power Swap", "Guard Swap", "Punishment", "Last Resort", "Worry Seed", "Sucker Punch", "Toxic Spikes",
    "Heart Swap", "Aqua Ring", "Magnet Rise", "Flare Blitz", "Force Palm", "Aura Sphere", "Rock Polish", "Poison Jab",
    "Dark Pulse", "Night Slash", "Aqua Tail", "Seed Bomb", "Air Slash", "X-Scissor", "Bug Buzz", "Dragon Pulse", "Dragon Rush",
    "Power Gem", "Drain Punch", "Vacuum Wave", "Focus Blast", "Energy Ball", "Brave Bird", "Earth Power", "Switcheroo",
    "Giga Impact", "Nasty Plot", "Bullet Punch", "Avalanche", "Ice Shard", "Shadow Claw", "Thunder Fang", "Ice Fang",
    "Fire Fang", "Shadow Sneak", "Mud Bomb", "Psycho Cut", "Zen Headbutt", "Mirror Shot", "Flash Cannon", "Rock Climb",
    "Defog", "Trick Room", "Draco Meteor", "Discharge", "Lava Plume", "Leaf Storm", "Power Whip", "Rock Wrecker",
    "Cross Poison", "Gunk Shot", "Iron Head", "Magnet Bomb", "Stone Edge", "Captivate", "Stealth Rock", "Grass Knot", "Chatter",
    "Judgment", "Bug Bite", "Charge Beam", "Wood Hammer", "Aqua Jet", "Attack Order", "Defend Order", "Heal Order", "Head Smash",
    "Double Hit", "Roar of Time", "Spacial Rend", "Lunar Dance", "Crush Grip", "Magma Storm", "Dark Void", "Seed Flare",
    "Ominous Wind", "Shadow Force",
    # Gen 5
    "Hone Claws", "Wide Guard", "Guard Split", "Power Split", "Wonder Room", "Psyshock", "Venoshock", "Autotomize", "Rage Powder",
    "Telekinesis", "Magic Room", "Smack Down", "Storm Throw", "Flame Burst", "Sludge Wave", "Quiver Dance", "Heavy Slam",
    "Synchronoise", "Electro Ball", "Soak", "Flame Charge", "Coil", "Low Sweep", "Acid Spray", "Foul Play", "Simple Beam",
    "Entrainment", "After You", "Round", "Echoed Voice", "Chip Away", "Clear Smog", "Stored Power", "Quick Guard", "Ally Switch",
    "Scald", "Shell Smash", "Heal Pulse", "Hex", "Sky Drop", "Shift Gear", "Circle Throw", "Incinerate", "Quash", "Acrobatics",
    "Reflect Type", "Retaliate", "Final Gambit", "Bestow", "Inferno", "Water Pledge", "Fire Pledge", "Grass Pledge",
    "Volt Switch", "Struggle Bug", "Bulldoze", "Frost Breath", "Dragon Tail", "Work Up", "Electroweb", "Wild Charge",
    "Drill Run", "Dual Chop", "Heart Stamp", "Horn Leech", "Sacred Sword", "Razor Shell", "Heat Crash", "Leaf Tornado",
    "Steamroller", "Cotton Guard", "Night Daze", "Psystrike", "Tail Slap", "Hurricane", "Head Charge", "Gear Grind",
    "Searing Shot", "Techno Blast", "Relic Song", "Secret Sword", "Glaciate", "Bolt Strike", "Blue Flare", "Fiery Dance",
    "Freeze Shock", "Ice Burn", "Snarl", "Icicle Crash", "V-create", "Fusion Flare", "Fusion Bolt"
]

move_categories = ["Status", "Physical", "Special"]

types = ["Normal", "Fighting", "Flying", "Poison", "Ground", "Rock", "Bug", "Ghost", "Steel", "Fire", "Water", "Grass",
    "Electric", "Psychic", "Ice", "Dragon", "Dark"]

type_chart = {
    "Normal": {"Rock": 0.5, "Ghost": 0, "Steel": 0.5}, 
    "Fighting": {"Normal": 2, "Flying": 0.5, "Poison": 0.5, "Rock": 2, "Bug": 0.5, "Ghost": 0,
                "Steel": 2, "Psychic": 0.5, "Ice": 2, "Dark": 2},
    "Flying": {"Fighting": 2, "Rock": 0.5, "Bug": 2, "Steel": 0.5, "Grass": 2, "Electric": 0.5},
    "Poison": {"Poison": 0.5, "Ground": 0.5, "Rock": 0.5, "Ghost": 0.5, "Steel": 0, "Grass": 2},
    "Ground": {"Flying": 0, "Poison": 2, "Rock": 2, "Bug": 0.5, "Steel": 2, "Fire": 2,
                "Grass": 0.5, "Electric": 2},
    "Rock": {"Fighting": 0.5, "Flying": 2, "Ground": 0.5, "Bug": 2, "Steel": 0.5, "Fire": 2,
                "Ice": 2},
    "Bug": {"Fighting": 0.5, "Flying": 0.5, "Poison": 0.5, "Ghost": 0.5, "Steel": 0.5, "Fire": 0.5,
                "Grass": 2, "Psychic": 2, "Dark": 2}, 
    "Ghost": {"Normal": 0, "Ghost": 2, "Psychic": 2, "Dark": 0.5}, 
    "Steel": {"Rock": 2, "Steel": 0.5, "Fire": 0.5, "Water": 0.5, "Electric": 0.5, "Ice": 2}, 
    "Fire": {"Rock": 0.5, "Bug": 2, "Steel": 2, "Fire": 0.5, "Water": 0.5, "Grass": 2,
                "Ice": 2, "Dragon": 0.5}, 
    "Water": {"Ground": 2, "Rock": 2, "Fire": 2, "Water": 0.5, "Grass": 0.5, "Dragon": 0.5}, 
    "Grass": {"Flying": 0.5, "Poison": 0.5, "Ground": 2, "Rock": 2, "Bug": 0.5, "Steel": 0.5,
                "Fire": 0.5, "Water": 2, "Grass": 2, "Dragon": 0.5},
    "Electric": {"Flying": 2, "Ground": 0, "Water": 2, "Grass": 0.5, "Electric": 0.5, "Dragon": 0.5}, 
    "Psychic": {"Fighting": 2, "Poison": 2, "Steel": 0.5, "Psychic": 0.5, "Dark": 0}, 
    "Ice": {"Flying": 2, "Ground": 2, "Steel": 0.5, "Fire": 0.5, "Water": 0.5, "Grass": 2,
                "Ice": 0.5, "Dragon": 2}, 
    "Dragon": {"Steel": 0.5, "Dragon": 2}, 
    "Dark": {"Fighting": 0.5, "Ghost": 2, "Psychic": 2, "Dark": 0.5}
}

pokemon_narc = ndspy.narc.NARC.fromFile("pokemon_data.narc")
move_narc = ndspy.narc.NARC.fromFile("move_data.narc")

def parse_pokemon_entry(data):
    if len(data) < 40:
        return None
    return {
        'basehp': data[0],
        'baseatk': data[1],
        'basedef': data[2],
        'basespeed': data[3],
        'basespatk': data[4],
        'basespdef': data[5],
        'type1': data[6],
        'type2': data[7],
        'catchrate': data[8],
        'stage': data[9],
        'evs': int.from_bytes(data[10:12], 'little'),
        'item1': int.from_bytes(data[12:14], 'little'),
        'item2': int.from_bytes(data[14:16], 'little'),
        'item3': int.from_bytes(data[16:18], 'little'),
        'gender': data[18],
        'hatchcycle': data[19],
        'basehappy': data[20],
        'exprate': data[21],
        'egggroup1': data[22],
        'egggroup2': data[23],
        'ability1': data[24],
        'ability2': data[25],
        'ability3': data[26],
        'flee': data[27],
        'formid': int.from_bytes(data[28:30], 'little'),
        'form': int.from_bytes(data[30:32], 'little'),
        'numforms': data[32],
        'color': data[33],
        'baseexp': int.from_bytes(data[34:36], 'little'),
        'height': int.from_bytes(data[36:38], 'little'),
        'weight': int.from_bytes(data[38:40], 'little'),
    }

def parse_move_entry(data):
    if len(data) < 36:
        return None
    return {
        'type': data[0],
        'effect_category': data[1],
        'category': data[2],
        'power': data[3],
        'accuracy': data[4],
        'pp': data[5],
        'priority': data[6],
        'hits': data[7],
        'result_effect': int.from_bytes(data[8:10], 'little'),
        'effect_chance': data[10],
        'status': data[11],
        'min_turns': data[12],
        'max_turns': data[13],
        'crit': data[14],
        'flinch': data[15],
        'effect': int.from_bytes(data[16:18], 'little'),
        'recoil': data[18],
        'healing': data[19],
        'target': data[20],
        'stat1': data[21],
        'stat2': data[22],
        'stat3': data[23],
        'magnitude1': data[24],
        'magnitude2': data[25],
        'magnitude3': data[26],
        'stat_chance1': data[27],
        'stat_chance2': data[28],
        'stat_chance3': data[29],
        'flag': data[30]
    }

def read_moves_file(file_path="moves.txt"):
    try:
        with open(file_path, "r") as f:
            lines = f.readlines()
        move_ids = [int(line.strip()) for line in lines if line.strip().isdigit()]
        return move_ids

    except FileNotFoundError:
        print("File not found:", file_path)
        return []
    except ValueError:
        print("File contains invalid entries.")
        return []

def read_team_moves_file(file_path="team_moves.txt"):
    team_moves = []
    try:
        with open(file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip().isdigit()]

        for i in range(0, len(lines), 5):
            if i + 4 < len(lines):
                pokedex = int(lines[i])
                move_ids = list(map(int, lines[i + 1:i + 5]))
                team_moves.append({
                    "pokedex": pokedex,
                    "moves": move_ids
                })
        return team_moves

    except FileNotFoundError:
        print("File not found:", file_path)
        return []
    except ValueError:
        print("File contains invalid entries.")
        return []

default_menu_data = {
            "active": 0,
            "opponent": 0,
            "menu_state": 0,
            "cursor_location": 0,
            "move_id": 0
        }

previous_menu_data = {
            "active": 0,
            "opponent": 0,
            "menu_state": 0,
            "cursor_location": 0,
            "move_id": 0
        }

current_menu_data = {
            "active": 0,
            "opponent": 0,
            "menu_state": 0,
            "cursor_location": 0,
            "move_id": 0
        }

def read_battle_menu(filename="battle_menu.txt"):
    try:
        with open(filename, "r") as file:
            lines = file.read().splitlines()

        if len(lines) < 5:
            return default_menu_data

        active = int(lines[0])
        opponent = int(lines[1])
        menu_state = int(lines[2])
        cursor_location = int(lines[3])
        move_id = int(lines[4])

        return {
            "active": active,
            "opponent": opponent,
            "menu_state": menu_state,
            "cursor_location": cursor_location,
            "move_id": move_id
        }

    except FileNotFoundError:
        print("battle_menu.txt not found.")
        return default_menu_data
    except ValueError:
        return default_menu_data

def compare(current, previous):
    return current == previous

def getMenuState():
    battle_menu = read_battle_menu()
    if battle_menu is not None:
        if (battle_menu["menu_state"] == 0):
            return "MAIN"
        if (battle_menu["menu_state"] == 1):
            return "FIGHT"
        if (battle_menu["menu_state"] == 2):
            return "BAG"
        if (battle_menu["menu_state"] == 3):
            return "POKEMON"
        if (battle_menu["menu_state"] == 4):
            return "RUN"
    else:
        return None

def getCursorState():
    battle_menu = read_battle_menu()
    if battle_menu is not None:
        if (battle_menu["menu_state"] != 1):
            if (battle_menu["cursor_location"] == 0):
                return "FIGHT"
            if (battle_menu["cursor_location"] == 1):
                return "BAG"
            if (battle_menu["cursor_location"] == 2):
                return "POKEMON"
            if (battle_menu["cursor_location"] == 3):
                return "RUN"
    else:
        return None

def getActive():
    battle_menu = read_battle_menu()
    if (battle_menu["active"] > 0 and battle_menu["active"] < 650):
        return speciesNamesList[battle_menu["active"]]

def getOpponent():
    battle_menu = read_battle_menu()
    if (battle_menu["opponent"] > 0 and battle_menu["opponent"] < 650):
        return speciesNamesList[battle_menu["opponent"]]

def getPokemonData(pokedex):
    pokemon = pokemon_narc.files[pokedex]
    pokemon_data = parse_pokemon_entry(pokemon)
    print("Pokemon:", speciesNamesList[pokedex - 1])
    print(pokemon_data)

def getPokemonTypes(pokedex):
    pokemon = pokemon_narc.files[pokedex]
    pokemon_data = parse_pokemon_entry(pokemon)
    type1 = pokemon_data['type1']
    type2 = pokemon_data['type2']
    print(speciesNamesList[pokedex - 1])
    print(types[type1])
    if (type1 != type2):
        print(types[type2])
    print("-----")

def getMove():
    battle_menu = read_battle_menu()
    if (battle_menu is not None):
        if (battle_menu["move_id"] > 0 and battle_menu["move_id"] < 560):
            return move_names[battle_menu["move_id"]]

def getMoveData():
    battle_menu = read_battle_menu()
    active = battle_menu["active"]
    opponent = battle_menu["opponent"]
    moves = read_moves_file()
    for move_id in moves:
        if (move_id != 0):
            move = move_narc.files[move_id]
            move_data = parse_move_entry(move)
            print("Name:", move_names[move_id])
            print("Type:", types[move_data['type']])
            print("Power:", move_data['power'])
            print("Category:", move_categories[move_data['category']])
            print("Accuracy:", move_data['accuracy'])
            print("Damage Calculation:", damageCalculation(active, opponent, move_data['type'], move_data['power'], move_data['category']))
            print("-----")
            #print(move_data)

def getTeamMoveData():
    battle_menu = read_battle_menu()
    team = read_team_moves_file()
    if (battle_menu is not None and team is not None):
        opponent = battle_menu["opponent"]
        overall_best_move = None
        overall_max_damage = -1
        for pokemon in team:
            pokedex = pokemon['pokedex']
            moves = pokemon['moves']
            member_best_move = None
            member_max_damage = -1
            for move_id in moves:
                if (move_id != 0):
                    try:
                        move = move_narc.files[move_id]
                        move_data = parse_move_entry(move)
                        damage = damageCalculation(pokedex, opponent, move_data['type'], move_data['power'], move_data['category'])
                        #print("Pokemon:", speciesNamesList[pokedex - 1])
                        #print("Name:", move_names[move_id])
                        #print("Type:", types[move_data['type']])
                        #print("Power:", move_data['power'])
                        #print("Category:", move_categories[move_data['category']])
                        #print("Accuracy:", move_data['accuracy'])
                        #print("Damage Calculation:", damage)
                        #print("-----")
                        if damage > member_max_damage:
                            member_max_damage = damage
                            member_best_move = {
                                "pokemon": speciesNamesList[pokedex - 1],
                                "name": move_names[move_id],
                                "type": types[move_data['type']],
                                "power": move_data['power'],
                                "category": move_categories[move_data['category']],
                                "accuracy": move_data['accuracy'],
                                "damage": damage
                            }
                            if member_max_damage > overall_max_damage:
                                overall_max_damage = member_max_damage
                                overall_best_move = member_best_move

                    except IndexError:
                        print(f"Invalid move ID: {move_id}")
            if member_best_move:
                print("Best Move for", member_best_move["pokemon"])
                print("Name:", member_best_move["name"])
                print("Type:", member_best_move["type"])
                print("Power:", member_best_move["power"])
                print("Category:", member_best_move["category"])
                print("Accuracy:", member_best_move["accuracy"])
                print("Damage Calculation:", member_best_move["damage"])
                print("*****")
        if overall_best_move:
            print("**Overall Best Move**:")
            print("Pokemon:", overall_best_move["pokemon"])
            print("Name:", overall_best_move["name"])
            print("Type:", overall_best_move["type"])
            print("Power:", overall_best_move["power"])
            print("Category:", overall_best_move["category"])
            print("Accuracy:", overall_best_move["accuracy"])
            print("Damage Calculation:", overall_best_move["damage"])
            print("*****")

def damageCalculation(player, opponent, moveType, power, category):
    battle_menu = read_battle_menu()
    playerPokemon = pokemon_narc.files[player]
    player_data = parse_pokemon_entry(playerPokemon)
    opponentPokemon = pokemon_narc.files[opponent]
    opponent_data = parse_pokemon_entry(opponentPokemon)
    playerType1 = types[player_data['type1']]
    playerType2 = types[player_data['type2']]
    opponentType1 = types[opponent_data['type1']]
    opponentType2 = types[opponent_data['type2']]
    opponentTypes = {opponentType1, opponentType2}
    stab = 1
    if (types[moveType] == playerType1 or types[moveType] == playerType2):
        stab = 1.5
    playerAttack = 1
    opponentDefense = 1
    if (category == 1):
        playerAttack = player_data['baseatk']
        opponentDefense = opponent_data['basedef']
    elif (category == 2):
        playerAttack = player_data['basespatk']
        opponentDefense = opponent_data['basespdef']
    else:
        playerAttack = 1
        opponentDefense = 1
    damage = (power * (playerAttack / opponentDefense)) * stab * typeChart(types[moveType], opponentTypes)
    damage = round(damage)
    return damage

def typeChart(moveType, pokemonTypes):
    typeDamage = 1
    for types in pokemonTypes:
        typeDamage *= type_chart.get(moveType, {}).get(types, 1)
    return typeDamage

while True:
    current_menu_data = read_battle_menu()
    while ((current_menu_data["active"] > 0 and current_menu_data["active"] < 650 and 
        current_menu_data["opponent"] > 0 and current_menu_data["opponent"] < 650)
        and not (compare(previous_menu_data["opponent"], current_menu_data["opponent"]))):
        #getPokemonData(current_menu_data["active"])
        #getPokemonData(current_menu_data["opponent"])
        getPokemonTypes(current_menu_data["active"])
        getPokemonTypes(current_menu_data["opponent"])
        #getMove()
        getTeamMoveData()
        getMenuState()
        getCursorState()
        previous_menu_data = current_menu_data.copy()