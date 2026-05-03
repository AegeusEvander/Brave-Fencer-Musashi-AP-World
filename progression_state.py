from typing import Dict, NamedTuple, Set, Optional, List
from .locations import standard_location_name_to_id, jp_id_offset
from .items import item_name_to_id

progression_state_table: Dict[int, str] = {
    0x000a: "zipline down gondola",
    0x0014: "Rescue Leno",
    0x001e: "Talk to the mayor after rescuing Leno",
    0x0028: "Jon asks for food and water",
    0x0032: "Feed Jon",
    0x003c: "Find Jon's Key",
    0x0046: "Free Jon",
    0x0050: "Give Jon the 4 trees",
    0x005a: "Find Bracelet",
    0x0064: "Equip L-Brace",
    0x006e: "Agree to help the mayor with Steamwood",
    0x0078: "Talk to Fores and start the Steamwood event",
    0x0082: "Fix Steamwood",
    0x0085: "Collect the Earth Scroll",
    0x0087: "Meet Jon after collecting Earth Scroll",
    0x008c: "Talk to Geezer about opening hells valley",
    0x0096: "have Geezer permission to face the Earth Crest Guardian",
    0x00a0: "Allies open the gate to Hell's Valley",
    0x00c8: "Skullpion Defeated",
    0x00d2: "The Mayor says you can get the key to the mine from the windmill",
    0x00dc: "Acquire Mine Key",
    0x00e6: "Acquire Misteria Bloom",
    0x00f0: "Give Misteria to Mayor and Mayor wonders if Hotelo is alright",
    0x00fa: "Meet Hotelo on Twinpeak Mountain and return to village instead",
    0x0104: "Meet Hotelo on Twinpeak Mountain and go after Aqualin",
    0x010e: "Get Aqualin",
    0x0118: "Give Aqualin to Hotelo",
    0x0122: "Talk to Tim after saving him",
    0x012c: "Tim is Saved",
    0x0136: "Talk to Towst, who is banging on the closed restaurant",
    0x0140: "Wanda tells how to reach the basement",
    0x014a: "Meet the restaurant owner at the basement",
    0x0172: "Open all blue eyes",
    0x017c: "Get the Ugly Belt",
    0x0181: "Equip the L-Belt",
    0x0186: "The owner of the restaurant says he needs the rope from the church to get into the well",
    0x0190: "Something is happening at the church at 2 am",
    0x019a: "Enter the church infested with vambees",
    0x01a4: "Exit the church infested with vambees",
    0x01ae: "Father White asks you to retrieve Church Bell",
    0x01cc: "Collected water scroll",
    0x01d1: "Interacted with the church bell (does not require talking to Father White)",
    0x01d6: "Give the Church Bell to the Father White",
    0x01e0: "Return the bell to the village",
    0x0258: "Relic Keeper Defeated",
    0x0276: "Fix the Village Well",
    0x0280: "The mayor's wife asks you to fix the Gondola Gizmo",
    0x028a: "Carpenters describe the Gondola Gizmo",
    0x0294: "Deliver the Gizmo Gondola",
    0x029e: "A fire starts in the village",
    0x02a8: "Put out fire",
    0x02b2: "Mrs. Govern thanks you and tells musashi about the thieves",
    0x02bc: "Get the calendar and rock salt",
    0x02c6: "Use salt on the slug",
    0x02d0: "collect the fire scroll",
    0x02da: "Save the princess",
    0x02e4: "Take the princess to the castle",
    0x02ee: "The mercenaries tell you how to navigate to Frozen Palace",
    0x02f0: "Reach the Frozen Palace gate for the first time",
    0x02f8: "Meet Gingerelle",
    0x0302: "Melt boss door",
    0x030c: "Open and enter the boss door in Frozen Palace",
    0x0384: "Frost Dragon Defeated",
    0x0398: "Complete 4 chapter",
    0x03a2: "Start 5 chapter mayor says to visit shops",
    0x03ac: "Talk to a shop about the missing profits",
    0x03b6: "The princess disappeared and took the village profits with her",
    0x03c0: "go down fixed gondola",
    0x03ca: "Receive Handle 0",
    0x03d4: "Pick up Profits",
    0x03e8: "Give back the profits",
    0x03f2: "Finish Steamwood 2",
    0x044c: "Get the Wind Scroll",
    0x0460: "break your own bincho field",
    0x047e: "See the GiAnt near Twinpeak entrance",
    0x0488: "hop on gondola to squish ant",
    0x0492: "GiAnt breaks open entrance to Upper Mines",
    0x04b0: "Defeat Queen Ant",
    0x04ba: "Go up to the sky island",
    0x0514: "Defeat Ben",
    0x0578: "Defeat Ed",
    0x05dc: "Defeat Topo",
    0x0636: "Start the race against Dark Lumina and DL2 fight",
    0x0640: "DL3 fight",
    0x064a: "end of Credits (would you like to save)",
}

def calc_progression_state(ctx: "BizHawkClientContext", loc_id: int, old_progression_state: int, progression_flags: List[bool], completed_progression_states: Set[int], received_list: List[int]) -> (int, str):
    if(loc_id == 0x3000): #Castle Outside 
        if(old_progression_state in [0x0294, 0x29e] and ctx.slot_data["skip_minigame_town_on_fire"] == False): #0x029e: "A fire starts in the village",
            return 0, ""
        if(not 0x2b2 in completed_progression_states and 0x294 in completed_progression_states and ctx.slot_data["skip_minigame_town_on_fire"] == False): #02a8= Put out fire
            return 0x29e, "" #"A fire starts in the village",
        if(0x47e in completed_progression_states and not 0x488 in completed_progression_states):
            return 0x47e, "" #0x047e: "See the mutant ant at the mountain entrance",
        if(((0x0294 in completed_progression_states and ctx.slot_data["playthrough_method"] == 2) or (0x3c0 in completed_progression_states and ctx.slot_data["playthrough_method"] == 1)) and old_progression_state < 0x3c0 ):
            return 0x3c0, "" #0x03c0: "go down fixed gondola",
        if(not 0x0294 in completed_progression_states and old_progression_state >= 0x3c0 ):
            return 0xa, "" #0x000a: "zipline down gondola",
        #if(0x3b6 in completed_progression_states and not 0x3b6 in completed_progression_states and old_progression_state != 0x3ac): #0x03b6: "The princess disappeared and took the village profits with her",
        #    return 0x3ac #0x03ac: "Talk to a shop about the missing profits"
    if(loc_id == 0x3003): #Castle Meeting Room 
        if(not 0xc8 in completed_progression_states): #0x00c8: "Acquire your first crest",
            if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["MercenC"] in received_list and item_name_to_id["SoldierA"] in received_list and item_name_to_id["KnightB"] in received_list):
                if(((ctx.slot_data["scroll_sanity"] == False and 0x85 in completed_progression_states) or item_name_to_id["Earth Scroll"] in received_list)):
                    if(ctx.slot_data["lumina_randomzied"] == False or item_name_to_id["Lumina"] in received_list or (ctx.slot_data["wind_scroll_logic"] == 3 and progression_flags[26][1] & 0b01 == 0b01)):
                        if(ctx.slot_data["grocery_sanity"] or ctx.slot_data["grocery_sanity_heal_logic"] == False or item_name_to_id["W-Gel"] in received_list or item_name_to_id["Progressive Drink"] in received_list):
                            return 0x8c, "" #0x008c: "Talk to Geezer about opening hells valley",
        if(0x0280 in completed_progression_states and not 0x0294 in completed_progression_states): #0x0294: "Deliver the Gizmo Gondola",
            if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["CarpentB"] in received_list and item_name_to_id["CarpentC"] in received_list):
                if(ctx.slot_data["quest_item_sanity"] == True):
                    if(item_name_to_id["Gondola Gizmo"] in received_list):
                        return 0x028a, "" #0x028a: "Carpenters inform you of the appearance of the item needed to fix the Gondola Gizmo",
                elif(item_name_to_id["Bracelet"] in received_list):
                    return 0x028a, "" #0x028a: "Carpenters inform you of the appearance of the item needed to fix the Gondola Gizmo",

        if(0x2e4 in completed_progression_states and not 0x2f0 in completed_progression_states): #0x02f0: "Reach the frost palace gate for the first time",
            if(item_name_to_id["MercenA"] in received_list and item_name_to_id["MercenB"] in received_list and item_name_to_id["MercenC"] in received_list):
                return 0x02ee, "" #0x02ee: "The mercenaries give you the location",
        #might need to add something for delivery gondola gizmo
        if(ctx.slot_data["playthrough_method"] == 1 and 0x50 in completed_progression_states and 0x85 in completed_progression_states and not 0xc8 in completed_progression_states): #0x00c8: "Acquire your first crest",
            return 0x8c, "" #0x008c: "Talk to Geezer about opening hells valley",
        if(0x280 in completed_progression_states and not 0x294 in completed_progression_states): #0x0294: "Deliver the Gizmo Gondola",
            return 0x280, "" #0x0280: "The mayor's wife asks you to fix the Gondola Gizmo",
        if(ctx.slot_data["playthrough_method"] == 1 and 0x2e4 in completed_progression_states and not 0x2f0 in completed_progression_states and old_progression_state != 0x2e4): #0x02f0: "Reach the frost palace gate for the first time",
            return 0x02ee, "" #0x02ee: "The mercenaries give you the location",

        if(ctx.slot_data["playthrough_method"] == 2 and not 0x2f0 in completed_progression_states and item_name_to_id["MercenA"] in received_list and item_name_to_id["MercenB"] in received_list and item_name_to_id["MercenC"] in received_list):
            return 0x02ee, "" #0x02ee: "The mercenaries give you the location",
    #0x3004: "Castle Gondola", 
        #0x03b6: "The princess disappeared and took the village profits with her",
        #0x03c0: "go down fixed gondola",
    if(loc_id == 0x3014): #"Somnolent Forest", 
        if(0x32 in completed_progression_states and not 0x3c in completed_progression_states): #0x003c: "Find Jon's Key",
            if(old_progression_state != 0x32):
                return 0x32, "" #0x0032: "Feed Jon",
            return 0, ""
        if(0x4b0 in completed_progression_states and progression_flags[17][22] & 0b1 != 0b1 and old_progression_state != 0x4b0): #0x04b0: "Defeat Queen Ant", get note
            return 0x4b0, "" #0x04b0: "Defeat Queen Ant", 
        if((0x02e4 in completed_progression_states or ctx.slot_data["playthrough_method"] == 2)): #0x02f0: "Reach the frost palace gate for the first time",
            if(item_name_to_id["MercenA"] in received_list and item_name_to_id["MercenB"] in received_list and item_name_to_id["MercenC"] in received_list):
                if(old_progression_state != 0x2f0):
                    return 0x02ee, "" #0x02ee: "The mercenaries give you the location",
                return 0, ""
        if(old_progression_state == 0x2bc and not 0x2bc in completed_progression_states):
            return 0xa, "" #0x000a: "zipline down gondola",
        if(not 0x4b0 in completed_progression_states and old_progression_state > 0x492):
            return 0xa, "" #0x000a: "zipline down gondola",
    if(loc_id == 0x301b): #"Meandering Forest", 
        if(0x32 in completed_progression_states and not 0x3c in completed_progression_states and old_progression_state != 0x32): #0x003c: "Find Jon's Key",
            return 0x32, "" #0x0032: "Feed Jon",
        if((0x02e4 in completed_progression_states or ctx.slot_data["playthrough_method"] == 2) and old_progression_state != 0x2f0): #0x02f0: "Reach the frost palace gate for the first time",
            if(item_name_to_id["MercenA"] in received_list and item_name_to_id["MercenB"] in received_list and item_name_to_id["MercenC"] in received_list):
                return 0x02ee, "" #0x02ee: "The mercenaries give you the location",
	#0x301c: "Steamwood Forest", 
    if(loc_id == 0x301e): #"Steamwood Outside", 
        if(old_progression_state in [0x78, 0x82]):
            return 0, ""
        #from CommonClient import logger
        #logger.info("Looking at rules for Steamwood 2")
        if((0x03c0 in completed_progression_states or ctx.slot_data["playthrough_method"] == 2) and (not 0x3ca in completed_progression_states or (ctx.slot_data["quest_item_sanity"] == True and (not(standard_location_name_to_id["Handle #1 - Steamwood 2"] in ctx.checked_locations or standard_location_name_to_id["Handle #1 - Steamwood 2"] + jp_id_offset in ctx.checked_locations) or not(standard_location_name_to_id["Handle #4 - Steamwood 2"] in ctx.checked_locations or standard_location_name_to_id["Handle #4 - Steamwood 2"] + jp_id_offset in ctx.checked_locations) or not (standard_location_name_to_id["Handle #8 - Steamwood 2"] in ctx.checked_locations or standard_location_name_to_id["Handle #8 - Steamwood 2"] + jp_id_offset in ctx.checked_locations))))): #0x03ca: "Receive Handle 0",
            #logger.info("One layer deep")
            if(ctx.slot_data["quest_item_sanity"] == True):
                #logger.info("two layers deep")
                if(item_name_to_id["Manual"] in received_list and item_name_to_id["Bracelet"] in received_list and item_name_to_id["Handle #0"] in received_list and item_name_to_id["Handle #1"] in received_list and item_name_to_id["Handle #4"] in received_list and item_name_to_id["Handle #8"] in received_list and item_name_to_id["Profits"] in received_list and item_name_to_id["Ugly Belt"] in received_list):
                    if(len({0x5b, 0x5c, 0x5d, 0x67, 0x6c} & set(progression_flags[19])) == 5):
                        #logger.info("three layers deep")
                        return 0x3c0, "" #0x03c0: "go down fixed gondola", #check for all handles, manual, bracelet, profits 
            elif(0x82 in completed_progression_states and 0x181 in completed_progression_states):
                return 0x3c0, "" #0x03c0: "go down fixed gondola"
        if(old_progression_state == 0x3c0):
            return 0x64, "" #0x0064: "Equip L-Brace",
        
    if(loc_id == 0x3021): #"Island of Dragons",
        #if(0x2bc in completed_progression_states and not 0x2c6 in completed_progression_states):
        #    return 0x2bc #0x02bc: "Get the calendar and rock salt",
        #if(not 0x2c6 in completed_progression_states and item_name_to_id["Rock Salt"] in received_list):
        #    return 0x2bc #0x02bc: "Get the calendar and rock salt",
        if(not 0x2c6 in completed_progression_states and 0x5f in set(progression_flags[19])): #and (ctx.slot_data["playthrough_method"] == 2 or 0x258 in completed_progression_states)): #rock salt in inventory
            return 0x2bc, "" #0x02bc: "Get the calendar and rock salt",
        if(old_progression_state < 0x2c6 and 0x2c6 in completed_progression_states):
            return 0x2c6, "" #0x02c6: "Use salt on the slug"
        if(0x2c6 in completed_progression_states and not 0x2d0 in completed_progression_states):
            return 0x2c6, "" #0x02c6: "Use salt on the slug"
        if(old_progression_state >= 0x2c6 and not 0x2c6 in completed_progression_states):
            return 0xa, "" #0x000a: "zipline down gondola",
    if(loc_id == 0x3022): #"Graveyard", 
        if(old_progression_state !=  0x32):
            return 0x32, "" #0x0032: "Feed Jon",
    if(loc_id == 0x3024): #"Skullpion Arena", 
        if(not 0xc8 in completed_progression_states and old_progression_state != 0xa0): #0x00c8: "Acquire your first crest",
            if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["MercenC"] in received_list and item_name_to_id["SoldierA"] in received_list and item_name_to_id["KnightB"] in received_list):
                return 0xa0, "" #0x00a0: "Allies open the gate to Hell's Valley",
        if(0xc8 in completed_progression_states):
            return 0xc8, ""
        #TODO add entrance rando logic if not all npcs present
    if(loc_id == 0x3025): #"Twinpeak Entrance", 
        if(not 0x14 in completed_progression_states and progression_flags[17][10] & 0b10000000 == 0b10000000): #agree to rescue dog but have yet to do so
            if(old_progression_state != 0xa):
                return 0xa, "" #0x000a: "zipline down gondola",
            return 0, ""
        if(not 0x46 in completed_progression_states and old_progression_state > 0x1e): #only allow lilypads after rescuing Jon
            return 0x1e, "" #0x001e: "Talk to the mayor after rescuing Leno",
        if(old_progression_state in [0xd2, 0xdc, 0xe6] and 0x46 in completed_progression_states and old_progression_state != 0x46): #make it so Hotelo does not block exploration
            return 0x46, "" #0x0046: "Free Jon",
        if(old_progression_state in [0xd2, 0xdc, 0xe6] and not 0x46 in completed_progression_states and old_progression_state != 0xa): #make it so Hotelo does not block exploration
            return 0x1e, "" #0x001e: "Talk to the mayor after rescuing Leno",
        if(old_progression_state == 0xa and 0x14 in completed_progression_states):
            return 0x14, "" #0x0014: "Rescue Leno",
    if(loc_id == 0x3026): #"Twinpeak Around the Bend", 
        if(0x82 in completed_progression_states and progression_flags[17][2] & 0b1000000 != 0b1000000 and item_name_to_id["Bracelet"] in received_list and old_progression_state != 0x82):
            return 0x82, "" #0x0082: "Fix Steamwood"
        if(progression_flags[17][2] & 0b1000000 != 0b1000000 and old_progression_state > 0x82):
            return 0xa, "" #0x000a: "zipline down gondola", to make it so player can't climb to earth scroll without doing minigame
        if(old_progression_state in [0xd2, 0xdc, 0xe6] and 0x46 in completed_progression_states and old_progression_state != 0x46): #make it so Hotelo does not block exploration
            return 0x46, "" #0x0046: "Free Jon",
        if(old_progression_state in [0xd2, 0xdc, 0xe6] and not 0x46 in completed_progression_states and old_progression_state != 0xa): #make it so Hotelo does not block exploration
            return 0xa, "" #0x000a: "zipline down gondola",
    if(loc_id == 0x3029): #"Twinpeak Second Peak", 
        if(old_progression_state in [0x104, 0x10e]): #0x0104: "Meet Hotelo on Twinpeak Mountain and go after Aqualin",
            return 0, "" #don't interupt aqualin minigame
        if(not 0x46 in completed_progression_states and old_progression_state <= 0x46):
            return 0x5a, "" #0x005a: "Find Bracelet",
        if(ctx.slot_data["quest_item_sanity"] == True):
            if(received_list.count(item_name_to_id["Log"]) >= 4 and not 0x50 in completed_progression_states and 0x46 in completed_progression_states and old_progression_state != 0x46):
                return 0x46, "" #0x0046: "Free Jon",
            if(received_list.count(item_name_to_id["Log"]) < 4):
                return 0x5a, "" #0x005a: "Find Bracelet",
        else:
            if((item_name_to_id["Lumina"] in received_list or ctx.slot_data["lumina_randomzied"] == False) and not 0x50 in completed_progression_states and 0x46 in completed_progression_states and old_progression_state != 0x46):
                return 0x46, "" #0x0046: "Free Jon",
            if(not item_name_to_id["Lumina"] in received_list and ctx.slot_data["lumina_randomzied"] == True):
                return 0x5a, "" #0x005a: "Find Bracelet",
        if(0x50 in completed_progression_states and old_progression_state != 0x5a):
            return 0x5a, "" #0x005a: "Find Bracelet",
	#0x302a: "Twinpeak Rafting", 
    if(loc_id == 0x302b): #"Twinpeak Path to Skullpion", 
        if(not 0xa0 in completed_progression_states and item_name_to_id["CarpentA"] in received_list and item_name_to_id["MercenC"] in received_list and item_name_to_id["SoldierA"] in received_list and item_name_to_id["KnightB"] in received_list and 0x96 != old_progression_state):
            if(ctx.slot_data["playthrough_method"] == 2 or (0x50 in completed_progression_states and 0x85 in completed_progression_states)): 
                return 0x96, "" #0x0096: "have Geezer permission to face the Earth Crest Guardian",
        if(0xa0 in completed_progression_states and old_progression_state < 0xa0):
            return 0xa0, "" #0x00a0: "Allies open the gate to Hell's Valley",
        if(not 0xa0 in completed_progression_states and old_progression_state >= 0xa0): #close gate
            return 0xa, "" #0x000a: "zipline down gondola",
    if(loc_id == 0x302c): #"Twinpeak Waterfall Cave 2", 
        #from CommonClient import logger
        #logger.info("Looking at rules for waterfall Cave 2")
        if(not 0x118 in completed_progression_states and 0xf0 in completed_progression_states and not old_progression_state in [0xf0, 0xfa, 0x104, 0x10e, 0x118]):
            #logger.info("Past first check for aqualin minigame")
            if(((ctx.slot_data["quest_item_sanity"] == True and item_name_to_id["Aqualin"] in received_list) or ctx.slot_data["quest_item_sanity"] == False) and (progression_flags[26][0] & 0b1000000 == 0b1000000 or (progression_flags[26][1] & 0b1000100 == 0b1000100 and ctx.slot_data["sky_scroll_logic"] == 3))): #aqualin and earth scroll or double jump and sky
                #logger.info("Past second check for aqualin minigame")
                return 0xf0, "" #0x00f0: "Give Misteria to Mayor and Mayor wonders if Hotelo is alright",
    if(loc_id == 0x3034): #"Restaurant Basement Entrance", 
        if(not 0x14a in completed_progression_states and old_progression_state != 0x140):
            return 0x140, "" #0x0140: "Wanda talks about the vambees' nest",
        if(not 0x17c in completed_progression_states and 0x172 in completed_progression_states and old_progression_state != 0x172):
            return 0x172, "" #0x0172: "Open all blue eyes",
        if(not 0x17c in completed_progression_states and not 0x172 in completed_progression_states and 0x14a in completed_progression_states and old_progression_state != 0x14a):
            return 0x14a, "" #0x014a: "Meet the restaurant owner at the basement",
    if(loc_id == 0x3042): #"Relic Keeper Arena", 
        if(not 0x258 in completed_progression_states and old_progression_state != 0x1e0):
            return 0x1e0, "" #0x01e0: "Return the bell to the village",
    if(loc_id == 0x3047): #"Misteria Underground Lake", 
        if(not 0xe6 in completed_progression_states and old_progression_state != 0xdc):
            return 0xdc, "" #0x00dc: "Acquire Mine's Key",
    if(loc_id == 0x304b): #"Lower Mine Scrap Depository", 
        if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["CarpentB"] in received_list and item_name_to_id["CarpentC"] in received_list and old_progression_state != 0x28a and (ctx.slot_data["playthrough_method"] == 2 or 0x276 in completed_progression_states)):
            return 0x028a, "" #0x028a: "Carpenters inform you of the appearance of the item needed to fix the Gondola Gizmo",
	#0x304c: "Restaurant Basement Outside Relic Keeper", 
    if(loc_id == 0x304d): #"Grillin Reservoir Tunnel", 
        if(old_progression_state in [0x398, 0x3a2, 0x3ac, 0x3b6, 0x3c0, 0x3ca]): #anything chapter 5 before finishing steamwood turn off steam in tunnel
            return 0xa, "" #0x000a: "zipline down gondola",
    if(loc_id == 0x304e): #"Grillin Reservoir", 
        if(int.from_bytes(progression_flags[18], byteorder='little') != 0x1052):
            if(0x1ae in completed_progression_states and 0x12c in completed_progression_states and 0x136 in completed_progression_states):
                if((ctx.slot_data["quest_item_sanity"] == False or item_name_to_id["Key"] in received_list) and (ctx.slot_data["scroll_sanity"] == False or (item_name_to_id["Water Scroll"] in received_list or (item_name_to_id["Sky Scroll"] in received_list and ctx.slot_data["sky_scroll_logic"] > 1)))):
                    return 0x1ae, "" #0x01ae: "The Father asks you to retrieve Church Bell",
            if(old_progression_state <= 0x276 or old_progression_state >= 0x190):
                return 0xc8, "" #0x00c8: "Acquire your first crest",
        #check if progression state affects Rope to climb
	#0x3051: "Chapter 3 Church Vambee Fight",
    if(loc_id == 0x305c): #"Frozen Palace Lobby",
        #TODO for every area with an eye door make sure progression state isnt too high for entrance rando 
        if(not 0x2f8 in completed_progression_states and 0x2f0 in completed_progression_states and old_progression_state < 0x2f0):
            return 0x2f0, "" #0x02f0: "Reach the frost palace gate for the first time",
        if(not 0x302 in completed_progression_states and 0x2f8 in completed_progression_states and old_progression_state < 0x2f8):
            return 0x2f8, "" #0x02f8: "Meet Gingerelle",
        if(not 0x30c in completed_progression_states and 0x302 in completed_progression_states and old_progression_state < 0x302):
            return 0x302, "" #0x0302: "Melt boss door",
        if(not 0x384 in completed_progression_states and 0x30c in completed_progression_states and old_progression_state < 0x30c):
            return 0x30c, "" #0x030c: "Open and enter the big gate of the 3 eyes in the ice palace",
        if((old_progression_state > 0x398 or old_progression_state < 0x30c) and 0x30c in completed_progression_states):
            return 0x30c, "" #0x030c: "Open and enter the big gate of the 3 eyes in the ice palace",
        if((old_progression_state > 0x398 or old_progression_state < 0x302) and 0x302 in completed_progression_states):
            return 0x302, "" #0x0302: "Melt boss door",
        if((old_progression_state > 0x398 or old_progression_state < 0x2f8) and 0x2f8 in completed_progression_states):
            return 0x2f8, "" #0x02f8: "Meet Gingerelle",
    if(loc_id == 0x3066): #"Frozen Palace Dragon Church", 
        if(old_progression_state != 0x30c):
            return 0x30c, "" #0x030c: "Open and enter the big gate of the 3 eyes in the ice palace",
	#0x3068: "Frozen Palace Courtyard", 
	#0x3069: "Chapter 4 Village on Fire", 
	#0x306f: "Upper Mine Big Fan", 
    if(loc_id == 0x3072): #"Upper Mine Gondola Station", 
        if(old_progression_state != 0x492):
            return 0x492, "" #0x0492: "GiAnt breaks open entrance to Upper Mines",
	#0x3074: "Upper Mine Above Queen Ant", 
    if(loc_id == 0x3075): #"Queen Ant Arena",
        if(old_progression_state != 0x492):
            return 0x492, "" #0x0492: "GiAnt breaks open entrance to Upper Mines",
	#0x3081: "Sky Island",    
    if(loc_id in [0x1010, 0x1052, 0x1077, 0x1094]): #"Chapter 2 Grillin Village", 
        if(old_progression_state in [0x78]):
            return 0, ""
        if(progression_flags[17][10] & 0b10000000 != 0b10000000): #have yet to talk to mayor
            return 0xa, "Need to talk to Mayor to ask about the five scrolls" #0x000a: "zipline down gondola",
        #0x000a: "zipline down gondola",
        #0x0014: "Rescue Leno",
        if((old_progression_state == 0x14 or 0x14 in completed_progression_states) and not 0x1e in completed_progression_states): #need to check with mayor after saving leno
            return 0x14, "Need to let Mayor know that Leno has been saved" #x0014: "Rescue Leno",
        #0x001e: "Talk to the mayor after rescuing Leno",
        if(0x1e in completed_progression_states and not 0x32 in completed_progression_states): #need to talk to and feed man in stocks
            if(ctx.slot_data["bakery_sanity"] == True and ctx.slot_data["quest_item_sanity"] == True):
                if(item_name_to_id["Progressive Bread"] in received_list and item_name_to_id["Well H20"] in received_list):
                    if(0x28 in completed_progression_states):
                        return 0x28, "The man in the stocks needs bread and water" #0x0028: "Jon asks for food and water",
                    return 0x1e, "The man in the stocks needs bread and water" #0x001e: "Talk to the mayor after rescuing Leno",
            elif(ctx.slot_data["bakery_sanity"] == True):
                if(item_name_to_id["Progressive Bread"] in received_list):
                    if(0x28 in completed_progression_states):
                        return 0x28, "The man in the stocks needs bread and water" #0x0028: "Jon asks for food and water",
                    return 0x1e, "The man in the stocks needs bread and water" #0x001e: "Talk to the mayor after rescuing Leno",
            elif(ctx.slot_data["quest_item_sanity"] == True):
                if(item_name_to_id["Well H20"] in received_list):
                    if(0x28 in completed_progression_states):
                        return 0x28, "The man in the stocks needs bread and water" #0x0028: "Jon asks for food and water",
                    return 0x1e, "The man in the stocks needs bread and water" #0x001e: "Talk to the mayor after rescuing Leno",
            else:
                if(0x28 in completed_progression_states):
                    return 0x28, "The man in the stocks needs bread and water" #0x0028: "Jon asks for food and water",
                return 0x1e, "The man in the stocks needs bread and water" #0x001e: "Talk to the mayor after rescuing Leno",
        #0x0028: "Jon asks for food and water",
        #0x0032: "Feed Jon",
        if(0x32 in completed_progression_states and not 0x46 in completed_progression_states): #need to free Jon
            if(ctx.slot_data["quest_item_sanity"] == True):
                #if(item_name_to_id["Jon's Key"] in received_list):
                if(0x4d in set(progression_flags[19])):
                    return 0x3c, "Jon requests that you free him from the stocks" #0x003c: "Find Jon's Key",
            else:
                if(0x3c in completed_progression_states):
                    return 0x3c, "Jon requests that you free him from the stocks" #0x003c: "Find Jon's Key",
        #0x003c: "Find Jon's Key",
        #0x0046: "Free Jon",
        #0x0050: "Give Jon the 4 trees and understand about the five scrolls",
        #0x005a: "Find Bracelet",
        if(0x64 in completed_progression_states and not 0x6e in completed_progression_states): #need to accept fixing steamwood
            return 0x64, "" #0x0064: "Equip L-Brace",
        #0x0064: "Equip L-Brace",
        #0x006e: "Agree to help the mayor with Steamwood",
        #0x0078: "Talk to Fores and start the Steamwood event",#check for manual and bracelet
        if(0x82 in completed_progression_states and progression_flags[17][12] & 0b10000000 != 0b10000000): #mayor Berry
            return 0x82, "The Mayor has a reward for Musashi" #0x0082: "Fix Steamwood",
        #0x0082: "Fix Steamwood",
        #0x0085: "Collect the Earth Scroll",
        #0x0087: "Meet Jon after collecting Earth Scroll",
        #0x008c: "Talk to Geezer about opening hells valley",
        #0x0096: "have Geezer permission to face the Earth Crest Guardian",
        #0x00a0: "Allies open the gate to Hell's Valley",
        if(ctx.slot_data["quest_item_sanity"] == True):
            if(not standard_location_name_to_id["Well H20 - Grillin Village"] in ctx.checked_locations and not (standard_location_name_to_id["Well H20 - Grillin Village"] + jp_id_offset) in ctx.checked_locations): #grab water from well before it 'dries' up
                return 0xa, "Need to draw water from the well before it dries up" #0x000a: "zipline down gondola",
        if(ctx.slot_data["playthrough_method"] == 1 and not (0xc8 in completed_progression_states)):
            if(old_progression_state >= 0xc8):
                return 0xa, "Nothing to do in town until the earth crest guardian is slain" #0x000a: "zipline down gondola",
            return 0, "Nothing to do in town until the earth crest guardian is slain"

	#0x1052: "Chapter 3 Grillin Village", 
        if((ctx.slot_data["playthrough_method"] == 2 or 0xc8 in completed_progression_states) and not 0xd2 in completed_progression_states): #start save tim quest
            if(old_progression_state in [0xc8, 0xd2]):
                return 0, "The Mayor is waiting in the town square"
            return 0xc8, "The Mayor is waiting in the town square" #0x00c8: "Acquire your first crest",
        #0x00c8: "Acquire your first crest",
        if(0xd2 in completed_progression_states and not 0xdc in completed_progression_states): #start save tim quest
            if(old_progression_state == 0xd2):
                return 0, "You can get the key to the mine from Wid at the windmill"
            return 0xd2, "You can get the key to the mine from Wid at the windmill" #0x00d2: "The Mayor says you can get the key to the coal mine with the man from the mill",
        #0x00d2: "The Mayor says you can get the key to the coal mine with the man from the mill",
        if(0x59 in set(progression_flags[19])):
            return 0xdc, "With the Key in your inventory you can open the door to the mine" #0x00dc: "Acquire Mine Key",
        if(0xdc in completed_progression_states and not 0xf0 in completed_progression_states): #need to turn in misteria #TODO check if dc works or if it needs e6 to turn in misteria, it needs e6
            if(ctx.slot_data["quest_item_sanity"] == True):
                #if(item_name_to_id["Misteria"] in received_list):
                if(0x56 in set(progression_flags[19])):
                    return 0xe6, "The Mayor is waiting for Misteria" #0x00e6: "Acquire Misteria Bloom",
                if(old_progression_state == 0xe6 and progression_flags[17][13] & 0b10000000 != 0b10000000):
                    return 0xdc, "" #0x00dc: "Acquire Mine's Key",
                if(progression_flags[17][13] & 0b10000000 == 0b10000000):
                    return 0xe6, "The Mayor is waiting for Misteria" #0x00e6: "Acquire Misteria Bloom",
            elif(0xe6 in completed_progression_states):
                return 0xe6, "The Mayor is waiting for Misteria" #0x00e6: "Acquire Misteria Bloom",
        #0x00dc: "Acquire Mine's Key",
        #0x00e6: "Acquire Misteria Bloom",
        #0x00f0: "Give Misteria to Mayor and Mayor wonders if Hotelo is alright",
        #0x00fa: "Meet Hotelo on Twinpeak Mountain and return to village instead",
        #0x0104: "Meet Hotelo on Twinpeak Mountain and go after Aqualin",
        #0x010e: "Get Aqualin",
        #if(0x118 in completed_progression_states and not 0x122 in completed_progression_states):
        #    if(not old_progression_state in [0x118, 0x122]):
        #        return 0x118 #0x0118: "Give Aqualin to Hotelo",
        #0x0118: "Give Aqualin to Hotelo",
        if(0x118 in completed_progression_states and not 0x12c in completed_progression_states):
            return 0x122, "" #0x0122: "Talk to Tim after saving him",
        #0x0122: "Talk to Tim after saving him",
        if(0x12c in completed_progression_states and not 0x140 in completed_progression_states):
            if(not old_progression_state in [0x122, 0x12c, 0x136]):
                return 0x12c, "Need to talk to Towst and then Wanda" #0x012c: "Tim became a Vambee/ Tim is Saved",
            return 0, "Need to talk to Towst and then Wanda"
        #0x012c: "Tim became a Vambee/ Tim is Saved",
        #if(0x136 in completed_progression_states and not 0x140 in completed_progression_states):
            #return 0x136 #0x0136: "Talk to the drunk and discover you",
        #0x0136: "Talk to the drunk and discover you",
        #0x0140: "Wanda talks about the vambees' nest",
        #0x014a: "Meet the restaurant owner at the basement",
        #0x0172: "Open all blue eyes",
        #0x017c: "Get the Ugly Belt",
        if(0x181 in completed_progression_states and not 0x186 in completed_progression_states and not 0x1ae in completed_progression_states):
            return 0x181, "" #0x0181: "Equip the L-Belt",
        #0x0181: "Equip the L-Belt",
        if((0x186 in completed_progression_states or (progression_flags[26][1] & 0b10 == 0b10 and ctx.slot_data["wind_scroll_logic"] == 3)) and not 0x190 in completed_progression_states):
            return 0x186, "Father White at the church requires assistance" #0x0186: "The owner of the restaurant says he needs the rope",
        #0x0186: "The owner of the restaurant says he needs the rope",
        if(0x190 in completed_progression_states and not 0x19a in completed_progression_states):
            return 0x190, "Father White at the church requires assistance" #0x0190: "Something is happening at the church at 2 am",
        #0x0190: "Something is happening at the church at 2 am",
        if(0x19a in completed_progression_states and not 0x1a4 in completed_progression_states):
            return 0, "Father White at the church requires assistance" #
        #0x019a: "Enter the church infested with vambees",
        if(0x1a4 in completed_progression_states and not 0x1ae in completed_progression_states):
            return 0, "Father White at the church requires assistance" #
        #0x01a4: "Exit the church infested with vambees",
        if((int.from_bytes(progression_flags[18], byteorder='little') & 0xff) in [0x43, 0x52] and not 0x1d6 in completed_progression_states):
            return 0x1d1, "" #0x01d1: "Interacting with the church bell (does not require talking to priest)",

        if(ctx.slot_data["playthrough_method"] == 1 and 0x1ae in completed_progression_states and 0x12c in completed_progression_states and 0x136 in completed_progression_states and not 0x1d6 in completed_progression_states): #TODO make less dumb
            if((ctx.slot_data["quest_item_sanity"] == False or item_name_to_id["Key"] in received_list) and (ctx.slot_data["scroll_sanity"] == False or (item_name_to_id["Water Scroll"] in received_list or (item_name_to_id["Sky Scroll"] in received_list and ctx.slot_data["sky_scroll_logic"] > 1)))):
                return 0x1ae, "Need to find and return the Bell" ##0x01ae: "The Father asks you to retrieve Church Bell",
        
        if(ctx.slot_data["playthrough_method"] == 1 and not 0x258 in completed_progression_states and 0x1e0 in completed_progression_states):
            return 0x1e0, "Need to defeat the water crest guardian" #0x01e0: "Return the bell to the village",

        if(ctx.slot_data["playthrough_method"] == 1 and not (0x258 in completed_progression_states and 0x1d6 in completed_progression_states and 0x1ae in completed_progression_states)):
            return 0x190, "Father White at the church requires assistance" #0x0190: "Something is happening at the church at 2 am",

        if(0x58 in progression_flags[19] and progression_flags[17][15] & 0b1000000 != 0b1000000 and (old_progression_state < 0xc8 or old_progression_state > 0x258) and not 0x1e0 in completed_progression_states): #if rope is in inventory and no rope has been placed
            return 0x1ae, "You can place the rope at the well" ##0x01ae: "The Father asks you to retrieve Church Bell",
        #0x01ae: "The Father asks you to retrieve Church Bell",
        #0x01cc: "Collected water scroll",
        #0x01d1: "Interacting with the church bell (does not require talking to priest)",
        #0x01d6: "Give the Church Bell to the priest",
        #0x01e0: "Return the bell to the village",
	#0x1077: "Chapter 4 Grillin Village",
        if((ctx.slot_data["playthrough_method"] == 2 or 0x258 in completed_progression_states) and progression_flags[17][16] & 0b100000 != 0b100000 and not 0x280 in completed_progression_states and not 0x2b2 in completed_progression_states):
            return 0x258, "You can talk to Mrs Govern about the state of the well" #0x0258: "Acquire your second crest",
        #0x0258: "Acquire your second crest",
        if(0x276 in completed_progression_states and progression_flags[17][16] & 0b100000 == 0b100000 and not 0x280 in completed_progression_states and not 0x2b2 in completed_progression_states):
            return 0x276, "You can let Mrs Govern know that the well has been fixed" #0x0276: "Fix the Village Well",
        #0x0276: "Fix the Village Well",
        #0x0280: "The mayor's wife asks you to fix the Gondola",
        #0x028a: "Carpenters inform you of the appearance of the item needed to fix the Gondola Gizmo",
        #0x0294: "Deliver the Gizmo Gondola",
        #0x029e: "A fire starts in the village",
        #0x02a8: "Put out fire",
        if((0x2b2 in completed_progression_states and not 0x2bc in completed_progression_states) or (ctx.slot_data["skip_minigame_town_on_fire"] == True and not 0x2bc in completed_progression_states and 0x294 in completed_progression_states and 0x276 in completed_progression_states)):
            return 0x2b2, "You can check how Mr Govern is doing" #0x02b2: "Mrs. Govern thanks you and tells musashi about the thieves",
        #0x02b2: "Mrs. Govern thanks you and tells musashi about the thieves",
        #0x02bc: "Get the calendar and rock salt",
        #0x02c6: "Use salt on the slug",
        #0x02d0: "collect the fire scroll",
        #0x02da: "Save the princess",
        #0x02e4: "Rescue princess Filet and take her to the castle",
        #0x02ee: "The mercenaries give you the location",
        #0x02f0: "Reach the frost palace gate for the first time",
        #0x02f8: "Meet Gingerelle",
        #0x0302: "Melt boss door",
        #0x030c: "Open and enter the big gate of the 3 eyes in the ice palace",
        #0x0384: "Defeat Frost Dragon",
        if(ctx.slot_data["playthrough_method"] == 1 and not (0x384 in completed_progression_states and 0x2bc in completed_progression_states)):
            return 0x258, "Need to defeat the fire crest guardian and/or assist Mrs Govern " #0x0258: "Acquire your second crest",

	#0x1094: "Chapter 5/6 Grillin Village"
        #if(0x398 in completed_progression_states and not 0x3a2 in completed_progression_states):
            #return 0x398 #0x0398: "Complete 4 chapter",
        #0x0398: "Complete 4 chapter",
        if((0x398 in completed_progression_states or 0x3a2 in completed_progression_states or (ctx.slot_data["playthrough_method"] == 2 and 0x294 in completed_progression_states)) and not 0x3ac in completed_progression_states):
            if(old_progression_state == 0x3ac):
                if(ctx.slot_data["playthrough_method"] == 2):
                    return 0, "Nothing to do in town right now"
                return 0, "Need to talk to a shopkeeper about what happened"
            
            if(ctx.slot_data["playthrough_method"] == 2):
                return 0x3a2, "Nothing to do in town right now"
            return 0x3a2, "Need to talk to a shopkeeper about what happened" #0x03a2: "Start 5 chapter mayor says to visit shops",
        #0x03a2: "Start 5 chapter mayor says to visit shops",
        #0x03ac: "Talk to a shop about the missing profits",
        #0x03b6: "The princess disappeared and took the village profits with her",
        #0x03c0: "go down fixed gondola",
        #0x03ca: "Receive Handle 0",
        #0x03d4: "Pick up Profits",
        #0x03e8: "Give back the profits",
        if(0x3f2 in completed_progression_states and progression_flags[17][20] & 0b100000 != 0b100000): #talk to mayor about profits
            return 0x3f2, "The Mayor has a reward for Musashi" #0x03f2: "Finish the events of the second Steamwood",
        #0x03f2: "Finish the events of the second Steamwood",
        #0x044c: "Get the Wind Scroll",
        #0x0460: "break your own bincho field",
        #0x047e: "See the mutant ant at the mountain entrance",
        #0x0488: "select to take gondola to ant",
        
        if(0x32 in completed_progression_states and not 0x46 in completed_progression_states and old_progression_state ==0x3c): #need to free Jon but not for free
            if(ctx.slot_data["quest_item_sanity"] == True):
                if(not item_name_to_id["Jon's Key"] in received_list):
                    return 0x32, "" #0x0032: "Feed Jon"
        #0x0032: "Feed Jon",
        #0x003c: "Find Jon's Key",
        if(item_name_to_id["Rope"] in received_list and not item_name_to_id["Key"] in received_list):
            if(old_progression_state >= 0x276 or old_progression_state < 0xc8):
                return 0xc8, "Nothing to do in town right now" #0x00c8: "Acquire your first crest",
        
        if(0x1ae in completed_progression_states and 0x12c in completed_progression_states and 0x136 in completed_progression_states and not 0x1d6 in completed_progression_states): #TODO make less dumb
            if((ctx.slot_data["quest_item_sanity"] == False or item_name_to_id["Key"] in received_list) and (ctx.slot_data["scroll_sanity"] == False or item_name_to_id["Water Scroll"] in received_list)):
                return 0x1ae, "Can return Bell to town" ##0x01ae: "The Father asks you to retrieve Church Bell",
        #0x01ae: "The Father asks you to retrieve Church Bell",
        
        if(0x4b0 in completed_progression_states and old_progression_state < 0x4b0):
            return 0x4b0, "Nothing to do in town right now" #0x04b0: "Defeat Queen Ant",\

        if(0x1e0 in completed_progression_states and old_progression_state < 0x1d6 and old_progression_state > 0xc8):
            return 0x1e0, "Nothing to do in town right now" #0x01e0: "Return the bell to the village",

        if(old_progression_state < 0xc8 and old_progression_state > 0x5a): #grocery closed
            return 0xa, "Nothing to do in town right now" #0x000a: "zipline down gondola",

        if(old_progression_state > 0x4b0):
            return 0xa, "Nothing to do in town right now" #0x000a: "zipline down gondola",

        if(old_progression_state == 0x1e):
            return 0xa, "Nothing to do in town right now" #0x000a: "zipline down gondola",

        if(old_progression_state == 0x3c0):
            return 0x4b0, "Nothing to do in town right now" #0x04b0: "Defeat Queen Ant",\
        #0x005a: "Find Bracelet",
        #0x0064: "Equip L-Brace",
        #0x006e: "Agree to help the mayor with Steamwood",
        #0x0078: "Talk to Fores and start the Steamwood event",
        #0x0082: "Fix Steamwood",
        #0x0085: "Collect the Earth Scroll",
        #0x0087: "Meet Jon after collecting Earth Scroll",
        #0x008c: "Talk to Geezer about opening hells valley",
        #0x0096: "have Geezer permission to face the Earth Crest Guardian",
        #0x00a0: "Allies open the gate to Hell's Valley",
        #0x00c8: "Skullpion Defeated",
        #TODO logic for when there is nothing that needs to be done right now in the town
        return 0x0, "Nothing to do in town right now" #0x000a: "zipline down gondola",
    if(loc_id in [0x1011, 0x1053, 0x1078, 0x1095]): #"Chapter 2 Upper Village", 
	#0x1053: "Chapter 3 Upper Village", 
	#0x1078: "Chapter 4 Upper Village", 
    #0x1095: "Chapter 5/6 Upper Village"
        if(0x118 in completed_progression_states and not 0x122 in completed_progression_states):
            return 0x118, "" #0x0118: "Give Aqualin to Hotelo",
        #0x0118: "Give Aqualin to Hotelo",
        #if(0x14 in completed_progression_states and progression_flags[17][16] & 0b1000 != 0b1000): #rescued leno but no cutscene
        #    return 0x14 #0x0014: "Rescue Leno",

        if(not 0x14 in completed_progression_states and progression_flags[17][10] & 0b10000000 == 0b10000000 and old_progression_state == 0xa): #yet to rescue leno... but might soon
            return 0, "" #0x0014: "Rescue Leno",
        #0x0064: "Equip L-Brace",
        if(0x6e in completed_progression_states and not 0x82 in completed_progression_states):
            if(ctx.slot_data["quest_item_sanity"] == True):
                if(item_name_to_id["Manual"] in received_list):
                    return 0x6e, "" #0x006e: "Agree to help the mayor with Steamwood",
                elif(old_progression_state == 0x6e):
                    return 0xa, "" #0x000a: "zipline down gondola",
            else:
                return 0x6e, "" #0x006e: "Agree to help the mayor with Steamwood",
        #0x006e: "Agree to help the mayor with Steamwood",
        #0x0078: "Talk to Fores and start the Steamwood event",
        #0x0082: "Fix Steamwood",
        #0x044c: "Get the Wind Scroll",
        if(progression_flags[17][6] & 0b1000 == 0b1000 and 0x294 in completed_progression_states and not 0x492 in completed_progression_states and not 0x47e in completed_progression_states and (ctx.slot_data["playthrough_method"] == 2 or 0x03c0 in completed_progression_states)):
            if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["CarpentB"] in received_list and item_name_to_id["CarpentC"] in received_list and (item_name_to_id["Gondola Gizmo"] in received_list or (ctx.slot_data["quest_item_sanity"] == False and item_name_to_id["Bracelet"] in received_list))):
                return 0x460, "" #0x0460: "break your own bincho field",
        if(0x492 in completed_progression_states and old_progression_state < 0x492):
            return 0x492, "" #0x0492: "GiAnt breaks open entrance to Upper Mines",
        if(not 0x492 in completed_progression_states and old_progression_state >= 0x492):
            return 0x1e, "" #0x001e: "Talk to the mayor after rescuing Leno",
        #0x0460: "break your own bincho field",
        #0x047e: "See the mutant ant at the mountain entrance",
        #0x0488: "hop on gondola to squish ant",
        #0x0492: "GiAnt breaks open entrance to Upper Mines",
        #0x04b0: "Defeat Queen Ant",
    if(loc_id in [0x2013, 0x2055, 0x207a, 0x2097] and ctx.slot_data["playthrough_method"] == 2): #toy shop
        return 0x4b0, "" #0x0514: "Defeat Ben", 0x04b0: "Defeat Queen Ant",
    #0x2013: "Chapter 2 Toy Shop", 
	#0x2055: "Chapter 3 Toy Shop", 
	#0x207a: "Chapter 4 Toy Shop", 
    #0x2097: "Chapter 5/6 Toy Shop", 
    if(loc_id in [0x2015, 0x2056, 0x207b, 0x2098]): #"Chapter 2-6 Bakery", 
        if(ctx.slot_data["bakery_sanity"] == False):
            if(len({0xc8, 0x258, 0x384, 0x4b0} & completed_progression_states) > 1):
                if(old_progression_state < 0x258):
                    return 0x258, "" #0x0258: "Acquire your second crest",
            else:
                if(old_progression_state >= 0x258):
                    return 0xa, "" #0x000a: "zipline down gondola",
    #0x2015: "Chapter 2 Bakery", 
	#0x2056: "Chapter 3 Bakery", 
	#0x207b: "Chapter 4 Bakery", #two bosses killed
	#0x2098: "Chapter 5/6 Bakery", 
    if(loc_id in [0x2016, 0x2057, 0x207c, 0x2099]): #"Chapter 2-6 Grocery", 
        if(old_progression_state == 0x122):
            if(not 0x122 in completed_progression_states):
                return 0, ""
            return 0x12c, ""
        if(old_progression_state == 0x118):
            if(not 0x122 in completed_progression_states):
                return 0x122, ""
            return 0x12c, ""
        #if(old_progression_state in [0x118, 0x122]):
        #    return 0
        if(ctx.slot_data["grocery_sanity"] == False):
            if(len({0xc8, 0x258, 0x384, 0x4b0} & completed_progression_states) > 1):
                if(old_progression_state < 0x258):
                    return 0x258, "" #0x0258: "Acquire your second crest",
            else:
                if(old_progression_state >= 0x258):
                    return 0x12c, "" #0x012c: "Tim became a Vambee/ Tim is Saved",
	#0x2057: "Chapter 3 Grocery", 
	#0x207c: "Chapter 4 Grocery",#two bosses killed
	#0x2099: "Chapter 5/6 Grocery", 
    if(loc_id in [0x201a, 0x205b, 0x2080, 0x209d]): #"Chapter 2-6 Restaurant", 
        if((progression_flags[17][14] & 0b100000 == 0b100000 or progression_flags[17][14] & 0b1000000 == 0b1000000) and old_progression_state < 0x140): #talk to wanda and macho
            return 0x258, "" #0x0258: "Acquire your second crest",
        if(not (progression_flags[17][14] & 0b100000 == 0b100000 or progression_flags[17][14] & 0b1000000 == 0b1000000) and old_progression_state >= 0x140): #have not talked to wanda and macho
            return 0xa, "" #0x000a: "zipline down gondola",
	#0x205b: "Chapter 3 Restaurant", #check if tim was saved
	#0x2080: "Chapter 4 Restaurant", 
    #0x209d: "Chapter 5/6 Restaurant"

    return 0, ""

def calc_completed_progression_state(ctx: "BizHawkClientContext", progression_flags: List[List[bytes]]) -> Set[int]:
    val = set()
    if(progression_flags[17][11] & 0b10 == 0b10): # or progression_flags[17][16] & 0b1000 == 0b1000):
        val.add(0x0014)#: "Rescue Leno",
    if(progression_flags[17][11] & 0b11 == 0b11):
        val.add(0x001e)#: "Talk to the mayor after rescuing Leno",
    if(progression_flags[17][11] & 0b1000 == 0b1000):
        val.add(0x0028)#: "Jon asks for food and water",
    if(progression_flags[17][11] & 0b100000 == 0b100000):
        val.add(0x0032)#: "Feed Jon",
    if(progression_flags[17][11] & 0b1000000 == 0b1000000):
        val.add(0x003c)#: "Find Jon's Key",
    if(progression_flags[17][11] & 0b10000000 == 0b10000000):
        val.add(0x0046)#: "Free Jon",
    if(progression_flags[17][1] & 0b1000000 == 0b1000000):
        val.add(0x0050)#: "Give Jon the 4 trees and understand about the five scrolls",
        #val.add(0x005a)#: "Find Bracelet",
    if(progression_flags[26][1] & 0b10000000 == 0b10000000):
        val.add(0x0064)#: "Equip L-Brace",
    if(progression_flags[17][12] & 0b10000 == 0b10000):
        val.add(0x006e)#: "Agree to help the mayor with Steamwood",
    if(progression_flags[17][12] & 0b100000 == 0b100000):
        val.add(0x0078)#: "Talk to Fores and start the Steamwood event",
    if(progression_flags[17][12] & 0b1000000 == 0b1000000):
        val.add(0x0082)#: "Fix Steamwood",
    if(progression_flags[1][7] & 0b100000 == 0b100000):
        val.add(0x0085)#: "Collect the Earth Scroll",
    if(progression_flags[17][16] & 0b100 == 0b100):
        val.add(0x0087)#: "Meet Jon after collecting Earth Scroll",
    if(int.from_bytes(progression_flags[27], byteorder='little') > 3):
        val.add(0x008c)#: "Talk to Geezer about opening hells valley",
    if(int.from_bytes(progression_flags[27], byteorder='little') > 4):
        val.add(0x0096)#: "have Geezer permission to face the Earth Crest Guardian",
    if(progression_flags[17][13] & 0b1000 == 0b1000): #TODO check for something else for entrance rando
        val.add(0x00a0)#: "Allies open the gate to Hell's Valley", 
    if(progression_flags[17][13] & 0b1000 == 0b1000):
        val.add(0x00c8)#: "Acquire your first crest",
    #if(False): #TODO manually record when this happens Probably
    #if(int.from_bytes(progression_flags[24], byteorder='little') >= 0xa7):
        #val.add(0x00d2)#: "The Mayor says you can get the key to the coal mine with the man from the mill",
    #if(False): #TODO manually record when this happens Probably
    #if(int.from_bytes(progression_flags[24], byteorder='little') >= 0xa7):
    if((ctx.slot_data["quest_item_sanity"] == True and (standard_location_name_to_id["Key from Wid - Grillin Village"] in ctx.checked_locations or standard_location_name_to_id["Key from Wid - Grillin Village"] + jp_id_offset in ctx.checked_locations)) or (ctx.slot_data["quest_item_sanity"] == False and (progression_flags[17][13] & 0b1000000 == 0b1000000 or 0x59 in progression_flags[19]))): #yuck
        val.add(0x00d2)#: "The Mayor says you can get the key to the coal mine with the man from the mill",
        val.add(0x00dc)#: "Acquire Mine's Key",
    #if(False): #TODO manually record when this happens Probably
    if((ctx.slot_data["quest_item_sanity"] == True and (standard_location_name_to_id["Misteria - Misteria Underground Lake"] in ctx.checked_locations or standard_location_name_to_id["Misteria - Misteria Underground Lake"] + jp_id_offset in ctx.checked_locations)) or (ctx.slot_data["quest_item_sanity"] == False and (progression_flags[17][14] & 0b1 == 0b1 or progression_flags[17][13] & 0b10000000 == 0b10000000 or 0x56 in progression_flags[19]))): #yuck
        val.add(0x00e6)#: "Acquire Misteria Bloom",
    if(progression_flags[17][14] & 0b1 == 0b1): #is this agreeing with mayor to find hotelo
        val.add(0x00f0)#: "Give Misteria to Mayor and Mayor wonders if Hotelo is alright",
        #val.add(0x00fa)#: "Meet Hotelo on Twinpeak Mountain and return to village instead",
    if(progression_flags[17][16] & 0b10 == 0b10 or progression_flags[17][14] & 0b10 == 0b10): 
        val.add(0x0104)#: "Meet Hotelo on Twinpeak Mountain and go after Aqualin",
        val.add(0x010e)#: "Get Aqualin",
        val.add(0x0118)#: "Give Aqualin to Hotelo",
    #if(progression_flags[17][14] & 0b10 == 0b10): 
    if(progression_flags[17][14] & 0b1000 == 0b1000): 
        val.add(0x0122)#: "Talk to Tim after saving him",
        val.add(0x012c)#: "Tim became a Vambee/ Tim is Saved",
    if(progression_flags[17][14] & 0b100000 == 0b100000 or progression_flags[17][14] & 0b1000000 == 0b1000000): 
        val.add(0x0136)#: "Talk to the drunk and discover you",
        val.add(0x0140)#: "Wanda talks about the vambees' nest",
    if(progression_flags[17][5] & 0b1000000 == 0b1000000): 
        val.add(0x014a)#: "Meet the restaurant owner at the basement",
    if(progression_flags[17][15] & 0b11110 == 0b11110): 
        val.add(0x0172)#: "Open all blue eyes",
    if((ctx.slot_data["quest_item_sanity"] == True and (standard_location_name_to_id["Ugly Belt - Restaurant Basement"] in ctx.checked_locations or standard_location_name_to_id["Ugly Belt - Restaurant Basement"] + jp_id_offset in ctx.checked_locations)) or (ctx.slot_data["quest_item_sanity"] == False and progression_flags[26][1] & 0b1000000 == 0b1000000)): #yuck
        val.add(0x017c)#: "Get the Ugly Belt",
    if(progression_flags[26][1] & 0b1000000 == 0b1000000):
        val.add(0x0181)#: "Equip the L-Belt",
        #val.add(0x0186)#: "The owner of the restaurant says he needs the rope", #TODO add manually?
    if(progression_flags[20][0] & 0b10000000 == 0b10000000):
        val.add(0x0186)#: "The owner of the restaurant says he needs the rope",
        val.add(0x0190)#: "Something is happening at the church at 2 am",
        val.add(0x019a)#: "Enter the church infested with vambees",
        val.add(0x01a4)#: "Exit the church infested with vambees",
        val.add(0x01ae)#: "The Father asks you to retrieve Church Bell",
    if(progression_flags[1][7] & 0b1000000 == 0b1000000):
        val.add(0x01cc)#: "Collected water scroll",
    if(int.from_bytes(progression_flags[18], byteorder='little') == 0x1052):
        val.add(0x01d1)#: "Interacting with the church bell (does not require talking to priest)",
        val.add(0x01d6)#: "Give the Church Bell to the priest",
        val.add(0x01e0)#: "Return the bell to the village",
    if(progression_flags[4][17] & 0b10000000 == 0b10000000):
        val.add(0x0258)#: "Acquire your second crest",
    if(progression_flags[17][6] & 0b1 == 0b1): 
        val.add(0x0276)#: "Fix the Village Well",
    #if(progression_flags[17][16] & 0b100000 == 0b100000):
    if((ctx.slot_data["quest_item_sanity"] == True and (standard_location_name_to_id["Mrs Govern's Pie - Grillin Village"] in ctx.checked_locations or standard_location_name_to_id["Mrs Govern's Pie - Grillin Village"] + jp_id_offset in ctx.checked_locations)) or (ctx.slot_data["quest_item_sanity"] == False and progression_flags[17][16] & 0b100000 == 0b100000 and progression_flags[17][6] & 0b1 == 0b1 and ctx.slot_data["playthrough_method"] == 2)):
        val.add(0x0280)#: "The mayor's wife asks you to fix the Gondola Gizmo",
    if(int.from_bytes(progression_flags[27], byteorder='little') > 6):
        val.add(0x028a)#: "Carpenters inform you of the appearance of the item needed to fix the Gondola Gizmo",
    #if(int.from_bytes(progression_flags[27], byteorder='little') == 8):
        #val.add(0x0294)#: "Deliver the Gizmo Gondola",
    #if(False): #TODO manually record when this happens Probably
    if((ctx.slot_data["quest_item_sanity"] == True and (standard_location_name_to_id["Reward #1 After Extinguishing Village - Grillin Village"] in ctx.checked_locations or standard_location_name_to_id["Reward #1 After Extinguishing Village - Grillin Village"] + jp_id_offset in ctx.checked_locations))):
        val.add(0x0294)#: "Deliver the Gizmo Gondola",
        val.add(0x029e)#: "A fire starts in the village",
        val.add(0x02a8)#: "Put out fire",
        val.add(0x02b2)#: "Mrs. Govern thanks you and tells musashi about the thieves",
        val.add(0x02bc)#: "Get the calendar and rock salt",
    if(progression_flags[1][7] & 0b10000000 == 0b10000000):
        val.add(0x02c6)#: "Use salt on the slug",
        val.add(0x02d0)#: "collect the fire scroll",
    #if(False): #TODO manually record when this happens Probably
        val.add(0x02da)#: "Save the princess",
        #val.add(0x02e4)#: "Rescue princess Filet and take her to the castle",
    if(int.from_bytes(progression_flags[27], byteorder='little') > 9):
        val.add(0x02ee)#: "The mercenaries give you the location",
    if(progression_flags[17][17] & 0b10000000 == 0b10000000): 
        val.add(0x02f0)#: "Reach the frost palace gate for the first time",
    if(progression_flags[17][7] & 0b10000000 == 0b10000000): 
        val.add(0x02f8)#: "Meet Gingerelle",
    if(progression_flags[17][9] & 0b10000000 == 0b10000000): #enter room past boss door
        val.add(0x0302)#: "Melt boss door",
        val.add(0x030c)#: "Open and enter the big gate of the 3 eyes in the ice palace",
    if(progression_flags[4][23] & 0b10000000 == 0b10000000):
        val.add(0x0384)#: "Defeat Frost Dragon",
    if(progression_flags[17][2] & 0b10 == 0b10): 
        val.add(0x0398)#: "Complete 4 chapter",
    if(False): #TODO manually record when this happens Probably
        val.add(0x03a2)#: "Start 5 chapter mayor says to visit shops",
        val.add(0x03ac)#: "Talk to a shop about the missing profits",
    #if(int.from_bytes(progression_flags[27], byteorder='little') > 10):
        #val.add(0x03b6)#: "The princess disappeared and took the village profits with her",
    if(False): #TODO manually record when this happens Probably
        val.add(0x03c0)#: "go down fixed gondola",
    if(progression_flags[17][6] & 0b100000 == 0b100000): 
        val.add(0x03ca)#: "Receive Handle 0",
    if(progression_flags[4][27] & 0b10000000 == 0b10000000): #Topo action figure
        val.add(0x03d4)#: "Pick up Profits",
    if(progression_flags[28][0] & 0b10 == 0b10 or progression_flags[4][27] & 0b10000000 == 0b10000000):
        val.add(0x03e8)#: "Give back the profits",
        val.add(0x03f2)#: "Finish the events of the second Steamwood",
    if(progression_flags[1][8] & 0b1 == 0b1):
        val.add(0x044c)#: "Get the Wind Scroll",
        val.add(0x0460)#: "break your own bincho field",
    #if(False): #TODO manually record when this happens Probably
    if(progression_flags[17][21] & 0b10000000 == 0b10000000): #clear poison mist, probably want to track manually as well
        val.add(0x047e)#: "See the mutant ant at the mountain entrance",
        val.add(0x0488)#: "hop on gondola to squish ant",
        val.add(0x0492)#: "GiAnt breaks open entrance to Upper Mines",
    if(progression_flags[4][29] & 0b10000000 == 0b10000000):
        val.add(0x04b0)#: "Defeat Queen Ant",
    return val
