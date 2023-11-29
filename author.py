import os
import json
import multiprocessing
from tqdm import tqdm
import random
import re
from html import unescape

# print("files: ",file_paths)
# 10k
# gaming = ["girlgamers", "gaming", "csgo", "dota2", "leagueoflegends",  "minecraft", "eldenring", "truegaming", "overwatch"]
# ng = ["mademesmile", "wholesomememes", "politicalhumor", "memes", "funny", "askreddit", "", 'aww', 'worldnews', 'movies', 'pics']
gaming = ['0ad', '7daystodie', '8bitMMO', 'aberoth', 'AceAttorney', 'AceOfSpades', 'achron', 'ActOfAggression', 'theaftermath', 'aoecs', 'aoe2', 'aoeIII', 'ageofempiresrevival', 'AgeofMythology', 'ageofwonders', 'aion', 'AirMech', 'AIwar', 'AlanWake', 'ColonialMarines', 'alien_swarm', 'freeallegiance', 'alphaprotocol', 'AmongUs', 'anarchyonline', 'AnimalCrossing', 'ac_newhorizons', 'anno', 'ApexLegends', 'APlagueTale', 'arcanum', 'archeage', 'Arma', 'armagetronad', 'armoredcore', 'ARMS', 'Artemis', 'Ascend', 'assassinscreed', 'assassinscreed3', 'Assassinscreed4', 'AsteroidFight', 'atlanticaonline', 'Awesomenauts', 'baldursgate', 'BanjoKazooie', 'BannerSaga', 'arkham', 'BatmanArkham', 'battleblocktheater', 'Battlefield', 'battlefield3', 'ps3bf3', 'battlefield_4', 'badcompany2', 'PSBF', 'BattleForge', 'BattleRealms', 'battlezone', 'beatsaber', 'Bejeweled', 'Besiege', 'beyondgoodandevil', 'beyondtwosouls', 'bindingofisaac', 'Bioshock', 'BioshockInfinite', 'blackdesertonline', 'blackguards', 'Blacklight', 'blackmesasource', 'Blazblue', 'bloodlinechampions', 'btd6', 'bomberman', 'Borderlands', 'Borderlands2', 'Boktai', 'bridgeproject', 'brigandine', '', 'brink', 'bully', 'Cabal2', 'codbo', 'blackops2', 'CODGhosts', 'MW2', 'mw3', 'CODZombies', 'carmageddon', 'CarnageHeart', 'CastleStory', 'castlevania', 'catherinegame', 'ChivalryGame', 'Chorilion_City_Crimes', 'ChronoCross', 'chronotrigger', 'CitiesInMotion', 'CitiesSkylines', 'Cityofheroes', 'civ', 'CivMulti', 'ClashOfClans', 'ClashRoyale', 'colonysurvival', 'combatarms', 'commandandconquer', 'redalert2', 'CompanyOfHeroes', 'CompetitiveHalo', 'contra', 'Contrast', 'counter_strike', 'GlobalOffensive', 'The_Crew', 'survivetheculling', 'CrusaderKings', 'CubeWorld', 'Culdcept', 'cursedcrusade', 'cyberpunkgame', 'DanceDanceRevolution', 'Darkfall', 'dmo', 'EmbraceTheDarkness', 'darkout', 'Darksiders', 'darksouls', 'DarkSouls2', 'DayOfDefeat', 'dayz', 'dayzspawnhelpers', 'hoggit', 'blackshark', 'deadbydaylight', 'die', 'DeadlyPremonition', 'deadpoolgame', 'deadrising', 'DeadSpace', 'deadspace3', 'Defiance', 'demonssouls', 'DestinyTheGame', 'DetailCraft', 'Deusex', 'DevilMayCry', 'Diablo', 'DinoCrisis', 'Dirtybomb', 'Disgaea', 'dishonored', 'DistantWorlds', 'thedivision', 'djmax', 'dontstarve', 'Doom', 'Doom_FPS', 'DoomMods', 'DOTA', 'DotA2', 'dragonage', 'dragonquest', 'driver', 'dungeondefenders', 'ddo', 'Dredmor', 'dust514', 'dustforce', 'dwarffortress', 'earthbound', 'EA_NHL', 'EchoesOfMana', 'elastomania', 'EpicSeven', 'EternalCardGame', 'Morrowind', 'oblivion', 'elderscrollslegends', 'elderscrollsonline', 'teso', 'ESOXBOX', 'skyrim', 'skyrimdawnguard', 'skyrimDragonborn', 'skyrimhearthfire', 'ElectronicSuperJoy', 'elitegames', 'EliteDangerous', 'empyriongame', 'EndlessSpace', 'eRepublik', 'eu4', 'EuroTruck2', 'Eve', 'everquest', 'EQNext', 'EverSky', 'Egttr', 'EvolveGame', 'F12012', 'factorio', 'falconbms', 'FallGuysGame', 'Fallout', 'Reddit2238', 'fo3', 'Brotherhood_of_Steel', 'falloutlore', 'fnv', 'farcry', 'FastRacingNeo', 'FIFA', 'EAfifapc', 'FinalFantasy', 'finalfantasytactics', 'finalfantasyx', 'ffxi', 'ffxiv', 'ffxv', 'FFVIIRemake', 'fireemblem', 'firefall', 'FistfulOfFrags', 'FOnline', 'footballmanagergames', 'ForgeWar', 'FORTnITE', 'fortressforever', '', 'forza', 'FreedomForce', 'freelancer', 'freespace', 'frontmission', 'frozensynapse', 'ftlgame', 'Insomniacs_Fuse', 'FuturamaWOTgame', 'GalCiv', 'Galaga', 'GOWFA', 'ganbaregoemon', 'gmod', 'GearsOfWar', 'geometrydash', 'Gex', 'GhostRecon', 'GRFS', 'gnomoria', 'GodofWar', 'GoldenEye', 'GoldenSun', 'ggempire', 'grandia', 'GrandChase', 'GTA', 'GrandTheftAutoV', 'GTAVadventures', 'GT5', 'gravityrush', 'growtopia', 'GuildWars', 'Guildwars2', 'HalfLife', 'halo', 'Halo4', 'forge', 'HPHogwartsMystery', 'harvestmoon', 'Hawken', 'hearthfire', 'hearthstone', 'hellgate', 'HeroesandGenerals', 'HoMM', 'HeroesofNewerth', 'heroesofthestorm', 'HillClimbRacing', 'HiTMAN', 'HitmanAbsolution', 'hockeyquestionmark', 'Homefront', 'icewinddale', 'il2', 'ImpossibleCreatures', 'VanHelsing', 'infamous', 'TheWarZ', 'infinitecrisis', 'Injusticegame', 'InjusticeMobile', 'insurgency', 'InterstellarMarines', 'Ironfell', 'ironharvestgame', 'jakanddaxter', 'JanesCombatSims', 'JSRF', 'hawkthorne', 'jumpgate', 'JurassicParkAftermath', 'jurassicparkog', 'JC2', 'katamari', 'katawashoujo', 'KerbalSpaceProgram', 'KiDIcaruS', 'killingfloor', 'killzone', 'kag', 'kingdomcome', 'KingdomHearts', 'kol', 'kingdomsofamalur', 'kof', 'kot', 'Kirby', 'LadderSlasher', 'lanoire', 'LARP', 'TheLastFederation', 'TLOU', 'thelastofus', 'thelastofusfactions', 'leagueoflegends', 'l4d2', 'legendofdragoon', 'grimrock', 'LegendofLegaia', 'LegendOfMana', 'zelda', 'majorasmask', 'legogaming', 'lifeisstrange', 'littlebigplanet', 'thelongestjourney', 'lotro', 'lordsofuberdark', 'Mabinogi', 'Madden', 'mafia_2k', 'mag', 'magicka', 'maia', 'Manyland', 'Maplestory', 'MapleStory2', 'Marathon', 'mario', 'mariokart', 'MarioRPG', 'MarkLane', 'MAA', 'FutureFight', 'marvelheroes', 'MvC3', 'masseffect', 'masseffect3', 'MECoOp', 'mechwarrior', 'mwo', 'Megaman', 'Megaten', 'meltyblood', 'menofwar', 'metalgearsolid', 'metro2033', 'themightyquest', 'Minecraft', 'limitedservers', 'Minecraft360', 'minecraftxe', 'MinoMonsters', 'MomGamers', 'MLBTheShow', 'monacoismine', 'mnc', 'mncpc', 'MonsterHunter', 'MortalKombat', 'mk9', 'mountandblade', 'museumtycoon', 'myst', 'ns2', 'NBA2k', 'NCAAFBseries', 'needforspeed', 'NFSU2', 'neopets', 'NeoScavenger', 'Neotokyo', 'Neverwinter', 'NewWorldGame', 'ninjagaiden3', 'ninjagaidensigma2', 'Ni_no_Kuni', 'nomansskythegame', 'nowheregame', 'nox', 'Oddworld', 'Okami', 'OmegaStrikers', 'Onimusha', 'openra', 'openttd', 'ORBITOR', 'OrcsMustDie', 'orcsmustdie2', 'osugame', 'overlordgame', 'Overgrowth', 'Overwatch', 'Pacman', 'papermario', 'pathofexile', 'pathologic', 'paydaytheheist', 'paladins', 'peggle', 'Perpetuum', 'persona4golden', 'Persona5', 'PSO', 'PSO2', 'PhasmophobiaGame', 'ffpictlogica', 'pioneerspacesim', 'plagueinc', 'planescape', 'planetaryannihilation', 'Planetside', 'planets3', 'PlantsVSZombies', 'psbattleroyale', 'PocketPlanes', 'pokemon', 'pokemongo', 'ptcgo', 'Portal', 'PostKnightGame', 'prey', 'PrinceOfPersia', 'Prismata', 'prisonarchitect', 'WEPES', 'projecteternity', 'projectzomboid', 'PuzzleAndDragons', 'ypp', 'QuakeLive', 'quantumbreak', 'questforglory', 'id_RAGE', 'RagnarokOdyssey', 'RailroadTycoonSeries', 'RatchetAndClank', 'Rayman', 'RotMG', 'Recettear', 'reddeadredemption', 'redorchestra', 'relaxedpokemontrades', 'residentevil', 'TheMercenaries', 'resistance', 'RtCW', 'Rift', 'RimWorld', 'Risen', 'riseofnations', 'riseofthetriad', 'RisingWorld', 'RocketLeague', 'Rockband', 'RockRaiders', 'RogueCompany', 'RogueLegacy', 'rct', 'runescape', 'scape', 'trueruse', 'playrust', 'rustyhearts', 'SaintsRow', 'SanctuaryRPG', 'Sanctum', 'sauerbraten', 'savage', 'Scrolls', 'ScrumbleShip', 'SCUMgame', 'Seaworthy', 'TheSecretWorld', 'WARISPREJUDICE', 'seiken', 'Sekiro', 'Shenmue', 'theship', 'Shootmania', 'silenthill', 'SimCity', 'tappedout', 'thesims', 'SimsGlitches', 'SoSE', 'SirYouAreBeingHunted', 'skiesofarcadia', 'Skullgirls', 'skylanders', 'sleepingdogs', 'Slycooper', 'SmashMuck', 'Smite', 'SOCOM', 'FirstPersonSoda', 'SonicTheHedgehog', 'SoulCalibur', 'SoulCaliburV', 'SoundShapes', 'spacechem', 'SS13', 'spartacuslegends', 'spelunky', 'spiral_knights', 'splatoon', 'Splintercell', 'Spore', 'spyparty', 'Spyro', 'joinsquad', 'SSX', 'stalker', 'stanleyparable', 'starbound', 'starcitizen', 'StarConflict', 'starcraft', 'starforge', 'Starmade', 'StarSonata', 'sto', 'StarWarsBattlefront', 'kotor', 'swtor', 'StateOfDecay', 'Steel_Division', 'Stepmania', 'storyofseasons', 'StreetFighter', 'sf3', 'SF4', 'SFxT', 'stronghold', 'subspace', 'Sudeki', 'thesuffering', 'smnc', 'smashbros', 'SuperTurbo', 'Supremacy1914', '', 'ea_syndicate', 'SystemShock2', 'TagPro', 'tales', 'tf2', 'Tekken', 'TeraOnline', 'Terraria', 'tdu2', 'thehunterprimal', 'Thief', 'TibiaMMO', 'RedditCountryClub', 'titanfall', 'toejamandearl', 'TokyoJungle', 'TombRaider', 'THPS', 'Torchlight', 'TotalAnnihilation', 'totalwar', 'touhou', 'Towns', 'trainfever', 'transformice', 'trialsofmana', 'tribalhero', 'Tribes1', 'Trine', 'tropico', 'TrueSkate', 'turok', 'TwistedMetal', 'ultimategeneral', 'uncharted', 'UniverseProject', 'unrealtournament', 'UT2004', 'VagrantStory', 'valkyria', 'AVWW', 'VivaPinata', 'Vox', 'warcraft3', 'Warframe', 'wargame', 'Warlock', 'WarOfTheRoses', 'Warthunder', 'Wasteland', 'watch_dogs', 'Wayward', 'WesterosCraft', 'WildStar', 'thewitcher3', 'TheWolfAmongUs', 'EnemyTerritory', 'WTNO', 'worldalpha', 'TWEWY', 'WorldofTanks', 'WorldofTanksXbox', 'wow', 'classicwow', 'WWEGames', 'X3TC', 'Xcom', 'xlife', 'Xenogears', 'Xenosaga', 'Xenoblade_chronicles', 'XenobladeChroniclesX', 'yakuzagames', 'ZombiU', 'zzt', 'Link', 'backgammon', 'battlemaps', 'boardgames', 'cardsagainsthumanity', 'CarWarsGame', 'chess', 'DnD', 'DungeonsAndDragons', 'baduk', 'lfg', 'magicTCG', 'Malifaux', 'Miniswap', 'Munchkin', 'Netrunner', 'Pathfinder_RPG', 'pkmntcg', 'rpg', 'Shadowrun', 'XWingTMG', 'tabletop', 'Warhammer', 'Warmachine', 'yugioh', '4sentencegamereviews', '60fpsGamingGifs', '90sGamer', 'AVGN', 'AskGames', 'BarCraft', 'gamingvids', 'betakeys', 'betatests', 'casualgaming', 'chiptunes', 'CCGstudies', 'completegaming', 'consolerepair', 'CoOpGaming', 'coopplay', 'CrazyGameIdeas', 'creepygaming', 'customcontrollers', 'customcovers', 'DeadGames', 'DidYouKnowGaming', 'DirtyGaming', 'dogeforgames', 'gamingeastereggs', 'emulation', 'esports', 'FanTheories', 'findgames', 'flashgamers', 'FlashGames', 'fragfilms', 'freegames', 'freemmorpgs', 'freeonlinegaming', 'freetoplaygames', 'FreeWebGames', 'FutureGames', 'GBL', 'Gamebundles', 'gamecollecting', 'GameCommentatorSwap', 'GameCult', 'GameDeals', 'gamedesign', 'gamedevclassifieds', 'gamedev', 'gamedrawings', 'gamefilm', 'gamefurniture', 'gamegrumps', 'gameideas', 'GameInfirmary', 'GameMods', 'gamenostalgia', 'GameOffers', 'GamePhysics', 'GameplayUnlimited', 'gameplayvideos', 'GameRanks', 'GamerConfessions', 'gamereviews', 'gamernews', 'GamerPals', 'GamerPorn', 'Gamer', 'gamerproblems', 'GamerVideos', 'Games', 'Gamescom', 'GameScreens', 'gamesell', 'games_journalism', 'GameSociety', 'GamesTheMovie', 'gamestory', 'gamestream', 'gameswap', 'GameswapEurope', 'gamesworthplaying', 'gametales', 'GameTheorists', 'Gamingtiles', 'gamewallpaper', 'gameworlds', 'Gaming4Gamers', 'gamingadvice', 'gamingartwork', 'GamingAU', 'GamingChallenges', 'Gamingcirclejerk', 'gamingfashion', 'gamingforleisure', 'Gaming_Gear', 'Gaming_Geek', 'gaminghistory', 'GamingHumor', 'GamingIsBeautiful', 'gamingkickstarter', 'Gamingmemories', 'gamingmentors', 'gamingmommies', 'GamingMusicVideos', 'gamingnews', 'GamingPeripherals', 'GamingPlays', 'gamingphotography', 'Gamingsaves', 'gamingsuggestions', 'Gamingthoughts', 'GGT', 'geekmerch', 'GiftofGames', 'Glitchers', 'GraphicsofGames', 'greatsteamgames', 'guildofgames', 'Homebrews', 'ImaginaryGaming', 'IndieDev', 'indiegameswap', 'IndieGaming', 'indiejunction', 'ingaming', 'jeuxvideo', 'justgames', 'KillMyBacklog', 'lanparty', 'letsplay', 'LetsPlayVideos', 'linux_gaming', 'loadingscreenthoughts', 'longlostgamers', 'lowendgaming', 'ludology', 'machinima', 'MakeMyGame', 'MakingTheClutch', 'MAME', 'masochisticgamers', 'moddingguides', 'montageparodies', 'multiplayerservers', 'needateam', 'Newgrounds', 'NorseGaming', 'oculus', 'onlinegames', 'opensourcegames', 'patientgamers', 'gamingpc', 'playitforward', 'playmygame', 'Playntrade', 'PromoteGamingVideos', 'puregameplay', 'quicklooks', 'retrogamemusic', 'RetroGamePorn', 'retrogameswap', 'retrogaming', 'Retrogamingmusic', 'retrophonegaming', 'secretofmana', 'ServerReviews', 'ShittyFragVideos', 'shittysteamgames', 'ShouldIbuythisgame', 'ShowOffYourCharacter', 'Simulate', 'socialgaming', 'SophisticatedGamers', 'SFM', 'speedrun', 'Sprays', 'Squads', 'steamdeals', 'SteamGameSwap', 'steam_giveaway', 'greenlightquality', 'storiesofwar', 'StreamRequest', 'survivorzero', 'tipofmyjoystick', 'truegaming', 'UnreleasedGames', 'Upscaled', 'videogameartporn', 'VideoGameConspiracies', 'VideoGameCrossover', 'vgstreams', 'VideoGameMaps', 'videogamemetal', 'gamemusic', 'VideogameMysteries', 'videogameresearch', 'VideoGameReviews', 'videogametales', 'WackyGaming', 'walkthrough', 'WebGames', 'whatareyouplaying', 'wtfgames', 'YouShouldPlay', 'youtubegaming', 'zocken', '4Xgaming', '8bitworld', 'adventuregames', 'BaseBuildingGames', 'DinoVGs', 'FantasyGaming', 'Fighters', 'fightinggamesvideos', 'FPS', 'flightsim', 'gameslikeminecraft', 'HackAndSlash', 'HorrorGameVideos', 'HorrorGames', 'HorrorGaming', 'interactivefiction', 'JRPG', 'metroidvania', 'MMORPG', 'MUD', 'openworldgames', 'pdox', 'platformer', 'platforming', 'RealTimeStrategy', 'rhythmgames', 'roguelikedev', 'roguelikes', 'rpg_gamers', 'shmups', 'shutdownmmos', 'simracing', 'SimulationGaming', 'soccergaming', 'spacesimgames', 'stealthgames', 'StrategyGames', 'StrategyRpg', 'SurvivalGaming', 'survivalhorror', 'trucksim', 'tbs', 'tycoon', 'VGracing', 'vns', 'BrothersInArms', '360gamers', 'AchievementHunt', 'AdultGamers', 'ausgaming', 'blackgirlgamers', 'ChicagoGaming', 'classicbattlefield', 'ClearBackblast', 'DadsGaming', 'disabledgamers', 'DrunkenGamery', 'entgaming', 'evedreddit', 'freehugsbf3', 'freehugsmc', 'GamingQuebec', 'gaymers', 'GirlGamers', 'GW2EU', 'IndianGaming', 'indiegames', 'mindcrack', 'mcpublic', 'ProgressiveGamers', 'ProjectAwesome', 'purebattlefield', 'RDDT', 'rdtclan', 'RedditBrigade', 'redditcasual', 'RedditDads', 'NAE3', 'Playdate', 'wowgaymers', 'redditgw', 'FTH', 'RUGC', 'redditguild', 'gamingesp', 'SerbiaGaming', 'subdreddit', 'Team_Awesome', 'TestOutfit', 'ultrahardcore', 'wreckedrdt', 'zeldents', '3DO', '3DS', 'amiga', 'Amstrad', 'AndroidGaming', 'apple2', 'cade', 'Astrocade', 'Atari2600', 'atari5200', 'atari7800', 'atari8bit', 'AtariJaguar', 'atarilynx', 'atarist', 'bbcmicro', 'ChannelF', 'ColecoVision', 'Commodore', 'c64', 'consolegaming', 'consoles', 'Desura', 'dosgaming', 'Gameboy', 'Gamecube', '', 'GFWLive', 'handheld', 'INTV', 'iosgaming', 'macgaming', 'MagnavoxOdyssey', 'odyssey2', 'Microvision', 'MobileGaming', 'MSX', 'neogeo', 'nes', 'ngage', 'n64', 'NintendoSwitch', 'ouya', 'openpandora', 'pcgaming', 'playstation', 'psx', 'ps2', 'PS3', 'ps3deals', 'Ps3TechHelp', 'PS4', 'PS5', 'PlaystationHome', 'PSNFriends', 'PlayStationPlus', 'PSP', 'PlayStationSolutions', 'Trophies', 'vita', 'PocketGamers', 'SEGA32X', 'SegaCD', 'MegaCD', 'dreamcast', 'game_gear', 'SEGAGENESIS', 'Megadrive', 'MasterSystem', 'SMSGG', 'SegaSaturn', 'Sega_Saturn', 'SG1000', 'snes', 'Stadia', 'Steam', 'ti994a', 'trs80', 'TurboGrafx', 'Vectrex', 'VirtualBoy', 'wii', 'wiiu', 'sharpx68000', 'xbox', 'xbox360', 'xboxone', 'XboxSeriesX', 'zxspectrum', 'activision', 'AmanitaDesign', 'atari', 'atlus', 'BethesdaSoftworks', 'BigBlockGames', 'Blizzard', 'Bungie', 'casualnintendo', 'DOUBLEFINE', 'Ensemble', 'HumongousEnt', 'impressionsgames', 'Kairosoft', 'lucasarts', 'mogeko', 'mojang', 'nintendo', 'nipponichi', 'nordicgames', 'obsidian', 'paradoxplaza', 'platinumgames', 'PlutoGames', 'rockstar', 'SEGA', 'shinyloot', 'Sierra', 'SNKplaymore', 'sony', 'SquareEnix', 'TeamIco', 'telltale', 'Twitch', 'ubisoft', 'valve']

def append_to_txt(gcom, gstr): 
    with open(gstr+".json", 'ab+') as f:
        f.seek(0,2)
        if f.tell() == 0:
            f.write(json.dumps({"comments":gcom}).encode())
        else:
            f.seek(-2,2)           
            f.truncate()                           #Remove the last character, open the array
            f.write(' , '.encode())                #Write the separator
            f.write(json.dumps(gcom)[1:].encode())    #Dump the dictionary
            f.write('}'.encode())

def process_txt(filename, author):
    gcom = {}
    for auth in author:
        gcom[auth] = {"gaming":[],"nongaming":[]}
    _,y,d,_ = filename.split('_')
    #  = x
    if not os.path.exists("RC_"+y+"_"+d+"_gaming"):
        os.mkdir("RC_"+y+"_"+d+"_gaming")
    if not os.path.exists("RC_"+y+"_"+d+"_nongaming"):
        os.mkdir("RC_"+y+"_"+d+"_nongaming")
    with open(filename, 'r') as fp:
        data = list(fp)
        # if f.startswith():
        k=0
        for comment in tqdm(data):
            comment = json.loads(comment)
            if comment['body']=='[deleted]':
                continue            
            text = re.sub(r"(\r|\n|<.*?>)+", "", unescape(comment["body"])).strip()
            text = re.sub(r"\s*\[source\]\(http://[^\)]*\)", "", text)
            if len(text)>50:
                if comment['author'] in author:
                    if comment['subreddit'] in gaming:
                        gcom[comment['author']]["gaming"].append(text)
                        if len(gcom[comment['author']]["gaming"])==10000:
                            os.chdir("RC_"+y+"_"+d+"_gaming")
                            append_to_txt(gcom[comment['author']],comment['author']) # Dump the dictionary
                            os.chdir('..')
                            gcom[comment['author']]['gaming'] = []
                    else:
                        gcom[comment['author']]["nongaming"].append(text)
                        if len(gcom[comment['author']]["nongaming"])==10000:
                            os.chdir("RC_"+y+"_"+d+"_nongaming")
                            append_to_txt(gcom[comment['author']],comment['author'])
                            os.chdir("..")
                            gcom[comment['author']]['nongaming'] = []
                    # k+=1
        for auth in author:
            if len(gcom[auth]['gaming'])>0:
                os.chdir("RC_"+y+"_"+d+"_gaming")
                append_to_txt(gcom[auth]['gaming'],auth)
                os.chdir("..")
            if len(gcom[auth]['nongaming'])>0:
                os.chdir("RC_"+y+"_"+d+"_nongaming")
                append_to_txt(gcom[auth]['nongaming'],auth)
                os.chdir("..")
                

    print(filename,": ",k)


def process(filename,gcom,ngcom):
    with open(filename, 'r') as fp:
        data = list(fp)
        # if f.startswith():
        k=0
        for comment in tqdm(data):
            comment = json.loads(comment)
            if comment['body']=='[deleted]' or comment['author']=='[deleted]':
                continue
            if comment['subreddit'] in gaming:
                if comment['author'] not in gcom:
                    gcom[comment['author']] = 1
                else:
                    gcom[comment['author']] += 1
                k+=1
            else:
                if comment['author'] not in ngcom:
                    ngcom[comment['author']] = 1
                else:
                    ngcom[comment['author']] += 1

    print(filename,": ",k)



import time
start = time.time()
os.chdir("reddit_all")

yy = None
gcom = {}
ngcom = {}
for f in os.listdir("."):
    _,y,d,_ = f.split('_')
    if yy is None:
        yy=y
    if yy is not None and yy!=y:
        if len(gcom)>0 and len(ngcom)>0:
            both = set(gcom.keys()).intersection(set(ngcom.keys()))
            overall = {}
            for key in both:
                if ngcom[key]<=1.5*gcom[key] and ngcom[key]>=0.5*gcom[key]:
                    overall[key] = {"gaming":gcom[key], "nongaming":ngcom[key], "total":gcom[key]+ngcom[key]}
            sorted_items = sorted(overall.items(), key=lambda x: x[1]['total'], reverse=True)
            top_10 = dict(sorted_items[:10])
            print(top_10)
        gcom = {}
        ngcom = {}
        yy=y
    process(f,gcom,ngcom)
    
if len(gcom)>0 and len(ngcom)>0:
    both = set(gcom.keys()).intersection(set(ngcom.keys()))
    overall = {}
    for key in both:
        if ngcom[key]<=1.5*gcom[key] and ngcom[key]>=0.75*gcom[key]:
            overall[key] = {"gaming":gcom[key], "nongaming":ngcom[key], "total":gcom[key]+ngcom[key]}
    sorted_items = sorted(overall.items(), key=lambda x: x[1]['total'], reverse=True)
    top_10 = dict(sorted_items[:10])
    print(top_10)

for f in os.listdir("."):
    process_txt(f,top_10.keys())
end = time.time()
print(end - start)

# num_processes = multiprocessing.cpu_count()
# pool = multiprocessing.Pool(processes=num_processes)

# # map the process_file function to each file path in parallel
# pool.map(process, file_paths)

# # close the pool to release resources
# pool.close()
# pool.join()