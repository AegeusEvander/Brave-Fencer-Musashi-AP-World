from itertools import groupby
from typing import Dict, List, Set, NamedTuple, Optional
from BaseClasses import ItemClassification as IC


class BFMItemData(NamedTuple):
    classification: IC
    quantity_in_item_pool: int
    item_id_offset: int
    item_group: str = ""
    jp_name: Optional[str] = None


item_base_id = 0x0ba1b8
item_action_figure_id = 0x100
scroll_base_id = 0x200
core_base_id = 0x300
level_base_id = 0x400
quest_base_id = 0x500
jp_id_offset = 0x0c0000

item_table: Dict[str, BFMItemData] = {
    "Guard": BFMItemData(IC.progression, 1, 0x40, "NPC", jp_name = "みはりのナミロス"),
    "Seer": BFMItemData(IC.progression, 1, 0x41, "NPC", jp_name = "うらないしギアラ"),
    "Hawker": BFMItemData(IC.progression, 1, 0x42, "NPC", jp_name = "たかじょうトクセン"),
    "Maid": BFMItemData(IC.progression, 1, 0x43, "NPC", jp_name = "そうじふジョミーノ"),
    "MusicianB": BFMItemData(IC.progression, 1, 0x44, "NPC", jp_name = "フーソッシモがくし"),
    "SoldierA": BFMItemData(IC.progression, 1, 0x45, "NPC", jp_name = "ヘいしバラニック"),
    "MercenC": BFMItemData(IC.progression, 1, 0x46, "NPC", jp_name = "ようへいミーノ"),
    "CarpentA": BFMItemData(IC.progression, 1, 0x47, "NPC", jp_name = "だいくツケコンデル"),
    "KnightB": BFMItemData(IC.progression, 1, 0x48, "NPC", jp_name = "きしラド"),
    "Shepherd": BFMItemData(IC.progression, 1, 0x49, "NPC", jp_name = "うまやばんバッサシ"),
    "Bailiff": BFMItemData(IC.progression, 1, 0x4a, "NPC", jp_name = "グラムだいかん"),
    "Taster": BFMItemData(IC.progression, 1, 0x4b, "NPC", jp_name = "9だいめどくみやく"),
    "CarpentB": BFMItemData(IC.progression, 1, 0x4c, "NPC", jp_name = "だいくニコミテール"),
    "Weaver": BFMItemData(IC.progression, 1, 0x4d, "NPC", jp_name = "つむぎてエイランチ"),
    "SoldierB": BFMItemData(IC.progression, 1, 0x4e, "NPC", jp_name = "へいしバーベック"),
    "KnightA": BFMItemData(IC.progression, 1, 0x4f, "NPC", jp_name = "きしニック"),
    "CookA": BFMItemData(IC.progression, 1, 0x50, "NPC", jp_name = "しょくじがかりリブ"),
    "Acrobat": BFMItemData(IC.progression, 1, 0x51, "NPC", jp_name = "きょくげいしナムル"),
    "MercenB": BFMItemData(IC.progression, 1, 0x52, "NPC", jp_name = "ようへいカルビ"),
    "Janitor": BFMItemData(IC.progression, 1, 0x53, "NPC", jp_name = "ベんじょのニクジル"),
    "Artisan": BFMItemData(IC.progression, 1, 0x54, "NPC", jp_name = "かじやのトック"),
    "CarpentC": BFMItemData(IC.progression, 1, 0x55, "NPC", jp_name = "おやかたマーダレー"),
    "MusicianC": BFMItemData(IC.progression, 1, 0x56, "NPC", jp_name = "ビビンバッハガくし"),
    "Knitter": BFMItemData(IC.progression, 1, 0x57, "NPC", jp_name = "ぬのがかりビセット"),
    "Chef": BFMItemData(IC.progression, 1, 0x58, "NPC", jp_name = "クーパー・シェフ"),
    "MercenA": BFMItemData(IC.progression, 1, 0x59, "NPC", jp_name = "ようへいロースウ"),
    "Chief": BFMItemData(IC.progression, 1, 0x5a, "NPC", jp_name = "ビールかんとく"),
    "CookB": BFMItemData(IC.progression, 1, 0x5b, "NPC", jp_name = "ムッシュ・ワギュウ"),
    "Conductor": BFMItemData(IC.progression, 1, 0x5c, "NPC", jp_name = "おんがくだんちょう"),
    "Butcher": BFMItemData(IC.progression, 1, 0x5d, "NPC", jp_name = "にくきりハーラミン"),
    "KnightC": BFMItemData(IC.progression, 1, 0x5e, "NPC", jp_name = "きしコブクローネ"),
    "Doctor": BFMItemData(IC.progression, 1, 0x5f, "NPC", jp_name = "モルホンいし"),
    "KnightD": BFMItemData(IC.progression, 1, 0x60, "NPC", jp_name = "きしだんちょう"),
    "Alchemist": BFMItemData(IC.progression, 1, 0x61, "NPC", jp_name = "れんきんじゃつし"),
    "Librarian": BFMItemData(IC.progression, 1, 0x62, "NPC", jp_name = "ゾウモッツしょき"),
    "Longevity Berry": BFMItemData(IC.progression, 13, 0x63 + item_base_id, "Stat Up", jp_name = "チョウジュベリー"),
    "Rock": BFMItemData(IC.useful, 1, 0x13, "Chest Reward", jp_name = "かがやくいし"),
    "Old Sword": BFMItemData(IC.filler, 1, 0x15, "Chest Reward", jp_name = "さびたつるぎ"),
    "Shield": BFMItemData(IC.filler, 1, 0x17, "Chest Reward", jp_name = "ふるびたタテ"),
    "Old Book": BFMItemData(IC.filler, 1, 0x19, "Chest Reward", jp_name = "しめったしょもつ"),
    "Aged Coin": BFMItemData(IC.filler, 1, 0x1b, "Chest Reward", jp_name = "あなあきコイン"),
    "Old Crown": BFMItemData(IC.filler, 1, 0x1d, "Chest Reward", jp_name = "すすけたかんむり"),
    "Old Pipe": BFMItemData(IC.filler, 1, 0x1f, "Chest Reward", jp_name = "あなあきこんぼう"),
    "Odd Hat": BFMItemData(IC.filler, 1, 0x21, "Chest Reward", jp_name = "ひびわれ・かめん"),
    "Dagger": BFMItemData(IC.filler, 1, 0x23, "Chest Reward", jp_name = "ふるびたたんけん"),
    "Powder": BFMItemData(IC.filler, 1, 0x25, "Chest Reward", jp_name = "しろいこな"),
    "Cloth": BFMItemData(IC.useful, 1, 0x27, "Chest Reward", jp_name = "あつでのまきぬの"),
    "Helmet": BFMItemData(IC.filler, 1, 0x29, "Chest Reward", jp_name = "ゆがんだツボ"),
    "Used Boot": BFMItemData(IC.filler, 1, 0x2b, "Chest Reward", jp_name = "よれよれながぐつ"),
    "Old Glove": BFMItemData(IC.filler, 1, 0x2d, "Chest Reward", jp_name = "ほつれたてぶくろ"),
    "Armor": BFMItemData(IC.filler, 1, 0x2f, "Chest Reward", jp_name = "ヘこんだヨロイ"),
    "Long Tube": BFMItemData(IC.useful, 1, 0x31, "Chest Reward", jp_name = "とんがりばう"),
    "Red Cloth": BFMItemData(IC.filler, 1, 0x33, "Chest Reward", jp_name = "あかいぬのきれ"),
    "White Cloth": BFMItemData(IC.filler, 1, 0x35, "Chest Reward", jp_name = "しろいぬのきれ"),
    "Black Cloth": BFMItemData(IC.filler, 1, 0x37, "Chest Reward", jp_name = "くろいぬのきれ"),
    "Large Tool": BFMItemData(IC.filler, 1, 0x39, "Chest Reward", jp_name = "スルドイどうぐ"),
    "Odd Bone": BFMItemData(IC.filler, 1, 0x3b, "Chest Reward", jp_name = "しんぴのほねぐみ"),
    "Bracelet": BFMItemData(IC.progression, 1, 0x49, "Chest Reward", jp_name = "おおきなうでわ"),
    "Old Shirt": BFMItemData(IC.useful, 1, 0x4a, "Chest Reward", jp_name = "よれよれシャツ"),
    "Red Shoes": BFMItemData(IC.progression, 1, 0x4b, "Chest Reward", jp_name = "まっかなボロぐつ"),
    "Red Eye": BFMItemData(IC.progression, 1, 0x60, "Chest Reward", jp_name = "レッドアイ"),
    "Blue Eye": BFMItemData(IC.progression, 1, 0x61, "Chest Reward", jp_name = "ブルーアイ"),
    "Green Eye": BFMItemData(IC.progression, 1, 0x62, "Chest Reward", jp_name = "グリーンアイ"),
    "1000 Drans": BFMItemData(IC.filler, 0, 0x78, "Chest Reward", jp_name = "1000ドラン"), # moving 6 to 0 to allow for dynamic filler levels
    "Lumina": BFMItemData(IC.progression | IC.useful, 1, 0x79, "Equipment", jp_name = "レイガンド"),
    "Progressive Bread": BFMItemData(IC.progression, 7, 0x80, "Bakery", jp_name = "あたらしいパン"),
    "Juice": BFMItemData(IC.filler, 1, 0x71, "Restaurant", jp_name = "ジュース"),
    "Pea Soup": BFMItemData(IC.filler, 1, 0x72, "Restaurant", jp_name = "ビアール"),
    "Cake": BFMItemData(IC.filler, 1, 0x73, "Restaurant", jp_name = "シャンペ イル"),
    "Gravy": BFMItemData(IC.filler, 1, 0x74, "Restaurant", jp_name = "しろドワイン"),
    "Salad": BFMItemData(IC.filler, 1, 0x75, "Restaurant", jp_name = "あかドワイン"),
    "Lasagna": BFMItemData(IC.filler, 1, 0x76, "Restaurant", jp_name = "ウイスキール"),
    "Pork Chop": BFMItemData(IC.filler, 1, 0x77, "Restaurant", jp_name = "ブランデーナ"),
    "Rice Ball": BFMItemData(IC.filler, 1, 0x01, "Grocery", jp_name = "ライスボール"),
    "Gel": BFMItemData(IC.filler, 1, 0x04, "Grocery", jp_name = "リカバージェル"),
    "W-Gel": BFMItemData(IC.progression, 1, 0x05, "Grocery", jp_name = "Wリカバージェル"),
    "Progressive Drink": BFMItemData(IC.progression, 2, 0x06, "Grocery", jp_name = "あたらしいリカバー"),
    #"EX-Drink": BFMItemData(IC.useful, 1, 0x07, "Grocery"),
    "Progressive Mint": BFMItemData(IC.useful, 2, 0x08, "Grocery", jp_name = "あたらしいミント"),
    "Antidote": BFMItemData(IC.useful, 1, 0x09, "Grocery", jp_name = "ポイズンレス"),
    "S-Revive": BFMItemData(IC.useful, 1, 0x0a, "Grocery", jp_name = "リバイバーS"),
    "Orange": BFMItemData(IC.progression, 1, 0x0b, "Grocery", jp_name = "おおきなミカン"),
    "Neatball": BFMItemData(IC.useful, 1, 0x6a, "Grocery", jp_name = "ワギュウおにぎり"),
    "Cheese": BFMItemData(IC.useful, 1, 0x6b, "Grocery", jp_name = "なっとうペースト"),
    #"H-Mint": BFMItemData(IC.useful, 1, 0x6d, "Grocery"),
    "Musashi Action Figure": BFMItemData(IC.filler, 1, 0x0 + item_action_figure_id, "Toy Shop", jp_name = "ムサシ"),
    "Bee Plant": BFMItemData(IC.filler, 1, 0x1 + item_action_figure_id, "Toy Shop", jp_name = "ビー・プラント"),
    "Soldier1": BFMItemData(IC.filler, 1, 0x2 + item_action_figure_id, "Toy Shop", jp_name = "ル・コアールヘい1"),
    "Soldier2": BFMItemData(IC.filler, 1, 0x3 + item_action_figure_id, "Toy Shop", jp_name = "ル・コアールヘい2"),
    "Rootrick": BFMItemData(IC.filler, 1, 0x4 + item_action_figure_id, "Toy Shop", jp_name = "ボルドーしょうい"),
    "Steam Knight": BFMItemData(IC.filler, 1, 0x5 + item_action_figure_id, "Toy Shop", jp_name = "スチーム・ナイト"),
    "Soldier3": BFMItemData(IC.filler, 1, 0x6 + item_action_figure_id, "Toy Shop", jp_name = "ル・コアールヘい3"),
    "Herb Plant": BFMItemData(IC.filler, 1, 0x7 + item_action_figure_id, "Toy Shop", jp_name = "ハーブ・プラント"),
    "King Man Eater": BFMItemData(IC.filler, 1, 0x8 + item_action_figure_id, "Toy Shop", jp_name = "キングマンイーター"),
    "Magician": BFMItemData(IC.filler, 1, 0x9 + item_action_figure_id, "Toy Shop", jp_name = "マジシャン"),
    "Sleepie": BFMItemData(IC.filler, 1, 0xa + item_action_figure_id, "Toy Shop", jp_name = "スリーピー"),
    "Skullpion": BFMItemData(IC.filler, 1, 0xb + item_action_figure_id, "Toy Shop", jp_name = "スカル゠ピオン"),
    "Relic Vambee": BFMItemData(IC.filler, 1, 0xc + item_action_figure_id, "Toy Shop", jp_name = "レリクスヴヌンビ"),
    "Vambee Soldier": BFMItemData(IC.filler, 1, 0xd + item_action_figure_id, "Toy Shop", jp_name = "ヴヌンビへい"),
    "Bowler": BFMItemData(IC.filler, 1, 0xe + item_action_figure_id, "Toy Shop", jp_name = "ボウラー"),
    "Cure Worm": BFMItemData(IC.filler, 1, 0xf + item_action_figure_id, "Toy Shop", jp_name = "キュアワーム"),
    "Bubbles": BFMItemData(IC.filler, 1, 0x10 + item_action_figure_id, "Toy Shop", jp_name = "リキュールちゃうい"),
    "Relic Keeper": BFMItemData(IC.filler, 1, 0x11 + item_action_figure_id, "Toy Shop", jp_name = "レリクスキーパー"),
    "Penguin": BFMItemData(IC.filler, 1, 0x12 + item_action_figure_id, "Toy Shop", jp_name = "フェイクペンギン"),
    "Haya Wolf": BFMItemData(IC.filler, 1, 0x13 + item_action_figure_id, "Toy Shop", jp_name = "カラテウルフ"),
    "Slow Guy": BFMItemData(IC.filler, 1, 0x14 + item_action_figure_id, "Toy Shop", jp_name = "スローガイ"),
    "Stomp Golem": BFMItemData(IC.filler, 1, 0x15 + item_action_figure_id, "Toy Shop", jp_name = "ストンプゴーレム"),
    "Gingerelle": BFMItemData(IC.filler, 1, 0x16 + item_action_figure_id, "Toy Shop", jp_name = "ブランディたいい"),
    "Frost Dragon": BFMItemData(IC.filler, 1, 0x17 + item_action_figure_id, "Toy Shop", jp_name = "フロストドラグーン"),
    "GiAnt": BFMItemData(IC.filler, 1, 0x18 + item_action_figure_id, "Toy Shop", jp_name = "ジャイアント"),
    "Toad Stool": BFMItemData(IC.filler, 1, 0x19 + item_action_figure_id, "Toy Shop", jp_name = "トードストゥール"),
    "Ed & Ben": BFMItemData(IC.filler, 1, 0x1a + item_action_figure_id, "Toy Shop", jp_name = "エドとベーン"),
    "Topo": BFMItemData(IC.filler, 1, 0x1b + item_action_figure_id, "Toy Shop", jp_name = "トポ"),
    "Colonel Capricola": BFMItemData(IC.filler, 1, 0x1c + item_action_figure_id, "Toy Shop", jp_name = "ウォッカたいき"),
    "Queen Ant": BFMItemData(IC.filler, 1, 0x1d + item_action_figure_id, "Toy Shop", jp_name = "アントヒルクィーン"),
    "Improved Fusion": BFMItemData(IC.useful, 1, 0x81, "Tech", jp_name = "しんらいこうまる"),
    "Dashing Pierce": BFMItemData(IC.useful, 1, 0x82, "Tech", jp_name = "ダッシュつき"),
    "Shish Kebab": BFMItemData(IC.useful, 1, 0x83, "Tech", jp_name = "くしざし"),
    "Crosswise Cut": BFMItemData(IC.progression, 1, 0x84, "Tech", jp_name = "じうもんじぎり"),
    "Tenderize": BFMItemData(IC.useful, 1, 0x85, "Tech", jp_name = "まきわりダイナマイト"),
    "Desperado Attack": BFMItemData(IC.useful, 1, 0x86, "Tech", jp_name = "デスペラードアタック"),
    "Rumparoni Special": BFMItemData(IC.useful, 1, 0x87, "Tech", jp_name = "タンシオーネ・クロスアタック"),
    "Earth Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x16 + scroll_base_id, "Scroll", jp_name = "チのまき"),
    "Water Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x17 + scroll_base_id, "Scroll", jp_name = "ミズのまき"),
    "Fire Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x18 + scroll_base_id, "Scroll", jp_name = "ヒのまき"),
    "Wind Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x19 + scroll_base_id, "Scroll", jp_name = "カゼのまき"),
    "Sky Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x1a + scroll_base_id, "Scroll", jp_name = "ソラのまき"),
    "Earth Boss Core": BFMItemData(IC.progression, 1, 0x8a + scroll_base_id, "Core", jp_name = "スカル゠ピオンのコア"),
    "Water Boss Core": BFMItemData(IC.progression, 1, 0x8b + scroll_base_id, "Core", jp_name = "レリクスキーパーのコア"),
    "Fire Boss Core": BFMItemData(IC.progression, 1, 0x8c + scroll_base_id, "Core", jp_name = "フロストドラグーンのコア"),
    "Wind Boss Core": BFMItemData(IC.progression, 1, 0x8d + scroll_base_id, "Core", jp_name = "アントヒルクィーンのコア"),
    "Body Stat Up": BFMItemData(IC.useful, 29, 0x1 + level_base_id, "Level", jp_name = "ちから アップ"),
    "Mind Stat Up": BFMItemData(IC.useful, 29, 0x2 + level_base_id, "Level", jp_name = "こころ アップ"),
    "Fusion Stat Up": BFMItemData(IC.useful, 29, 0x3 + level_base_id, "Level", jp_name = "らいこうまる アップ"),
    "Lumina Stat Up": BFMItemData(IC.useful, 29, 0x4 + level_base_id, "Level", jp_name = "レイガンド アップ"),
    "Ugly Belt": BFMItemData(IC.progression, 1, 0x1 + quest_base_id, "Quest", jp_name = "きたないべルト"),
    "Well H20": BFMItemData(IC.progression, 1, 0x2 + quest_base_id, "Quest", jp_name = "いど みず"),
    "Jon's Key": BFMItemData(IC.progression, 1, 0x3 + quest_base_id, "Quest", jp_name = "ジャンのカギ"),
    "Log": BFMItemData(IC.progression, 4, 0x4 + quest_base_id, "Quest", jp_name = "まるた"),
    "Manual": BFMItemData(IC.progression, 1, 0x5 + quest_base_id, "Quest", jp_name = "ウッドのメモ"),
    "Misteria": BFMItemData(IC.progression, 1, 0x6 + quest_base_id, "Quest", jp_name = "まばろしのはな"),
    "Aqualin": BFMItemData(IC.progression, 1, 0x7 + quest_base_id, "Quest", jp_name = "いやしのみず"),
    "Rope": BFMItemData(IC.progression, 1, 0x8 + quest_base_id, "Quest", jp_name = "かぎづめロープ"),
    "Key": BFMItemData(IC.progression, 1, 0x9 + quest_base_id, "Quest", jp_name = "はいこうのカギ"),
    "Angel Statue": BFMItemData(IC.progression, 1, 0xa + quest_base_id, "Quest", jp_name = "てんしのぞう"),
    "Handle #0": BFMItemData(IC.progression, 1, 0xb + quest_base_id, "Quest", jp_name = "0ばんハンドル"),
    "Handle #1": BFMItemData(IC.progression, 1, 0xc + quest_base_id, "Quest", jp_name = "1ばんハンドル"),
    "Handle #4": BFMItemData(IC.progression, 1, 0xd + quest_base_id, "Quest", jp_name = "4ばんハンドル"),
    "Handle #8": BFMItemData(IC.progression, 1, 0xe + quest_base_id, "Quest", jp_name = "8ばんハンドル"),
    "Calendar": BFMItemData(IC.filler, 1, 0xf + quest_base_id, "Quest", jp_name = "カレンダー"),
    "Rock Salt": BFMItemData(IC.progression, 1, 0x10 + quest_base_id, "Quest", jp_name = "あらじお"),
    "Gondola Gizmo?": BFMItemData(IC.filler, 3, 0x11 + quest_base_id, "Quest", jp_name = "ゴンドラパーツ?"),
    "Gondola Gizmo": BFMItemData(IC.progression, 1, 0x12 + quest_base_id, "Quest", jp_name = "ゴンドラパーツ"),
    "Profits": BFMItemData(IC.progression, 1, 0x13 + quest_base_id, "Quest", jp_name = "うりあげきん"),
    "Note": BFMItemData(IC.filler, 1, 0x14 + quest_base_id, "Quest", jp_name = "ジャンのメモ"),
}

# items we'll want the location of in slot data, for generating in-game hints
slot_data_item_names = [
    "Guard",
    "Seer",
    "Hawker",
    "MusicianB",
    "SoldierA",
    "Acrobat",
]

item_name_to_id: Dict[str, int] = {name: item_base_id * (data.item_group == "NPC") + data.item_id_offset for name, data in item_table.items()}
jp_item_name_to_id: Dict[str, int] = {data.jp_name: item_base_id * (data.item_group == "NPC") + data.item_id_offset + jp_id_offset for name, data in item_table.items()}
item_name_to_id.update(jp_item_name_to_id)

item_id_to_name: Dict[int, str] = {(item_base_id * (data.item_group == "NPC") + data.item_id_offset): name for name, data in item_table.items()}
jp_item_id_to_name: Dict[int, str] = {(item_base_id * (data.item_group == "NPC") + data.item_id_offset + jp_id_offset): data.jp_name for name, data in item_table.items()}
item_id_to_name.update(jp_item_id_to_name)

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == IC.filler]

npc_ids: List[int] = [item_base_id + data.item_id_offset for name, data in item_table.items() if data.item_group == "NPC"]

def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}

for name, data in item_table.items():
    if(data.item_group != ""):
        item_name_groups[data.item_group] = item_name_groups[data.item_group].union([data.jp_name])

