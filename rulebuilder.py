from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
from .locations import location_name_groups, location_table, standard_location_name_to_id, days_of_week
from .items import item_table
from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasAny, HasAll, Rule, CanReachRegion, True_, HasAnyCount, HasFromList
from .options import QuestItemSanity, PlaythroughMethod, ScrollSanity, WindScrollLogic, GrocerySanity, GrocerySanityHealLogic, BakerySanity, SkyScrollLogic, StartingMaxHP, CoreSanity, LuminaRandomized, ForceSodaFountainToBeLast, SetGoal, TimeSanity, TimeSanitySettings
if TYPE_CHECKING:
    from . import BFMWorld
import math


def check_location_name(name: str, lang: bool) -> str:
    if(lang == False):
        return name
    return location_table[name].jp_name

def check_item_name(name: str, lang: bool) -> str:
    if(lang == True):
        return name
    return item_table[name].jp_name

def set_rules(world: "BFMWorld") -> None:
    player = world.player
    options = world.options
    lang = world.options.set_lang.value == 1 or world.using_ut == True or world.options.spoiler_items_in_english.value == True

    quest_item_sanity_off = OptionFilter(QuestItemSanity, False)
    quest_item_sanity_on = OptionFilter(QuestItemSanity, True)
    bakery_sanity_off = OptionFilter(BakerySanity, False)
    bakery_sanity_on = OptionFilter(BakerySanity, True)
    scroll_sanity_off = OptionFilter(ScrollSanity, False)
    scroll_sanity_on = OptionFilter(ScrollSanity, True)
    core_sanity_off = OptionFilter(CoreSanity, False)
    core_sanity_on = OptionFilter(CoreSanity, True)
    grocery_sanity_off = OptionFilter(GrocerySanity, False)
    grocery_sanity_on = OptionFilter(GrocerySanity, True)
    time_sanity_off = OptionFilter(TimeSanity, False)
    time_sanity_on = OptionFilter(TimeSanity, True)
    time_sanity_separate = OptionFilter(TimeSanitySettings, TimeSanitySettings.option_separate)
    time_sanity_combined = OptionFilter(TimeSanitySettings, TimeSanitySettings.option_combined)
    heal_logic_on = [grocery_sanity_on] + [OptionFilter(GrocerySanityHealLogic, True)]
    is_lumina_not_randomized = OptionFilter(LuminaRandomized, False)
    is_open_world = OptionFilter(PlaythroughMethod, PlaythroughMethod.option_open_world)

    can_enter_grocery = (HasAny(check_item_name("10:00", lang), check_item_name("11:00", lang), check_item_name("12:00", lang), check_item_name("13:00", lang), check_item_name("14:00", lang), check_item_name("15:00", lang), check_item_name("16:00", lang), check_item_name("17:00", lang), check_item_name("18:00", lang), check_item_name("19:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 10:00", lang), check_item_name("Mon 11:00", lang), check_item_name("Mon 12:00", lang), check_item_name("Mon 13:00", lang), check_item_name("Mon 14:00", lang), check_item_name("Mon 15:00", lang), check_item_name("Mon 16:00", lang), check_item_name("Mon 17:00", lang), check_item_name("Mon 18:00", lang), check_item_name("Mon 19:00", lang),
        check_item_name("Tue 10:00", lang), check_item_name("Tue 11:00", lang), check_item_name("Tue 12:00", lang), check_item_name("Tue 13:00", lang), check_item_name("Tue 14:00", lang), check_item_name("Tue 15:00", lang), check_item_name("Tue 16:00", lang), check_item_name("Tue 17:00", lang), check_item_name("Tue 18:00", lang), check_item_name("Tue 19:00", lang),
        check_item_name("Wed 10:00", lang), check_item_name("Wed 11:00", lang), check_item_name("Wed 12:00", lang), check_item_name("Wed 13:00", lang), check_item_name("Wed 14:00", lang), check_item_name("Wed 15:00", lang), check_item_name("Wed 16:00", lang), check_item_name("Wed 17:00", lang), check_item_name("Wed 18:00", lang), check_item_name("Wed 19:00", lang),
        check_item_name("Thr 10:00", lang), check_item_name("Thr 11:00", lang), check_item_name("Thr 12:00", lang), check_item_name("Thr 13:00", lang), check_item_name("Thr 14:00", lang), check_item_name("Thr 15:00", lang), check_item_name("Thr 16:00", lang), check_item_name("Thr 17:00", lang), check_item_name("Thr 18:00", lang), check_item_name("Thr 19:00", lang),
        check_item_name("Sky 10:00", lang), check_item_name("Sky 11:00", lang), check_item_name("Sky 12:00", lang), check_item_name("Sky 13:00", lang), check_item_name("Sky 14:00", lang), check_item_name("Sky 15:00", lang), check_item_name("Sky 16:00", lang), check_item_name("Sky 17:00", lang), check_item_name("Sky 18:00", lang), check_item_name("Sky 19:00", lang),
        check_item_name("Sat 10:00", lang), check_item_name("Sat 11:00", lang), check_item_name("Sat 12:00", lang), check_item_name("Sat 13:00", lang), check_item_name("Sat 14:00", lang), check_item_name("Sat 15:00", lang), check_item_name("Sat 16:00", lang), check_item_name("Sat 17:00", lang), check_item_name("Sat 18:00", lang), check_item_name("Sat 19:00", lang),
        check_item_name("Sun 10:00", lang), check_item_name("Sun 11:00", lang), check_item_name("Sun 12:00", lang), check_item_name("Sun 13:00", lang), check_item_name("Sun 14:00", lang), check_item_name("Sun 15:00", lang), check_item_name("Sun 16:00", lang), check_item_name("Sun 17:00", lang), check_item_name("Sun 18:00", lang), check_item_name("Sun 19:00", lang)) & time_sanity_combined) | time_sanity_off

    can_enter_toy_shop = (HasAny(check_item_name("12:00", lang), check_item_name("13:00", lang), check_item_name("14:00", lang), check_item_name("15:00", lang), check_item_name("16:00", lang), check_item_name("17:00", lang), check_item_name("18:00", lang), check_item_name("19:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 12:00", lang), check_item_name("Mon 13:00", lang), check_item_name("Mon 14:00", lang), check_item_name("Mon 15:00", lang), check_item_name("Mon 16:00", lang), check_item_name("Mon 17:00", lang), check_item_name("Mon 18:00", lang), check_item_name("Mon 19:00", lang),
        check_item_name("Tue 12:00", lang), check_item_name("Tue 13:00", lang), check_item_name("Tue 14:00", lang), check_item_name("Tue 15:00", lang), check_item_name("Tue 16:00", lang), check_item_name("Tue 17:00", lang), check_item_name("Tue 18:00", lang), check_item_name("Tue 19:00", lang),
        check_item_name("Thr 12:00", lang), check_item_name("Thr 13:00", lang), check_item_name("Thr 14:00", lang), check_item_name("Thr 15:00", lang), check_item_name("Thr 16:00", lang), check_item_name("Thr 17:00", lang), check_item_name("Thr 18:00", lang), check_item_name("Thr 19:00", lang),
        check_item_name("Sky 12:00", lang), check_item_name("Sky 13:00", lang), check_item_name("Sky 14:00", lang), check_item_name("Sky 15:00", lang), check_item_name("Sky 16:00", lang), check_item_name("Sky 17:00", lang), check_item_name("Sky 18:00", lang), check_item_name("Sky 19:00", lang),
        check_item_name("Sat 12:00", lang), check_item_name("Sat 13:00", lang), check_item_name("Sat 14:00", lang), check_item_name("Sat 15:00", lang), check_item_name("Sat 16:00", lang), check_item_name("Sat 17:00", lang), check_item_name("Sat 18:00", lang), check_item_name("Sat 19:00", lang),
        check_item_name("Sun 12:00", lang), check_item_name("Sun 13:00", lang), check_item_name("Sun 14:00", lang), check_item_name("Sun 15:00", lang), check_item_name("Sun 16:00", lang), check_item_name("Sun 17:00", lang), check_item_name("Sun 18:00", lang), check_item_name("Sun 19:00", lang)) & time_sanity_combined) | time_sanity_off

    can_enter_restaurant = (HasAny(check_item_name("18:00", lang), check_item_name("19:00", lang), check_item_name("20:00", lang), check_item_name("21:00", lang), check_item_name("22:00", lang), check_item_name("23:00", lang), check_item_name("00:00", lang), check_item_name("01:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 18:00", lang), check_item_name("Mon 19:00", lang), check_item_name("Mon 20:00", lang), check_item_name("Mon 21:00", lang), check_item_name("Mon 22:00", lang), check_item_name("Mon 23:00", lang), check_item_name("Tue 00:00", lang), check_item_name("Tue 01:00", lang),
        check_item_name("Tue 18:00", lang), check_item_name("Tue 19:00", lang), check_item_name("Tue 20:00", lang), check_item_name("Tue 21:00", lang), check_item_name("Tue 22:00", lang), check_item_name("Tue 23:00", lang), check_item_name("Wed 00:00", lang), check_item_name("Wed 01:00", lang),
        check_item_name("Wed 18:00", lang), check_item_name("Wed 19:00", lang), check_item_name("Wed 20:00", lang), check_item_name("Wed 21:00", lang), check_item_name("Wed 22:00", lang), check_item_name("Wed 23:00", lang), check_item_name("Thr 00:00", lang), check_item_name("Thr 01:00", lang),
        check_item_name("Thr 18:00", lang), check_item_name("Thr 19:00", lang), check_item_name("Thr 20:00", lang), check_item_name("Thr 21:00", lang), check_item_name("Thr 22:00", lang), check_item_name("Thr 23:00", lang), check_item_name("Sky 00:00", lang), check_item_name("Sky 01:00", lang),
        check_item_name("Sky 18:00", lang), check_item_name("Sky 19:00", lang), check_item_name("Sky 20:00", lang), check_item_name("Sky 21:00", lang), check_item_name("Sky 22:00", lang), check_item_name("Sky 23:00", lang), check_item_name("Sat 00:00", lang), check_item_name("Sat 01:00", lang),
        check_item_name("Sat 18:00", lang), check_item_name("Sat 19:00", lang), check_item_name("Sat 20:00", lang), check_item_name("Sat 21:00", lang), check_item_name("Sat 22:00", lang), check_item_name("Sat 23:00", lang), check_item_name("Sun 00:00", lang), check_item_name("Sun 01:00", lang)) & time_sanity_combined) | time_sanity_off

    can_enter_conners = (HasAny(check_item_name("11:00", lang), check_item_name("12:00", lang), check_item_name("13:00", lang), check_item_name("14:00", lang), check_item_name("15:00", lang)) & \
        HasAny(check_item_name("Tue", lang), check_item_name("Wed", lang), check_item_name("Thr", lang), check_item_name("Sky", lang), check_item_name("Sat", lang), check_item_name("Sun", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Tue 11:00", lang), check_item_name("Tue 12:00", lang), check_item_name("Tue 13:00", lang), check_item_name("Tue 14:00", lang), check_item_name("Tue 15:00", lang),
        check_item_name("Wed 11:00", lang), check_item_name("Wed 12:00", lang), check_item_name("Wed 13:00", lang), check_item_name("Wed 14:00", lang), check_item_name("Wed 15:00", lang),
        check_item_name("Thr 11:00", lang), check_item_name("Thr 12:00", lang), check_item_name("Thr 13:00", lang), check_item_name("Thr 14:00", lang), check_item_name("Thr 15:00", lang),
        check_item_name("Sky 11:00", lang), check_item_name("Sky 12:00", lang), check_item_name("Sky 13:00", lang), check_item_name("Sky 14:00", lang), check_item_name("Sky 15:00", lang),
        check_item_name("Sat 11:00", lang), check_item_name("Sat 12:00", lang), check_item_name("Sat 13:00", lang), check_item_name("Sat 14:00", lang), check_item_name("Sat 15:00", lang),
        check_item_name("Sun 11:00", lang), check_item_name("Sun 12:00", lang), check_item_name("Sun 13:00", lang), check_item_name("Sun 14:00", lang), check_item_name("Sun 15:00", lang)) & time_sanity_combined) | time_sanity_off

    can_catch_minku = (HasAny(check_item_name("22:00", lang), check_item_name("23:00", lang), check_item_name("00:00", lang), check_item_name("01:00", lang), check_item_name("02:00", lang), check_item_name("03:00", lang), check_item_name("04:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 22:00", lang), check_item_name("Mon 23:00", lang), check_item_name("Mon 00:00", lang), check_item_name("Mon 01:00", lang), check_item_name("Mon 02:00", lang), check_item_name("Mon 03:00", lang), check_item_name("Mon 04:00", lang),
        check_item_name("Tue 22:00", lang), check_item_name("Tue 23:00", lang), check_item_name("Tue 00:00", lang), check_item_name("Tue 01:00", lang), check_item_name("Tue 02:00", lang), check_item_name("Tue 03:00", lang), check_item_name("Tue 04:00", lang),
        check_item_name("Wed 22:00", lang), check_item_name("Wed 23:00", lang), check_item_name("Wed 00:00", lang), check_item_name("Wed 01:00", lang), check_item_name("Wed 02:00", lang), check_item_name("Wed 03:00", lang), check_item_name("Wed 04:00", lang),
        check_item_name("Thr 22:00", lang), check_item_name("Thr 23:00", lang), check_item_name("Thr 00:00", lang), check_item_name("Thr 01:00", lang), check_item_name("Thr 02:00", lang), check_item_name("Thr 03:00", lang), check_item_name("Thr 04:00", lang),
        check_item_name("Sky 22:00", lang), check_item_name("Sky 23:00", lang), check_item_name("Sky 00:00", lang), check_item_name("Sky 01:00", lang), check_item_name("Sky 02:00", lang), check_item_name("Sky 03:00", lang), check_item_name("Sky 04:00", lang),
        check_item_name("Sat 22:00", lang), check_item_name("Sat 23:00", lang), check_item_name("Sat 00:00", lang), check_item_name("Sat 01:00", lang), check_item_name("Sat 02:00", lang), check_item_name("Sat 03:00", lang), check_item_name("Sat 04:00", lang),
        check_item_name("Sun 22:00", lang), check_item_name("Sun 23:00", lang), check_item_name("Sun 00:00", lang), check_item_name("Sun 01:00", lang), check_item_name("Sun 02:00", lang), check_item_name("Sun 03:00", lang), check_item_name("Sun 04:00", lang)) & time_sanity_combined) | time_sanity_off

    #mayor hotelo 09:00 through 18:00

    #can_talk_to_wid = apparently you can talk to him 23:00 through 11:00

    can_talk_to_father_white = (Has(check_item_name("02:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 02:00", lang),
        check_item_name("Tue 02:00", lang),
        check_item_name("Wed 02:00", lang),
        check_item_name("Thr 02:00", lang),
        check_item_name("Sky 02:00", lang),
        check_item_name("Sat 02:00", lang),
        check_item_name("Sun 02:00", lang)) & time_sanity_combined) | time_sanity_off

    can_progress_rice_timer = (Has(check_item_name("23:00", lang)) & time_sanity_separate) | \
        (HasFromList(check_item_name("Mon 23:00", lang),
        check_item_name("Tue 23:00", lang),
        check_item_name("Wed 23:00", lang),
        check_item_name("Thr 23:00", lang),
        check_item_name("Sky 23:00", lang),
        check_item_name("Sat 23:00", lang),
        check_item_name("Sun 23:00", lang), count = 3) & time_sanity_combined) | time_sanity_off

    #18:00 - 23:00
    can_talk_to_towst = (HasAny(check_item_name("18:00", lang), check_item_name("19:00", lang), check_item_name("20:00", lang), check_item_name("21:00", lang), check_item_name("22:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 18:00", lang), check_item_name("Mon 19:00", lang), check_item_name("Mon 20:00", lang), check_item_name("Mon 21:00", lang), check_item_name("Mon 22:00", lang),
        check_item_name("Tue 18:00", lang), check_item_name("Tue 19:00", lang), check_item_name("Tue 20:00", lang), check_item_name("Tue 21:00", lang), check_item_name("Tue 22:00", lang),
        check_item_name("Wed 18:00", lang), check_item_name("Wed 19:00", lang), check_item_name("Wed 20:00", lang), check_item_name("Wed 21:00", lang), check_item_name("Wed 22:00", lang),
        check_item_name("Thr 18:00", lang), check_item_name("Thr 19:00", lang), check_item_name("Thr 20:00", lang), check_item_name("Thr 21:00", lang), check_item_name("Thr 22:00", lang),
        check_item_name("Sky 18:00", lang), check_item_name("Sky 19:00", lang), check_item_name("Sky 20:00", lang), check_item_name("Sky 21:00", lang), check_item_name("Sky 22:00", lang),
        check_item_name("Sat 18:00", lang), check_item_name("Sat 19:00", lang), check_item_name("Sat 20:00", lang), check_item_name("Sat 21:00", lang), check_item_name("Sat 22:00", lang),
        check_item_name("Sun 18:00", lang), check_item_name("Sun 19:00", lang), check_item_name("Sun 20:00", lang), check_item_name("Sun 21:00", lang), check_item_name("Sun 22:00", lang)) & time_sanity_combined) | time_sanity_off

    #18:00 - 00:00
    #can_talk_to_wanda = overlaps with towst

    #00:00 - 03:00
    #only going to count 00:00 - 02:00 so you can always get in
    vambees_open_door_or_restaurant_open = (HasAny(check_item_name("00:00", lang), check_item_name("01:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 00:00", lang), check_item_name("Mon 01:00", lang),
        check_item_name("Tue 00:00", lang), check_item_name("Tue 01:00", lang),
        check_item_name("Wed 00:00", lang), check_item_name("Wed 01:00", lang),
        check_item_name("Thr 00:00", lang), check_item_name("Thr 01:00", lang),
        check_item_name("Sky 00:00", lang), check_item_name("Sky 01:00", lang),
        check_item_name("Sat 00:00", lang), check_item_name("Sat 01:00", lang)) & time_sanity_combined) | time_sanity_off


    #00:00 - 05:00
    has_time_to_free_jon = (HasAny(check_item_name("00:00", lang), check_item_name("01:00", lang), check_item_name("02:00", lang), check_item_name("03:00", lang), check_item_name("04:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 00:00", lang), check_item_name("Mon 01:00", lang), check_item_name("Mon 02:00", lang), check_item_name("Mon 03:00", lang), check_item_name("Mon 04:00", lang),
        check_item_name("Tue 00:00", lang), check_item_name("Tue 01:00", lang), check_item_name("Tue 02:00", lang), check_item_name("Tue 03:00", lang), check_item_name("Tue 04:00", lang),
        check_item_name("Wed 00:00", lang), check_item_name("Wed 01:00", lang), check_item_name("Wed 02:00", lang), check_item_name("Wed 03:00", lang), check_item_name("Wed 04:00", lang),
        check_item_name("Thr 00:00", lang), check_item_name("Thr 01:00", lang), check_item_name("Thr 02:00", lang), check_item_name("Thr 03:00", lang), check_item_name("Thr 04:00", lang),
        check_item_name("Sky 00:00", lang), check_item_name("Sky 01:00", lang), check_item_name("Sky 02:00", lang), check_item_name("Sky 03:00", lang), check_item_name("Sky 04:00", lang),
        check_item_name("Sat 00:00", lang), check_item_name("Sat 01:00", lang), check_item_name("Sat 02:00", lang), check_item_name("Sat 03:00", lang), check_item_name("Sat 04:00", lang),
        check_item_name("Sun 00:00", lang), check_item_name("Sun 01:00", lang), check_item_name("Sun 02:00", lang), check_item_name("Sun 03:00", lang), check_item_name("Sun 04:00", lang)) & time_sanity_combined) | time_sanity_off


    #can_talk_to_fores = no time restriction
    #ant whenever

    #3:00 - 7:00
    can_pick_up_misteria = (HasAny(check_item_name("03:00", lang), check_item_name("04:00", lang), check_item_name("05:00", lang), check_item_name("06:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 03:00", lang), check_item_name("Mon 04:00", lang), check_item_name("Mon 05:00", lang), check_item_name("Mon 06:00", lang),
        check_item_name("Tue 03:00", lang), check_item_name("Tue 04:00", lang), check_item_name("Tue 05:00", lang), check_item_name("Tue 06:00", lang),
        check_item_name("Wed 03:00", lang), check_item_name("Wed 04:00", lang), check_item_name("Wed 05:00", lang), check_item_name("Wed 06:00", lang),
        check_item_name("Thr 03:00", lang), check_item_name("Thr 04:00", lang), check_item_name("Thr 05:00", lang), check_item_name("Thr 06:00", lang),
        check_item_name("Sky 03:00", lang), check_item_name("Sky 04:00", lang), check_item_name("Sky 05:00", lang), check_item_name("Sky 06:00", lang),
        check_item_name("Sat 03:00", lang), check_item_name("Sat 04:00", lang), check_item_name("Sat 05:00", lang), check_item_name("Sat 06:00", lang),
        check_item_name("Sun 03:00", lang), check_item_name("Sun 04:00", lang), check_item_name("Sun 05:00", lang), check_item_name("Sun 06:00", lang)) & time_sanity_combined) | time_sanity_off

    #Sky 7:00 - 12:00
    is_raining = (Has(check_item_name("Sky", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Sky 07:00", lang), check_item_name("Sky 08:00", lang), check_item_name("Sky 09:00", lang), check_item_name("Sky 10:00", lang), check_item_name("Sky 11:00", lang)) & time_sanity_combined) | time_sanity_off

    #18:00 - 09:00
    has_macho_left = Has(check_item_name("Guard", lang)) | \
        (HasAny(check_item_name("18:00", lang), check_item_name("19:00", lang), check_item_name("20:00", lang), check_item_name("21:00", lang), check_item_name("22:00", lang), check_item_name("23:00", lang), check_item_name("00:00", lang), check_item_name("01:00", lang), check_item_name("02:00", lang), check_item_name("03:00", lang), check_item_name("04:00", lang), check_item_name("05:00", lang), check_item_name("06:00", lang), check_item_name("07:00", lang), check_item_name("08:00", lang)) & time_sanity_separate) | \
        (HasAny(check_item_name("Mon 18:00", lang), check_item_name("Mon 19:00", lang), check_item_name("Mon 20:00", lang), check_item_name("Mon 21:00", lang), check_item_name("Mon 22:00", lang), check_item_name("Mon 23:00", lang), check_item_name("Mon 00:00", lang), check_item_name("Mon 01:00", lang), check_item_name("Mon 02:00", lang), check_item_name("Mon 03:00", lang), check_item_name("Mon 04:00", lang), check_item_name("Mon 05:00", lang), check_item_name("Mon 06:00", lang), check_item_name("Mon 07:00", lang), check_item_name("Mon 08:00", lang),
        check_item_name("Tue 18:00", lang), check_item_name("Tue 19:00", lang), check_item_name("Tue 20:00", lang), check_item_name("Tue 21:00", lang), check_item_name("Tue 22:00", lang), check_item_name("Tue 23:00", lang), check_item_name("Tue 00:00", lang), check_item_name("Tue 01:00", lang), check_item_name("Tue 02:00", lang), check_item_name("Tue 03:00", lang), check_item_name("Tue 04:00", lang), check_item_name("Tue 05:00", lang), check_item_name("Tue 06:00", lang), check_item_name("Tue 07:00", lang), check_item_name("Tue 08:00", lang),
        check_item_name("Wed 18:00", lang), check_item_name("Wed 19:00", lang), check_item_name("Wed 20:00", lang), check_item_name("Wed 21:00", lang), check_item_name("Wed 22:00", lang), check_item_name("Wed 23:00", lang), check_item_name("Wed 00:00", lang), check_item_name("Wed 01:00", lang), check_item_name("Wed 02:00", lang), check_item_name("Wed 03:00", lang), check_item_name("Wed 04:00", lang), check_item_name("Wed 05:00", lang), check_item_name("Wed 06:00", lang), check_item_name("Wed 07:00", lang), check_item_name("Wed 08:00", lang),
        check_item_name("Thr 18:00", lang), check_item_name("Thr 19:00", lang), check_item_name("Thr 20:00", lang), check_item_name("Thr 21:00", lang), check_item_name("Thr 22:00", lang), check_item_name("Thr 23:00", lang), check_item_name("Thr 00:00", lang), check_item_name("Thr 01:00", lang), check_item_name("Thr 02:00", lang), check_item_name("Thr 03:00", lang), check_item_name("Thr 04:00", lang), check_item_name("Thr 05:00", lang), check_item_name("Thr 06:00", lang), check_item_name("Thr 07:00", lang), check_item_name("Thr 08:00", lang),
        check_item_name("Sky 18:00", lang), check_item_name("Sky 19:00", lang), check_item_name("Sky 20:00", lang), check_item_name("Sky 21:00", lang), check_item_name("Sky 22:00", lang), check_item_name("Sky 23:00", lang), check_item_name("Sky 00:00", lang), check_item_name("Sky 01:00", lang), check_item_name("Sky 02:00", lang), check_item_name("Sky 03:00", lang), check_item_name("Sky 04:00", lang), check_item_name("Sky 05:00", lang), check_item_name("Sky 06:00", lang), check_item_name("Sky 07:00", lang), check_item_name("Sky 08:00", lang),
        check_item_name("Sat 18:00", lang), check_item_name("Sat 19:00", lang), check_item_name("Sat 20:00", lang), check_item_name("Sat 21:00", lang), check_item_name("Sat 22:00", lang), check_item_name("Sat 23:00", lang), check_item_name("Sat 00:00", lang), check_item_name("Sat 01:00", lang), check_item_name("Sat 02:00", lang), check_item_name("Sat 03:00", lang), check_item_name("Sat 04:00", lang), check_item_name("Sat 05:00", lang), check_item_name("Sat 06:00", lang), check_item_name("Sat 07:00", lang), check_item_name("Sat 08:00", lang),
        check_item_name("Sun 18:00", lang), check_item_name("Sun 19:00", lang), check_item_name("Sun 20:00", lang), check_item_name("Sun 21:00", lang), check_item_name("Sun 22:00", lang), check_item_name("Sun 23:00", lang), check_item_name("Sun 00:00", lang), check_item_name("Sun 01:00", lang), check_item_name("Sun 02:00", lang), check_item_name("Sun 03:00", lang), check_item_name("Sun 04:00", lang), check_item_name("Sun 05:00", lang), check_item_name("Sun 06:00", lang), check_item_name("Sun 07:00", lang), check_item_name("Sun 08:00", lang)) & time_sanity_combined) | time_sanity_off



    #how do timed minigames work *concern*
    #aqualin
    #defeat vambee soldiers (may not want to severely slow down time)
    #steamwood
    #Extinguishing

    #can access well at 09:00
    #low tide at 09:00
    has_completed_chapter_2 = is_open_world | Has("Skullpion killed")

    has_bracelet = Has(check_item_name("Bracelet", lang)) & can_enter_conners
    has_lumina = Has(check_item_name("Lumina", lang)) | is_lumina_not_randomized
    has_wind_scroll = (Has(check_item_name("Wind Scroll", lang)) & scroll_sanity_on) | (CanReachRegion("Wind Scroll") & has_lumina & scroll_sanity_off)#(has_completed_chapter_4 & can_enter_mine & has_water_scroll & has_water_boss_core & has_fire_scroll & has_fire_boss_core & has_lumina & has_bracelet)
    has_sky_scroll = (Has(check_item_name("Sky Scroll", lang)) & scroll_sanity_on)
    has_manual = Has(check_item_name("Manual", lang)) | quest_item_sanity_off
    has_skullpion_npcs = HasAll(check_item_name("SoldierA", lang), check_item_name("MercenC", lang), check_item_name("CarpentA", lang), check_item_name("KnightB", lang))
    can_complete_steamwood_1 = has_bracelet & has_manual
    has_healing = HasAny(check_item_name("W-Gel", lang), check_item_name("Progressive Drink", lang), options=heal_logic_on, filtered_resolution=True) & can_enter_grocery
    has_bread = Has(check_item_name("Progressive Bread", lang)) | bakery_sanity_off
    has_well_water = Has(check_item_name("Well H20", lang)) | quest_item_sanity_off
    can_feed_jon = has_bread & has_well_water
    has_jon_key = Has(check_item_name("Jon's Key", lang)) | quest_item_sanity_off
    has_freed_jon = can_feed_jon & has_jon_key & has_time_to_free_jon
    has_logs = Has(check_item_name("Log", lang), count=4) | (has_lumina & quest_item_sanity_off)
    can_cross_stream = Has("Can Cross Stream")
    can_reach_second_peak = can_cross_stream
    has_raft = has_freed_jon & has_logs #& can_reach_second_peak TODO for entrance rando

    has_earth_scroll = (Has(check_item_name("Earth Scroll", lang)) & scroll_sanity_on) | (has_bracelet & has_lumina & can_complete_steamwood_1 & can_cross_stream & scroll_sanity_off)
    wind_scroll_complex = has_wind_scroll & OptionFilter(WindScrollLogic, WindScrollLogic.option_complex)
    wind_scroll_simple = has_wind_scroll & OptionFilter(WindScrollLogic, WindScrollLogic.option_simple, operator="ge")
    #wind_scroll_complex_skullpion = wind_scroll_complex & (is_open_world | scroll_sanity_on)
    sky_scroll_complex = has_sky_scroll & OptionFilter(SkyScrollLogic, SkyScrollLogic.option_complex)
    sky_scroll_simple = has_sky_scroll & OptionFilter(SkyScrollLogic, SkyScrollLogic.option_simple, operator="ge")

    can_fight_skullpion = has_skullpion_npcs & has_earth_scroll & has_healing & (has_lumina | wind_scroll_complex) & (is_open_world | (has_raft & can_complete_steamwood_1)) 
    has_defeated_skullpion = can_fight_skullpion 

    can_enter_mine = (Has(check_item_name("Key", lang)) | quest_item_sanity_off) & has_completed_chapter_2
    can_double_jump = (Has(check_item_name("Ugly Belt", lang)) | (quest_item_sanity_off & has_bracelet & has_lumina & CanReachRegion("Restaurant Basement"))) & can_enter_conners

    
    has_misteria = Has(check_item_name("Misteria", lang)) | (quest_item_sanity_off & has_bracelet & can_pick_up_misteria) #& CanReachRegion("Misteria Underground Lake"))
    has_aqualin = Has(check_item_name("Aqualin", lang)) | quest_item_sanity_off
    has_rescued_tim = (has_earth_scroll | (can_double_jump & quest_item_sanity_on & sky_scroll_complex)) & has_misteria & has_aqualin & has_completed_chapter_2 & can_reach_second_peak
    has_steamwood_2_items = quest_item_sanity_off | (HasAll(check_item_name("Manual", lang), check_item_name("Handle #0", lang), check_item_name("Handle #1", lang), check_item_name("Handle #4", lang), check_item_name("Handle #8", lang), check_item_name("Profits", lang)) & quest_item_sanity_on)
    can_identify_gondola_gizmo = HasAll(check_item_name("CarpentA", lang), check_item_name("CarpentB", lang), check_item_name("CarpentC", lang))
    has_rope = has_completed_chapter_2 & ((Has(check_item_name("Rope", lang)) | ((can_double_jump | wind_scroll_complex) & quest_item_sanity_off)))
    has_water_scroll = Has(check_item_name("Water Scroll", lang)) | (has_completed_chapter_2 & has_rope & has_lumina & scroll_sanity_off)
    has_completed_chapter_3 = is_open_world | (Has("Relic Keeper killed") & has_completed_chapter_2 & (can_double_jump | wind_scroll_complex) & can_talk_to_father_white & can_enter_mine & (has_water_scroll | sky_scroll_simple))
    has_earth_boss_core = (Has("Skullpion killed") & core_sanity_off) | Has(check_item_name("Earth Boss Core", lang))
    has_water_boss_core = ((Has("Relic Keeper killed") & core_sanity_off) | Has(check_item_name("Water Boss Core", lang))) & can_enter_mine
    has_fire_boss_core = (Has("Frost Dragon killed") & core_sanity_off) | Has(check_item_name("Fire Boss Core", lang))
    has_wind_boss_core = (Has("Queen Ant killed") & core_sanity_off) | Has(check_item_name("Wind Boss Core", lang))
    has_fixed_well = has_water_scroll & has_water_boss_core & can_enter_mine
    has_fixed_gondola = has_completed_chapter_3 & can_identify_gondola_gizmo & has_fixed_well & (Has(check_item_name("Gondola Gizmo", lang)) | quest_item_sanity_off)
    
    has_completed_chapter_4 = is_open_world | (Has("Frost Dragon killed") & has_completed_chapter_3 & has_fixed_gondola)
    has_completed_chapter_5 = is_open_world | (Has("Queen Ant killed") & has_completed_chapter_4)
    can_complete_steamwood_2 = has_completed_chapter_4 & can_double_jump & has_bracelet & has_steamwood_2_items
    has_salt = has_completed_chapter_3 & (Has(check_item_name("Rock Salt", lang)) | (has_fixed_gondola & quest_item_sanity_off))
    has_angel_statue = has_completed_chapter_2 & (((has_water_scroll | sky_scroll_simple) & can_enter_mine & has_rescued_tim & (can_double_jump | wind_scroll_complex) & quest_item_sanity_off) | Has(check_item_name("Angel Statue", lang)))
    can_rescue_princess = has_salt & has_water_boss_core & has_water_scroll & has_lumina & (can_double_jump | wind_scroll_simple)
    can_enter_frozen_palace = HasAll(check_item_name("MercenA", lang), check_item_name("MercenB", lang), check_item_name("MercenC", lang)) & (is_open_world | can_rescue_princess)
    has_fire_scroll = Has(check_item_name("Fire Scroll", lang)) | (can_rescue_princess & scroll_sanity_off)
    has_saved_princess = is_open_world | (has_completed_chapter_3 & can_rescue_princess)
    can_fight_frost_dragon = HasAll(check_item_name("Red Eye", lang), check_item_name("Blue Eye", lang), check_item_name("Green Eye", lang), check_item_name("Red Shoes", lang)) & has_fire_scroll & has_lumina & can_double_jump & has_healing
    has_all_scrolls = has_earth_scroll & has_water_scroll & has_fire_scroll & has_wind_scroll & (has_sky_scroll | scroll_sanity_off)
    
    berries_needed = math.ceil((world.options.max_hp_logic.value - world.options.starting_hp) / 25.0)
    if(berries_needed > 1):
        berries_needed = berries_needed - (world.options.quest_item_sanity.value == False) #account for free mayor berry
    berries_needed = max(min(14 - (world.options.quest_item_sanity.value == False), berries_needed), 0)
    
    has_hp_for_soda_fountain = OptionFilter(StartingMaxHP, 1) | Has(check_item_name("Longevity Berry", lang), count=berries_needed)
    has_ex_drink = (Has(check_item_name("Progressive Drink", lang), count=2) | grocery_sanity_off) & can_enter_grocery
    has_defeated_needed_bosses = (True_() & OptionFilter(ForceSodaFountainToBeLast, False)) | (True_() & OptionFilter(SetGoal, SetGoal.option_defeat_sky_crest_guardian)) | (True_() & OptionFilter(SetGoal, SetGoal.option_defeat_final_boss)) | (OptionFilter(SetGoal, SetGoal.option_defeat_x_crest_guardian) & Has("Boss killed", count=world.options.guardian_goal.value-1)) | Has("Boss killed", count=4)
    has_rice = HasAll(check_item_name("Bailiff", lang), check_item_name("CookA", lang)) & can_progress_rice_timer
    has_orange = ((Has(check_item_name("Orange", lang)) | grocery_sanity_off) & has_rescued_tim) & can_enter_grocery


    world.set_rule(world.get_entrance("Grillin Village -> Defeat First Boss"), Has("Boss killed"))
    world.set_rule(world.get_entrance("Defeat First Boss -> Defeat Second Boss"), Has("Boss killed", count=2))
    world.set_rule(world.get_entrance("Defeat Second Boss -> Defeat Third Boss"), Has("Boss killed", count=3))
    world.set_rule(world.get_entrance("Defeat Third Boss -> Defeat Fourth Boss"), Has("Boss killed", count=4))
    world.set_rule(world.get_entrance("Upper Grillin Village -> Twinpeak Entrance"), has_macho_left)
    world.set_rule(world.get_entrance("Grillin Village -> Mine Entrance"), can_enter_mine)
    world.set_rule(world.get_entrance("Grillin Village -> Restaurant Basement"), has_rescued_tim & can_talk_to_towst & vambees_open_door_or_restaurant_open)
    world.set_rule(world.get_entrance("Restaurant Basement Bowling 1 -> Restaurant Basement Bowling 2"), has_lumina)
    world.set_rule(world.get_entrance("Restaurant Basement Before Bowling 1 -> Restaurant Basement Bowling 1"), has_bracelet)
    world.set_rule(world.get_entrance("Meandering Forest -> Graveyard"), can_feed_jon)
    world.set_rule(world.get_entrance("Steamwood Forest -> Steamwood 2"), can_complete_steamwood_2)
    if(options.toy_sanity.value == True):
        world.set_rule(world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 3"), has_completed_chapter_2)
        world.set_rule(world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 4"), has_completed_chapter_3 & can_enter_frozen_palace)
        world.set_rule(world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 5"), has_completed_chapter_4)
    world.set_rule(world.get_entrance("Twinpeak Entrance -> Twinpeak Path to Skullpion"), has_earth_scroll | sky_scroll_simple)
    world.set_rule(world.get_entrance("Twinpeak Entrance -> Twinpeak Around the Bend"), has_freed_jon | has_water_scroll | sky_scroll_simple | can_double_jump | wind_scroll_complex)
    world.set_rule(world.get_entrance("Twinpeak Path to Skullpion -> Skullpion Arena"), can_fight_skullpion)
    world.set_rule(world.get_entrance("Restaurant Basement -> Restaurant Basement Path to Crest Guardian"), (has_angel_statue & can_double_jump & has_water_scroll) | sky_scroll_complex)
    world.set_rule(world.get_entrance("Restaurant Basement Path to Crest Guardian -> Relic Keeper Arena"), has_water_scroll & has_healing & has_lumina)
    world.set_rule(world.get_entrance("Somnolent Forest -> Island of Dragons"), has_salt)
    world.set_rule(world.get_entrance("Somnolent Forest -> Somnolent Forest Behind Steam"), can_complete_steamwood_1)
    world.set_rule(world.get_entrance("Grillin Village -> Grillin Reservoir"), has_completed_chapter_2 & has_rope)
    world.set_rule(world.get_entrance("Mine Entrance -> Grillin Reservoir"), has_water_scroll | sky_scroll_simple)
    world.set_rule(world.get_entrance("Grillin Reservoir -> Mine Entrance"), has_water_scroll | sky_scroll_simple)
    world.set_rule(world.get_entrance("Mine Entrance -> Scrap Depository"), can_identify_gondola_gizmo & (can_double_jump | sky_scroll_complex) & has_completed_chapter_3 & (has_fixed_well | is_open_world))
    world.set_rule(world.get_entrance("Grillin Reservoir -> Reservoir Tunnel"), has_fixed_well)
    world.set_rule(world.get_entrance("Reservoir Tunnel -> Wind Scroll"), has_fire_boss_core & has_fire_scroll & has_bracelet)
    world.set_rule(world.get_entrance("Meandering Forest -> Frozen Palace Entrance"), can_enter_frozen_palace & has_saved_princess)
    world.set_rule(world.get_entrance("Frozen Palace Entrance -> Frozen Palace Red Eye Room"), can_double_jump | wind_scroll_complex | sky_scroll_simple)
    world.set_rule(world.get_entrance("Frozen Palace Entrance -> Frozen Palace Red Eye Door"), (Has(check_item_name("Red Eye", lang)) & (can_double_jump | wind_scroll_simple)) | sky_scroll_complex)
    world.set_rule(world.get_entrance("Frozen Palace Entrance -> Frozen Palace Blue Eye Door"), Has(check_item_name("Blue Eye", lang)))
    world.set_rule(world.get_entrance("Frozen Palace Entrance -> Frozen Palace Atrium Left Balcony"), sky_scroll_complex & (Has(check_item_name("Red Shoes", lang)) | can_double_jump | wind_scroll_complex))
    world.set_rule(world.get_entrance("Frozen Palace Blue Eye Door -> Frozen Palace Atrium Left Balcony"), can_double_jump | wind_scroll_simple) 
    world.set_rule(world.get_entrance("Frozen Palace Entrance -> Frozen Palace Green Eye Maze"), Has(check_item_name("Red Shoes", lang)) | sky_scroll_complex)
    world.set_rule(world.get_entrance("Frozen Palace Green Eye Maze -> Frozen Palace Atrium Right Balcony"), sky_scroll_complex)
    world.set_rule(world.get_entrance("Frozen Palace Entrance -> Frost Dragon Door"), can_fight_frost_dragon)
    world.set_rule(world.get_entrance("Upper Grillin Village -> Upper Mines"), has_completed_chapter_4 & has_bracelet & has_fire_boss_core & has_fire_scroll & has_fixed_well & has_fixed_gondola & (wind_scroll_simple | can_double_jump | sky_scroll_simple))
    world.set_rule(world.get_entrance("Upper Mines -> Upper Mines Behind Poison"), has_wind_scroll)
    world.set_rule(world.get_entrance("Upper Mines Behind Poison -> Upper Mines Poison Elevators"), (has_earth_scroll | sky_scroll_complex) & can_double_jump)
    world.set_rule(world.get_entrance("Upper Mines Poison Elevators -> Queen Ant Arena"), has_lumina & has_healing)
    world.set_rule(world.get_entrance("Steamwood Forest -> Sky Island"), has_earth_scroll & has_water_scroll & has_fire_scroll & has_wind_scroll & has_wind_boss_core & has_earth_boss_core & has_lumina & has_bracelet & (can_double_jump | sky_scroll_simple) & is_raining)
    world.set_rule(world.get_entrance("Sky Island -> Soda Fountain"), has_all_scrolls & can_double_jump & has_lumina & has_bracelet & has_hp_for_soda_fountain & has_ex_drink & has_defeated_needed_bosses)
    if(options.time_sanity.value == True):
        world.set_rule(world.get_entrance("Grillin Village -> Hilda's Grocery"), can_enter_grocery)
        if(options.toy_sanity.value == True):
            world.set_rule(world.get_entrance("Grillin Village -> Toy Shop Series 1"), can_enter_toy_shop)
        if(options.restaurant_sanity.value == True):
            world.set_rule(world.get_entrance("Grillin Village -> Restaurant"), can_enter_restaurant)


#def set_location_rules(world: "BFMWorld", lang: bool) -> None:
#    player = world.player
#    options = world.options
    loc_lang = options.set_lang.value == 2 and (options.spoiler_items_in_english.value == False or world.using_ut == True)
    bincho_rules: Dict[str, Rules] = {name: has_lumina for name in location_name_groups["Bincho"]}
    if(options.level_sanity.value == True and options.starting_hp.value != 1):
        for index, name in enumerate(location_name_groups["Level"]):
            if("Lum" in name):
                world.set_rule(world.get_location(check_location_name(name, loc_lang)), has_lumina) 
    bp_rules: Dict[str, Rules] = {}
    if(options.bp_sanity.value == True):

        bp_rules = {name: has_lumina for name in location_name_groups["BP"] if(not "Defeat" in name)}
        bp_rules["Weaver BP Up - Twinpeak Second Peak"] = bp_rules["Weaver BP Up - Twinpeak Second Peak"] & (can_double_jump | sky_scroll_simple)
        bp_rules["Chef BP Up - Frozen Palace Crate Pile"] = bp_rules["Chef BP Up - Frozen Palace Crate Pile"] & (can_double_jump | wind_scroll_complex)
        bp_rules["MusicianC BP Up - Frozen Palace Green Eye Maze"] = bp_rules["MusicianC BP Up - Frozen Palace Green Eye Maze"] & (can_double_jump | wind_scroll_complex)
        #for index, name in enumerate(location_name_groups["BP"]):
        #    if(not "Defeat" in name):
        #        set_rule(world.get_location(check_location_name(name, lang)), lambda state: has_lumina(state, world))
        #add_rule(world.get_location(check_location_name("Weaver BP Up - Twinpeak Second Peak", lang)),
        #    lambda state: can_double_jump(state, world) or has_sky_scroll_simple(state, world)) 
        #add_rule(world.get_location(check_location_name("Chef BP Up - Frozen Palace Crate Pile", lang)),
        #    lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world))
        #add_rule(world.get_location(check_location_name("MusicianC BP Up - Frozen Palace Green Eye Maze", lang)),
        #    lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world))

    if(options.quest_item_sanity.value == True):
        bincho_rules["Doctor Bincho - Twinpeak Around the Bend"] = bincho_rules["Doctor Bincho - Twinpeak Around the Bend"] & (has_raft | has_water_scroll | sky_scroll_simple)
        #add_rule(world.get_location(check_location_name("Doctor Bincho - Twinpeak Around the Bend", lang)),
        #    lambda state: has_raft(state, world) or has_water_scroll(state,world) or has_sky_scroll_simple(state, world)) 
        if(options.bp_sanity.value == True):
            bp_rules["Doctor BP Up - Twinpeak Around the Bend"] = bp_rules["Doctor BP Up - Twinpeak Around the Bend"] & (has_raft | has_water_scroll | sky_scroll_simple)
            #add_rule(world.get_location(check_location_name("Doctor BP Up - Twinpeak Around the Bend", lang)),
            #    lambda state: has_raft(state, world) or has_water_scroll(state,world) or has_sky_scroll_simple(state, world)) 
        world.set_rule(world.get_location(check_location_name("First Log - Twinpeak Second Peak", loc_lang)), has_lumina)
        world.set_rule(world.get_location(check_location_name("Second Log - Twinpeak Second Peak", loc_lang)), has_lumina)
        world.set_rule(world.get_location(check_location_name("Third Log - Twinpeak Second Peak", loc_lang)), has_lumina)
        world.set_rule(world.get_location(check_location_name("Fourth Log - Twinpeak Second Peak", loc_lang)), has_lumina)
        world.set_rule(world.get_location(check_location_name("Agree to Fix Steamwood - Grillin Village", loc_lang)), has_bracelet)
        world.set_rule(world.get_location(check_location_name("Mayor Berry - Grillin Village", loc_lang)), has_bracelet & Has(check_item_name("Manual", lang)))
        world.set_rule(world.get_location(check_location_name("Key from Wid - Grillin Village", loc_lang)), has_completed_chapter_2)
        world.set_rule(world.get_location(check_location_name("Aqualin - Twinpeak Second Peak", loc_lang)), has_rescued_tim)
        world.set_rule(world.get_location(check_location_name("Rescue Tim - Grillin Village", loc_lang)), has_rescued_tim)
        world.set_rule(world.get_location(check_location_name("Defeat Vambee Soldiers - Grillin Village", loc_lang)), has_completed_chapter_2 & (can_double_jump | wind_scroll_complex) & can_talk_to_father_white)
        world.set_rule(world.get_location(check_location_name("Return Bell - Grillin Village", loc_lang)), has_rescued_tim & (can_double_jump | wind_scroll_complex) & can_enter_mine & (has_water_scroll | sky_scroll_simple))
        world.set_rule(world.get_location(check_location_name("Mrs Govern's Pie - Grillin Village", loc_lang)), has_completed_chapter_3 & has_fixed_well)
        world.set_rule(world.get_location(check_location_name("Reward #1 After Extinguishing Village - Grillin Village", loc_lang)), has_completed_chapter_3 & has_fixed_gondola)
        world.set_rule(world.get_location(check_location_name("Reward #2 After Extinguishing Village - Grillin Village", loc_lang)), has_completed_chapter_3 & has_fixed_gondola)
        world.set_rule(world.get_location(check_location_name("Jon's Note - Somnolent Forest Deadend", loc_lang)), Has("Queen Ant killed"))
        world.set_rule(world.get_location(check_location_name("Ugly Belt - Restaurant Basement", loc_lang)), has_lumina & has_bracelet)#eventually will need to add requirements for four eyes
    
    bincho_rules["Weaver Bincho - Twinpeak Second Peak"] = bincho_rules["Weaver Bincho - Twinpeak Second Peak"] & (can_double_jump | sky_scroll_simple)
    #add_rule(world.get_location(check_location_name("Weaver Bincho - Twinpeak Second Peak", lang)),
    #    lambda state: can_double_jump(state, world) or has_sky_scroll_simple(state, world)) 
    world.set_rule(world.get_location(check_location_name("Minku - Twinpeak End of Stream", loc_lang)), (has_water_scroll | sky_scroll_simple) & can_catch_minku)
    world.set_rule(world.get_location(check_location_name("Minku - Steamwood Forest", loc_lang)), has_earth_boss_core & has_earth_scroll & has_bracelet & can_catch_minku)
    world.set_rule(world.get_location(check_location_name("Minku - Somnolent Forest", loc_lang)), (has_water_scroll | sky_scroll_simple) & can_catch_minku)
    if(options.bakery_sanity.value == True):
        world.set_rule(world.get_location(check_location_name("Item 6 (JamBread) - Bakery", loc_lang)), Has("Boss killed", count=2))
        world.set_rule(world.get_location(check_location_name("Item 7 (Biscuit) - Bakery", loc_lang)), Has("Boss killed", count=2))
    if(options.grocery_sanity.value == True):
        world.set_rule(world.get_location(check_location_name("Item 8 (Orange) - Grocery", loc_lang)), has_rescued_tim)#orange, save Tim
        world.set_rule(world.get_location(check_location_name("Item 9 (EX-Drink) - Grocery", loc_lang)), Has("Boss killed", count=2)) #Chapter 4 EX-Drink
        world.set_rule(world.get_location(check_location_name("Item 10 (H-Mint) - Grocery", loc_lang)), Has("Boss killed", count=2)) #Chapter 4 H-Mint
        world.set_rule(world.get_location(check_location_name("Item 11 (Riceball) - Grocery", loc_lang)), has_rice & Has(check_item_name("Chef", lang))) #rice ball
        world.set_rule(world.get_location(check_location_name("Item 12 (Neat Ball) - Grocery", loc_lang)), has_rice & HasAll(check_item_name("CookB", lang), check_item_name("Butcher", lang))) #neatball
    world.set_rule(world.get_location(check_location_name("Minku - Grillin Village Above Gondola", loc_lang)), has_bracelet & can_catch_minku)
    world.set_rule(world.get_location(check_location_name("Aged Coin Chest - Steamwood Forest", loc_lang)), has_bracelet)
    if(options.scroll_sanity.value == True):
        world.set_rule(world.get_location(check_location_name("Earth Scroll - Twinpeak First Peak", loc_lang)), has_lumina & can_complete_steamwood_1)
        world.set_rule(world.get_location(check_location_name("Water Scroll - Grillin Reservoir", loc_lang)), has_lumina)
        world.set_rule(world.get_location(check_location_name("Fire Scroll - Island of Dragons", loc_lang)), can_rescue_princess & has_lumina)
        world.set_rule(world.get_location(check_location_name("Wind Scroll - Grillin Volcano", loc_lang)), has_lumina)
    world.set_rule(world.get_location(check_location_name("Rock Chest - Twinpeak Second Peak", loc_lang)), has_earth_scroll | (can_double_jump & sky_scroll_complex))
    world.set_rule(world.get_location(check_location_name("Bracelet Chest - Twinpeak Entrance", loc_lang)), has_raft | has_water_scroll | sky_scroll_simple)
    world.set_rule(world.get_location(check_location_name("200 Drans Chest - Twinpeak Path to Skullpion", loc_lang)), ((has_water_scroll | sky_scroll_simple | has_raft) & has_earth_scroll) | sky_scroll_complex)
    world.set_rule(world.get_location(check_location_name("Glasses Chest - Somnolent Forest", loc_lang)), has_water_scroll & has_water_boss_core)
    world.set_rule(world.get_location(check_location_name("Minku - Grillin Reservoir", loc_lang)), ((has_water_scroll & has_water_boss_core) | sky_scroll_simple) & can_catch_minku)    
    world.set_rule(world.get_location(check_location_name("Old Shirt Chest - Grillin Reservoir", loc_lang)), (has_water_scroll & has_water_boss_core) | sky_scroll_simple)   
    world.set_rule(world.get_location(check_location_name("Used Boot Chest - Grillin Reservoir", loc_lang)), has_water_scroll & has_water_boss_core)
    bincho_rules["Chef Bincho - Frozen Palace Crate Pile"] = bincho_rules["Chef Bincho - Frozen Palace Crate Pile"] & (can_double_jump | wind_scroll_complex)
    #add_rule(world.get_location(check_location_name("Chef Bincho - Frozen Palace Crate Pile", lang)),
    #    lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world))
    world.set_rule(world.get_location(check_location_name("White Cloth Chest - Frozen Palace Green Eye Maze", loc_lang)), can_double_jump | wind_scroll_complex)
    bincho_rules["MusicianC Bincho - Frozen Palace Green Eye Maze"] = bincho_rules["MusicianC Bincho - Frozen Palace Green Eye Maze"] & (can_double_jump | wind_scroll_complex)
    #add_rule(world.get_location(check_location_name("MusicianC Bincho - Frozen Palace Green Eye Maze", lang)),
    #    lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world))
    
    if(options.toy_sanity.value == True):
        world.set_rule(world.get_location(check_location_name("Skullpion - Toy Shop", loc_lang)), Has("Skullpion killed"))
        world.set_rule(world.get_location(check_location_name("Ed & Ben - Toy Shop", loc_lang)), has_fixed_well)
        world.set_rule(world.get_location(check_location_name("Relic Keeper - Toy Shop", loc_lang)), Has("Relic Keeper killed"))
        world.set_rule(world.get_location(check_location_name("Frost Dragon - Toy Shop", loc_lang)), Has("Frost Dragon killed"))
        world.set_rule(world.get_location(check_location_name("Slow Guy - Toy Shop", loc_lang)), (HasAny(check_item_name("Red Eye", lang), check_item_name("Blue Eye", lang)) & (can_double_jump | wind_scroll_simple)) | HasAll(check_item_name("Green Eye", lang), check_item_name("Red Shoes", lang)) | sky_scroll_complex)
        world.set_rule(world.get_location(check_location_name("Stomp Golem - Toy Shop", loc_lang)), (Has(check_item_name("Red Eye", lang)) & (can_double_jump | wind_scroll_simple)) | HasAll(check_item_name("Green Eye", lang), check_item_name("Red Shoes", lang)) | sky_scroll_complex)
        world.set_rule(world.get_location(check_location_name("GiAnt - Toy Shop", loc_lang)), CanReachRegion("Upper Mines Ant Parade"))
        world.set_rule(world.get_location(check_location_name("Queen Ant - Toy Shop", loc_lang)), Has("Queen Ant killed"))
        world.set_rule(world.get_location(check_location_name("Toad Stool - Toy Shop", loc_lang)), CanReachRegion("Upper Mines Behind Poison") | CanReachRegion("Mine Entrance"))
        world.set_rule(world.get_location(check_location_name("Colonel Capricola - Toy Shop", loc_lang)), Has("Frost Dragon killed"))
        world.set_rule(world.get_location(check_location_name("Relic Vambee - Toy Shop", loc_lang)), CanReachRegion("Restaurant Basement"))
        world.set_rule(world.get_location(check_location_name("Bowler - Toy Shop", loc_lang)), CanReachRegion("Restaurant Basement Before Bowling 1"))
        world.set_rule(world.get_location(check_location_name("Cure Worm - Toy Shop", loc_lang)), CanReachRegion("Reservoir Tunnel") | (CanReachRegion("Mine Entrance") & has_bracelet))
        world.set_rule(world.get_location(check_location_name("Topo - Toy Shop", loc_lang)), can_complete_steamwood_2)
        world.set_rule(world.get_location(check_location_name("Vambee Soldier - Toy Shop", loc_lang)), has_completed_chapter_2 & (can_double_jump | wind_scroll_complex) & can_talk_to_father_white)
            #lambda state: has_rescued_tim(state, world) and can_double_jump(state, world))
        world.set_rule(world.get_location(check_location_name("Bubbles - Toy Shop", loc_lang)), has_completed_chapter_2 & (can_double_jump | wind_scroll_complex) & can_talk_to_father_white)
            #lambda state: has_rescued_tim(state, world) and can_double_jump(state, world))
    if(options.tech_sanity.value == True):
        world.set_rule(world.get_location(check_location_name("Improved Fusion (Artisan) - Allucaneet Castle", loc_lang)), Has(check_item_name("Artisan", lang)))
        world.set_rule(world.get_location(check_location_name("Dashing Pierce (Maid) - Allucaneet Castle", loc_lang)), Has(check_item_name("Maid", lang)))
        world.set_rule(world.get_location(check_location_name("Shish Kebab (Clown) - Allucaneet Castle", loc_lang)), Has(check_item_name("Acrobat", lang)) & has_orange)
        world.set_rule(world.get_location(check_location_name("Crosswise Cut (KnightB) - Allucaneet Castle", loc_lang)), Has("Skullpion killed"))
        world.set_rule(world.get_location(check_location_name("Tenderize (KnightA) - Allucaneet Castle", loc_lang)), Has(check_item_name("KnightA", lang)))
        world.set_rule(world.get_location(check_location_name("Desperado Attack (KnightC) - Allucaneet Castle", loc_lang)), HasAll(check_item_name("KnightC", lang), check_item_name("Crosswise Cut", lang)))
        world.set_rule(world.get_location(check_location_name("Rumparoni Special (KnightD) - Allucaneet Castle", loc_lang)), Has(check_item_name("KnightD", lang)))
    if(options.time_sanity.value == True):
        world.set_rule(world.get_location(check_location_name("Minku - Grillin Village Near Twinpeak", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Somnolent Forest Hidden Path", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Twinpeak Around the Bend", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Skullpion Arena", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Misteria Underground Lake", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Upper Mines Below Big Fan", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Upper Mines", loc_lang)), can_catch_minku)
        world.set_rule(world.get_location(check_location_name("Minku - Near Wind Scroll", loc_lang)), can_catch_minku)
        if(options.toy_sanity.value == True):
            world.set_rule(world.get_location(check_location_name("King Man Eater - Toy Shop", loc_lang)), has_macho_left)
        if(options.quest_item_sanity.value == True):
            world.set_rule(world.get_location(check_location_name("Misteria - Misteria Underground Lake", loc_lang)), can_pick_up_misteria)
        if(options.time_sanity_settings.value == 1): #separate
            world.set_rule(world.get_location(check_location_name("Reach Tue", loc_lang)), Has(check_item_name("Tue", lang)))
            world.set_rule(world.get_location(check_location_name("Reach Wed", loc_lang)), Has(check_item_name("Wed", lang)))
            world.set_rule(world.get_location(check_location_name("Reach Thr", loc_lang)), Has(check_item_name("Thr", lang)))
            world.set_rule(world.get_location(check_location_name("Reach Sky", loc_lang)), Has(check_item_name("Sky", lang)))
            world.set_rule(world.get_location(check_location_name("Reach Sat", loc_lang)), Has(check_item_name("Sat", lang)))
            world.set_rule(world.get_location(check_location_name("Reach Sun", loc_lang)), Has(check_item_name("Sun", lang)))
            for i in range(24):
                if(i != 9):
                    world.set_rule(world.get_location(check_location_name("Reach " + "0" * (i < 10) + f"{i}" + ":00", loc_lang)), Has(check_item_name("0" * (i < 10) + f"{i}" + ":00", lang)))
        else:
            for day in days_of_week:
                for i in range(24):
                    if(i != 9 or day != "Mon"):
                        world.set_rule(world.get_location(check_location_name("Reach " + day + " " + "0" * (i < 10) + f"{i}" + ":00", loc_lang)), Has(check_item_name(day + " " +"0" * (i < 10) + f"{i}" + ":00", lang)))




    
    for name in bincho_rules:
        world.set_rule(world.get_location(check_location_name(name, loc_lang)), bincho_rules[name])

    for name in bp_rules:
        world.set_rule(world.get_location(check_location_name(name, loc_lang)), bp_rules[name])