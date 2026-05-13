"""
Download all themed SVG icon sets for the html2video skill.

Combines cultivation (修仙) and science/tech themed icons into a single script.

Usage:
  python scripts/download-icons.py                      # download all
  python scripts/download-icons.py --list                # list all icons
  python scripts/download-icons.py --category chemistry   # specific category
  python scripts/download-icons.py --test                 # download + generate test HTML
  python scripts/download-icons.py --force                # re-download existing
  python scripts/download-icons.py --html-only            # generate test HTML only
"""

import json
import argparse
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
ICON_BASE = PROJECT_ROOT / "assets" / "icons"
TEST_HTML = PROJECT_ROOT / "test-all-icons.html"

GI = "https://game-icons.net/icons/000000/transparent/1x1"


def gi(name, artist="lorc"):
    return f"{GI}/{artist}/{name}.svg"


# ── Cultivation icons ──────────────────────────────────────────────

CULTIVATION = {
    "weapon": {
        "label_cn": "武器",
        "icons": {
            "crossed-swords": {"url": gi("crossed-swords"), "label_cn": "双剑", "desc": "交叉双剑"},
            "sword-wound": {"url": gi("sword-wound"), "label_cn": "剑伤", "desc": "剑击伤痕"},
            "pointy-sword": {"url": gi("pointy-sword"), "label_cn": "尖剑", "desc": "尖头长剑"},
            "hook-swords": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M96 32L64 64l160 160-16 16L48 80 16 112l160 160-16 16L0 128v48l144 144 16-16 16-16 160-160 16-16L496 32h-48L304 176 288 160 432 16h-48L240 160l-16-16L368 0h-48L192 128 176 112 320 0h-48L144 128 128 112 272 0h-48z"/></svg>', "label_cn": "钩剑", "desc": "双钩"},
        },
    },
    "alchemy": {
        "label_cn": "炼丹",
        "icons": {
            "cauldron": {"url": gi("cauldron"), "label_cn": "丹炉", "desc": "炼丹炉"},
            "potion-ball": {"url": gi("potion-ball"), "label_cn": "丹药", "desc": "圆球形丹药"},
            "drink-me": {"url": gi("drink-me"), "label_cn": "灵液", "desc": "药瓶"},
            "bubbling-flask": {"url": gi("bubbling-flask"), "label_cn": "灵瓶", "desc": "冒泡药瓶"},
            "round-bottom-flask": {"url": gi("round-bottom-flask"), "label_cn": "炼药瓶", "desc": "圆底烧瓶"},
        },
    },
    "nature": {
        "label_cn": "自然",
        "icons": {
            "lotus-flower": {"url": gi("lotus-flower"), "label_cn": "莲花", "desc": "莲花"},
            "lotus": {"url": gi("lotus"), "label_cn": "莲", "desc": "冥想莲"},
            "mushroom": {"url": gi("mushroom"), "label_cn": "灵芝", "desc": "灵芝"},
            "sun": {"url": gi("sun"), "label_cn": "太阳", "desc": "太阳/阳"},
            "crescent-moon": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M320 32C192 64 96 160 96 288c0 112 80 192 192 192 32 0 64-8 88-24-112-16-192-112-192-216S224 48 320 32z"/></svg>', "label_cn": "弯月", "desc": "新月/阴"},
            "mountains": {"url": gi("mountains"), "label_cn": "群山", "desc": "连绵山脉"},
        },
    },
    "beast": {
        "label_cn": "灵兽",
        "icons": {
            "dragon-head": {"url": gi("dragon-head"), "label_cn": "龙头", "desc": "龙族"},
            "dragon-breath": {"url": gi("dragon-breath"), "label_cn": "龙息", "desc": "龙焰"},
            "phoenix-flaming": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 32c-24 48-64 80-64 144 0 48 32 80 64 96 32-16 64-48 64-96 0-64-40-96-64-144zM128 192c-16 32-48 56-48 112 0 64 48 112 96 128 16-64 48-96 48-160 0-32-16-48-32-64-24 16-40 48-40 80h-24c0-40 16-72 32-96h-32zm256 0h-32c16 24 32 56 32 96h-24c0-32-16-64-40-80-16 16-32 32-32 64 0 64 32 96 48 160 48-16 96-64 96-128 0-56-32-80-48-112zM192 448c20 16 40 32 64 32s44-16 64-32c-20-8-40-16-64-16s-44 8-64 16z"/></svg>', "label_cn": "凤凰", "desc": "浴火凤凰"},
            "snake": {"url": gi("snake"), "label_cn": "蛇", "desc": "蛟龙前身"},
            "tortoise": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M96 288c-32 0-64 16-64 48h48c0-16 16-16 16 0H96v16h320v-16c0-16 16-16 16 0h48c0-32-32-48-64-48H96zm-48 64v32h416v-32H48zm32 32v32h32v-32H80zm288 0v32h32v-32h-32zm-224 32v32h192v-32H144zM256 128c-80 0-144 64-144 144h288c0-80-64-144-144-144zm0 48c24 0 48 24 48 48h-96c0-24 24-48 48-48z"/></svg>', "label_cn": "玄武", "desc": "龟/玄武"},
        },
    },
    "element": {
        "label_cn": "五行",
        "icons": {
            "fire": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 32c-40 80-120 120-120 220 0 80 60 160 120 180 60-20 120-100 120-180 0-100-80-140-120-220zm0 80c24 56 60 90 60 150 0 40-30 80-60 90-30-10-60-50-60-90 0-60 36-94 60-150z"/></svg>', "label_cn": "火", "desc": "火焰"},
            "water-drop": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 32C192 128 96 200 96 320c0 88 72 160 160 160s160-72 160-160C416 200 320 128 256 32zm0 96c48 72 96 120 96 192 0 52-44 96-96 96s-96-44-96-96c0-72 48-120 96-192z"/></svg>', "label_cn": "水", "desc": "水滴"},
            "lightning-frequency": {"url": gi("lightning-frequency"), "label_cn": "雷", "desc": "雷电/天劫"},
            "thunderball": {"url": gi("thunderball"), "label_cn": "雷球", "desc": "雷劫"},
            "windmill": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M32 128h280c20 0 40-16 40-36s-16-36-36-36-40 16-40 36h-48c0-48 40-84 88-84s88 36 88 84-40 84-88 84H32v-48zm0 128h320c48 0 88-36 88-84h-48c0 20-16 36-40 36H32v48z"/></svg>', "label_cn": "风", "desc": "风元素"},
        },
    },
    "spiritual": {
        "label_cn": "修为",
        "icons": {
            "meditation": {"url": gi("meditation"), "label_cn": "打坐", "desc": "冥想修炼"},
            "aura": {"url": gi("aura"), "label_cn": "灵气", "desc": "灵气外放"},
            "telepathy": {"url": gi("telepathy"), "label_cn": "神识", "desc": "神识传音"},
            "portal": {"url": gi("portal"), "label_cn": "传送门", "desc": "秘境入口"},
            "energy-shield": {"url": gi("energy-shield"), "label_cn": "护体真气", "desc": "能量护盾"},
            "yin-yang": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 32C132 32 32 132 32 256s100 224 224 224 224-100 224-224S380 32 256 32zm0 384c-24 0-48-20-48-48s20-48 48-48 48-20 48-48-20-48-48-48 20-48 48-48 48 20 48 48-20 48-48 48-48 20-48 48 20 48 48 48-20 48-48c0 88-72 144-144 144z"/></svg>', "label_cn": "阴阳", "desc": "阴阳太极"},
        },
    },
    "treasure": {
        "label_cn": "宝物",
        "icons": {
            "crystal-cluster": {"url": gi("crystal-cluster"), "label_cn": "灵石", "desc": "灵石矿"},
            "crystal-bars": {"url": gi("crystal-bars"), "label_cn": "灵晶", "desc": "灵晶"},
            "diamond-hard": {"url": gi("diamond-hard"), "label_cn": "钻石", "desc": "坚硬法器"},
            "gem-chain": {"url": gi("gem-chain"), "label_cn": "灵珠", "desc": "灵珠链"},
            "scroll-unfurled": {"url": gi("scroll-unfurled"), "label_cn": "功法卷轴", "desc": "功法"},
            "tied-scroll": {"url": gi("tied-scroll"), "label_cn": "密封卷轴", "desc": "封印秘籍"},
            "star-prominences": {"url": gi("star-prominences"), "label_cn": "星辰", "desc": "星辰之力"},
            "beams-aurora": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M32 128l112 80-112 80v48l176-128L32 80v48zm224 0l112 80-112 80v48l176-128L256 80v48zm224 0v48l-48 32 48 32v48l-112-80 112-80z"/></svg>', "label_cn": "极光", "desc": "天象异变"},
        },
    },
    "body": {
        "label_cn": "肉身",
        "icons": {
            "bleeding-eye": {"url": gi("bleeding-eye"), "label_cn": "天眼", "desc": "天眼"},
            "half-heart": {"url": gi("half-heart"), "label_cn": "道心", "desc": "道心"},
            "chained-heart": {"url": gi("chained-heart"), "label_cn": "锁心", "desc": "心魔"},
            "shield-echoes": {"url": gi("shield-echoes"), "label_cn": "护盾", "desc": "回声护盾"},
        },
    },
}

# ── Science/Tech themed icons ──────────────────────────────────────

THEMED = {
    "chemistry": {
        "label_cn": "化学",
        "icons": {
            "chemical-drop": {"url": gi("chemical-drop"), "label_cn": "化学液滴", "desc": "化学液滴"},
            "chemical-arrow": {"url": gi("chemical-arrow"), "label_cn": "反应箭头", "desc": "反应箭头"},
            "acid": {"url": gi("acid"), "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 32l-96 192c-32 64-48 96-48 144 0 80 64 112 144 112s144-32 144-112c0-48-16-80-48-144L256 32zm0 128l64 128c16 32 32 64 32 96 0 48-48 64-96 64s-96-16-96-64c0-32 16-64 32-96l64-128z"/></svg>', "label_cn": "酸液", "desc": "酸"},
            "flask": {"url": gi("round-bottom-flask"), "label_cn": "烧瓶", "desc": "烧瓶"},
            "bubbling-flask": {"url": gi("bubbling-flask"), "label_cn": "冒泡烧瓶", "desc": "冒泡烧瓶"},
            "test-tubes": {"url": gi("test-tubes"), "label_cn": "试管", "desc": "试管"},
            "beaker": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M160 32v192l-80 160c-16 32 0 64 32 64h288c32 0 48-32 32-64l-80-160V32h32V0H128v32h32zm32 0h96v192l80 160H112l80-160V32z"/></svg>', "label_cn": "烧杯", "desc": "烧杯"},
            "molecule": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M128 64a64 64 0 1 0 0 128 64 64 0 0 0 0-128zm256 0a64 64 0 1 0 0 128 64 64 0 0 0 0-128zM192 320a64 64 0 1 0 128 0 64 64 0 0 0-128 0z"/></svg>', "label_cn": "分子", "desc": "分子结构"},
        },
    },
    "biology": {
        "label_cn": "生物",
        "icons": {
            "dna": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M160 0c-32 64-96 128-96 192s48 96 96 128 96 64 96 128-48 32-48 64h32c0-32 48-64 48-128s-48-96-96-128S96 256 96 192 160 64 192 0h-32zm128 0c32 64 96 128 96 192s-48 96-96 128-96 64-96 128 48 32 48 64h-32c0-32-48-64-48-128s48-96 96-128 96-64 96-128S352 64 320 0h-32z"/></svg>', "label_cn": "DNA", "desc": "DNA双螺旋"},
            "cell": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><circle fill="none" stroke="#000" stroke-width="32" cx="256" cy="256" r="224"/><circle fill="#000" cx="220" cy="200" r="48"/></svg>', "label_cn": "细胞", "desc": "细胞"},
            "microscope": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M224 32v32h-32v192c0 64 32 96 64 128h-64v32h192v-32h-64c32-32 64-64 64-128h-32c0 48-32 80-64 96V64h-32V32h-32zm-96 384v32h224v-32H128zm-32 32v32h288v-32H96z"/></svg>', "label_cn": "显微镜", "desc": "显微镜"},
            "flower": {"url": gi("daisy"), "label_cn": "花", "desc": "花朵"},
            "heartbeat": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M0 256h80l40-96 56 224 48-192 40 128 40-64h56l40 64h72v32H344l-24-40-48 80-40-128-48 192-56-224-24 56H0z"/></svg>', "label_cn": "心跳", "desc": "心电图"},
        },
    },
    "hardware": {
        "label_cn": "硬件",
        "icons": {
            "cpu-shot": {"url": gi("cpu-shot"), "label_cn": "CPU", "desc": "处理器"},
            "processor": {"url": gi("processor"), "label_cn": "处理器", "desc": "芯片"},
            "motherboard": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 64h384v384H64V64zm32 32v320h320V96H96zm32 32h64v64h-64v-64zm0 96h128v32H128v-32zm192-96h64v64h-64v-64zm-64 128h128v96H224v-96z"/></svg>', "label_cn": "主板", "desc": "主板"},
            "ram-rows": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 192h384v128H64V192zm32 32v64h64v-64H96zm96 0v64h64v-64h-64zm96 0v64h64v-64h-64zm96 0v64h64v-64h-64z"/></svg>', "label_cn": "内存", "desc": "内存条"},
            "hard-drive": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 256h384v32H64v-32zm0 64h384v128H64V320zm32 32v64h64v-64H96zm256 0a32 32 0 1 1 0 64 32 32 0 0 1 0-64z"/></svg>', "label_cn": "硬盘", "desc": "硬盘"},
            "desktop": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M32 64h448v288H32V64zm32 32v224h384V96H64zM192 384h128v64H192v-64zm-64 64h256v32H128v-32z"/></svg>', "label_cn": "台式机", "desc": "台式电脑"},
            "laptop": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 96h384v256H64V96zm32 32v192h320V128H96zM0 384h512v32H0v-32z"/></svg>', "label_cn": "笔记本", "desc": "笔记本"},
            "router": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 320v64h384v-64H64zm0 96v64h384v-64H64zm160-224V96h64v96h160v64H64v-64h160z"/></svg>', "label_cn": "路由器", "desc": "路由器"},
            "server-rack": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M96 32h320v96H96zm0 128h320v96H96zm0 128h320v96H96zm32-224v32h256v-32H128zm0 128v32h256v-32H128zm0 128v32h256v-32H128z"/></svg>', "label_cn": "服务器", "desc": "机架服务器"},
        },
    },
    "energy": {
        "label_cn": "能源",
        "icons": {
            "nuclear-plant": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M240 32c-80 160-160 240-160 320 0 88 72 128 160 128s160-40 160-128c0-80-80-160-160-320zm0 128c48 96 96 144 96 224 0 48-48 64-96 64s-96-16-96-64c0-80 48-128 96-224z"/></svg>', "label_cn": "核能", "desc": "核能"},
            "solar-power": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M128 64h256v192H128V64zm32 32v128h192V96H160zM64 288h384v32H64v-32zm32 64h320v96H96v-96z"/></svg>', "label_cn": "太阳能", "desc": "太阳能"},
            "battery-pack": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 128h320v288H64zm384 64h32v160h-32zM96 160v224h256V160H96z"/></svg>', "label_cn": "电池", "desc": "电池"},
            "electric": {"url": gi("lightning-frequency"), "label_cn": "电力", "desc": "电力"},
            "wind-turbine": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M240 0v224c-16 4-32 16-40 32L48 96 32 112l160 160c-4 16-4 32 0 48L0 400l16 16 160-112c8 16 24 28 40 32V512h32v-176c16-4 32-16 40-32l160 112 16-16-192-80c4-16 4-32 0-48l160-160-16-16-152 160c-8-16-24-28-40-32V0h-32z"/></svg>', "label_cn": "风力", "desc": "风力发电"},
            "oil-rig": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M192 32v64h-64v32h64v64h-32v32h32v288h32V224h32v-32h-32v-64h64v-32h-64V32h-64z"/></svg>', "label_cn": "石油", "desc": "石油"},
        },
    },
    "finance": {
        "label_cn": "金融",
        "icons": {
            "chart-up": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 416V96h32v288h352v32H64zm96-64l80-96 64 64 128-160v64L304 320l-64-64-80 96z"/></svg>', "label_cn": "上涨", "desc": "上涨"},
            "chart-down": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 416V96h32v288h352v32H64zm96-96l80 96 64-64 128 160v-64L304 192l-64 64-80-96z"/></svg>', "label_cn": "下跌", "desc": "下跌"},
            "coins": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><circle fill="none" stroke="#000" stroke-width="32" cx="192" cy="192" r="160"/><circle fill="none" stroke="#000" stroke-width="24" cx="320" cy="320" r="160"/></svg>', "label_cn": "金币", "desc": "金币"},
            "bank": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 32L32 160h448L256 32zM64 192v192H32v32h448v-32h-32V192h-32v192h-96V192h-32v192h-96V192h-32v192H96V192H64z"/></svg>', "label_cn": "银行", "desc": "银行"},
            "candlestick": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M96 64v384h32V64H96zm32 96h64v128h-64zm64-32h32v192h-32V128zm64 64h64v128h-64zm64 32h32v64h-32zm64-96h32v256h-32V96z"/></svg>', "label_cn": "K线图", "desc": "K线"},
            "exchange": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M32 128l64-64 64 64h-48v128H80V128H32zm384 256l-64 64-64-64h48V256h32v128h48z"/></svg>', "label_cn": "汇率", "desc": "汇率"},
        },
    },
    "weather": {
        "label_cn": "气象",
        "icons": {
            "typhoon": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M256 64C150 64 64 150 64 256s86 192 192 192 192-86 192-192S362 64 256 64zm0 64c24 0 48 8 64 24-32-8-64 0-88 16-24 16-40 48-40 80 0 48 32 80 64 80s64-32 64-80c16 16 24 40 24 64 0 56-40 104-88 104s-88-48-88-104 40-104 88-104z"/></svg>', "label_cn": "台风", "desc": "台风"},
            "earthquake": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M32 320h96l32-64 48 128 64-192 48 128h48l32-64 32 64h48v32h-64l-16-32-16 32h-48l-32-96-64 192-48-128-32 64H32z"/></svg>', "label_cn": "地震", "desc": "地震"},
            "satellite": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M352 32l-64 64 128 128 64-64L352 32zM96 224L32 288l48 48-48 48 32 32 48-48 48 48 64-64-128-128z"/></svg>', "label_cn": "卫星", "desc": "卫星"},
            "thermometer": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M192 32v288c-32 24-48 64-48 96 0 64 48 96 112 96s112-32 112-96c0-32-16-72-48-96V32H192zm32 32h64v272l16 16c16 16 32 40 32 64 0 40-32 64-80 64s-80-24-80-64c0-24 16-48 32-64l16-16V64z"/></svg>', "label_cn": "温度计", "desc": "温度"},
            "rain": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M128 256c-64 0-96-48-96-96 0-64 48-96 96-96 16-32 64-64 128-64s112 32 128 64c64 0 96 48 96 96s-32 96-96 96H128zm16 48l-32 96h32l32-96h-32zm80 0l-32 128h32l32-128h-32zm80 0l-32 96h32l32-96h-32z"/></svg>', "label_cn": "降雨", "desc": "降雨"},
            "snowflake": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M240 0v80l-48-32-16 32 64 48v112l-96-56-16-80-32 8 16 48-64-32v32l64 32-48 16 8 32 80-16 96 56-96 56-80-16-8 32 48 16-64 32v32l64-32-16 48 32 8 16-80 96-56v112l-64 48 16 32 48-32V512h32v-80l48 32 16-32-64-48V272l96 56 16 80 32-8-16-48 64 32v-32l-64-32 48-16-8-32-80 16-96-56 96-56 80 16 8-32-48-16 64-32v-32l-64 32 16-48-32-8-16 80-96 56V128l64-48-16-32-48 32V0h-32z"/></svg>', "label_cn": "降雪", "desc": "降雪"},
            "tornado": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M64 64h384v32H64V64zm32 64h320v32H96v-32zm64 64h256v32H160v-32zm-32 64h224v32H128v-32zm96 64h160v32H224v-32zm32 64h96v32h-96v-32zm-16 64h64v32h-64v-32z"/></svg>', "label_cn": "龙卷风", "desc": "龙卷风"},
        },
    },
    "industry": {
        "label_cn": "工业",
        "icons": {
            "gears": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M224 32l-16 48c-16 4-32 12-44 24l-48-16-32 56 36 32c-4 16-4 32 0 48l-36 32 32 56 48-16c12 12 28 20 44 24l16 48h64l16-48c16-4 32-12 44-24l48 16 32-56-36-32c4-16 4-32 0-48l36-32-32-56-48 16c-12-12-28-20-44-24L288 32h-64zm32 128a64 64 0 1 1 0 128 64 64 0 0 1 0-128z"/></svg>', "label_cn": "齿轮组", "desc": "工业齿轮"},
            "factory": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M32 192v288h448V192h-64v64h-64v-64h-64v64h-64v-64h-64v64H96v-64H32z"/></svg>', "label_cn": "工厂", "desc": "工厂"},
            "wrench": {"url": gi("spanner"), "label_cn": "扳手", "desc": "扳手"},
            "assembly": {"url": gi("gears"), "label_cn": "装配", "desc": "装配"},
            "mining": {"url": "", "fallback_svg": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512"><path fill="#000" d="M224 32L96 256h256L224 32zm48 256v192h-32V288h-32v192h-32V288H96v32h48v160h192V320h48v-32H272z"/></svg>', "label_cn": "采矿", "desc": "采矿"},
        },
    },
}

ALL_CATALOGS = {**{k: v for k, v in CULTIVATION.items()}, **THEMED}


def download_svg(url, dest, timeout=20, fallback_svg=None):
    if fallback_svg and not url:
        dest.write_text(fallback_svg, encoding="utf-8")
        return True, f"{len(fallback_svg)}b"
    if not url:
        if fallback_svg:
            dest.write_text(fallback_svg, encoding="utf-8")
            return True, f"{len(fallback_svg)}b"
        return False, "no url"
    try:
        req = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urlopen(req, timeout=timeout) as r:
            data = r.read()
            if len(data) < 50:
                if fallback_svg:
                    dest.write_text(fallback_svg, encoding="utf-8")
                    return True, f"{len(fallback_svg)}b"
                return False, "too small"
            dest.write_bytes(data)
            return True, f"{len(data)}b"
    except Exception:
        if fallback_svg:
            dest.write_text(fallback_svg, encoding="utf-8")
            return True, f"{len(fallback_svg)}b"
        return False, "error"


def download_all(categories=None, force=False):
    ICON_BASE.mkdir(parents=True, exist_ok=True)
    ok = fail = skip = 0
    for cat_key, cat_data in ALL_CATALOGS.items():
        if categories and cat_key not in categories:
            continue
        cat_dir = ICON_BASE / cat_key
        cat_dir.mkdir(parents=True, exist_ok=True)
        for icon_key, meta in cat_data["icons"].items():
            dest = cat_dir / f"{icon_key}.svg"
            if dest.exists() and not force:
                ok += 1; skip += 1
                print(f"  SKIP: {cat_key}/{icon_key}")
                continue
            ok_f, msg = download_svg(meta.get("url", ""), dest, fallback_svg=meta.get("fallback_svg"))
            if ok_f:
                ok += 1
                print(f"  OK: {cat_key}/{icon_key} ({msg})")
            else:
                fail += 1
                print(f"  FAIL: {cat_key}/{icon_key} ({msg})")
    print(f"\nDone: {ok} ok ({skip} skipped), {fail} failed")


def list_icons():
    print(f"{'Category':<12} {'Icon':<22} {'Chinese':<8} {'Source':<14} Description")
    print("-" * 85)
    for cat_key, cat_data in ALL_CATALOGS.items():
        for icon_key, meta in cat_data["icons"].items():
            src = "game-icons" if meta.get("url") and "game-icons" in meta.get("url", "") else "hand-crafted"
            print(f"{cat_key:<12} {icon_key:<22} {meta['label_cn']:<8} {src:<14} {meta['desc']}")
    total = sum(len(c["icons"]) for c in ALL_CATALOGS.values())
    print(f"\nTotal: {total} icons in {len(ALL_CATALOGS)} categories")


def generate_test_html():
    rows = []
    for cat_key, cat_data in ALL_CATALOGS.items():
        cells = []
        for icon_key, meta in cat_data["icons"].items():
            p = f"assets/icons/{cat_key}/{icon_key}.svg"
            cells.append(
                f'<div class="c"><img src="{p}" alt="{meta["label_cn"]}" style="width:56px;height:56px;filter:invert(1)">'
                f'<div class="l">{meta["label_cn"]}</div></div>'
            )
        rows.append(f'<div class="cat"><h2>{cat_data["label_cn"]} ({cat_key})</h2><div class="g">{"".join(cells)}</div></div>')
    total = sum(len(c["icons"]) for c in ALL_CATALOGS.values())
    html = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><title>All Icons</title><style>
body{{background:#0a0a12;color:#e0e0e0;font-family:system-ui;padding:40px;margin:0}}
h1{{text-align:center;font-size:36px}}h2{{font-size:20px;color:#a78bfa;border-bottom:1px solid #333;padding-bottom:8px}}
.cat{{margin-bottom:40px}}.g{{display:flex;flex-wrap:wrap;gap:12px}}
.c{{width:80px;display:flex;flex-direction:column;align-items:center;gap:6px;padding:12px 4px;
background:rgba(255,255,255,0.03);border-radius:12px;transition:transform .2s;cursor:pointer}}
.c:hover{{transform:scale(1.15);background:rgba(167,139,250,0.1)}}
.l{{font-size:11px;color:#888;text-align:center}}
.info{{margin-top:32px;padding:16px;background:#111;border-radius:8px;font-size:14px;color:#666}}
</style></head><body><h1>Icon Library Test ({total} icons)</h1>{"".join(rows)}
<div class="info">Sources: game-icons.net (CC BY 3.0) + hand-crafted (CC0)</div></body></html>"""
    with open(TEST_HTML, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Test HTML: {TEST_HTML}")


def main():
    p = argparse.ArgumentParser(description="Download all SVG icons")
    p.add_argument("--list", action="store_true")
    p.add_argument("--category", type=str)
    p.add_argument("--test", action="store_true")
    p.add_argument("--force", action="store_true")
    p.add_argument("--html-only", action="store_true")
    a = p.parse_args()
    if a.list:
        list_icons(); return
    cats = [a.category] if a.category else None
    if a.html_only:
        generate_test_html(); return
    print("Downloading icons...")
    if cats:
        print(f"  Filter: {cats}")
    download_all(categories=cats, force=a.force)
    if a.test:
        generate_test_html()


if __name__ == "__main__":
    main()
