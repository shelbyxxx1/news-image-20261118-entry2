"""Typeset and draw the 18 November front page with Pillow."""

from functools import cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


SCALE = 2
LEFT, RIGHT = 36, 988
WIDTH = RIGHT - LEFT
PAPER, INK, RED = '#f6f1e5', '#16181d', '#a71e22'
BLUE, GOLD, GREY = '#1d3a5f', '#b98a1c', '#5a5e66'
RULE = '#b1a798'
FONT_DIR = Path('/usr/share/fonts/truetype/noto')
FACES = {
    'mast': 'NotoSerifDisplay-Black', 'display': 'NotoSerifDisplay-Bold',
    'serif-bold': 'NotoSerif-Bold', 'serif': 'NotoSerif-Regular',
    'sans': 'NotoSans-Condensed', 'bold': 'NotoSans-CondensedBold',
    'semi': 'NotoSans-CondensedSemiBold',
}


@cache
def font(face, size):
    return ImageFont.truetype(FONT_DIR / (FACES[face] + '.ttf'), round(size * SCALE))


def scaled(values):
    return tuple(round(value * SCALE) for value in values)


class Page:
    def __init__(self):
        self.image = Image.new('RGB', (1024 * SCALE, 1024 * SCALE), PAPER)
        self.draw = ImageDraw.Draw(self.image)

    def rect(self, box, fill=None, outline=None):
        self.draw.rectangle(scaled(box), fill=fill, outline=outline, width=SCALE)

    def line(self, points, color=RULE, width=1):
        self.draw.line([scaled(point) for point in points], fill=color, width=round(width * SCALE))

    def rule(self, y, x1=LEFT, x2=RIGHT, color=RULE, width=1):
        self.line(((x1, y), (x2, y)), color, width)

    def polygon(self, points, fill):
        self.draw.polygon([scaled(point) for point in points], fill=fill)

    def dot(self, x, y, radius, fill):
        self.draw.ellipse(scaled((x-radius, y-radius, x+radius, y+radius)), fill=fill)

    def text(self, x, baseline, content, face, size, color=INK, align='l', *, box=None):
        style = font(face, size)
        point = scaled((x, baseline))
        anchor = align + 's'
        bounds = self.draw.textbbox(point, content, font=style, anchor=anchor)
        box = box or (LEFT, 36, RIGHT, 988)
        limits = scaled(box)
        if any(bounds[index] < limits[index] for index in (0, 1)) or any(
            bounds[index] > limits[index] for index in (2, 3)
        ):
            raise ValueError(f'{content!r} exceeds {box}: {tuple(v / SCALE for v in bounds)}')
        self.draw.text(point, content, font=style, fill=color, anchor=anchor)

    def lines(self, x, baseline, lines, step, face, size, box):
        for index, line in enumerate(lines):
            self.text(x, baseline + step * index, line, face, size, box=box)


def masthead(page):
    page.rule(36, color=INK)
    page.text(LEFT, 56, 'LATE EDITION · ALL THE NEWS OF ONE DAY ON ONE PAGE', 'semi', 15)
    page.text(RIGHT, 56, 'No. 2026-322', 'semi', 15, align='r')
    page.rule(63)
    page.text(512, 122, 'THE WORLD IN ONE DAY', 'mast', 73, align='m', box=(LEFT, 64, RIGHT, 131))
    page.rect((LEFT, 133, RIGHT, 173), RED)
    page.text(512, 160, 'WEDNESDAY, 18 NOVEMBER 2026 — 35 STORIES · SIX CONTINENTS · ONE PAGE',
              'bold', 18, PAPER, 'm', box=(LEFT, 133, RIGHT, 173))


def leaders(page):
    page.line(((648, 184), (648, 513)))
    page.text(LEFT, 195, 'STRAIT OF HORMUZ — GULF WAR WIDENS', 'bold', 16, RED)
    page.lines(LEFT, 238, ("U.S. jets hit Iran missile site;", "Tehran’s drones strike",
                           "back at Bahrain and Kuwait"),
               40, 'display', 42, (LEFT, 201, 633, 327))
    page.lines(LEFT, 342, (
        'U.S. fighters hit a Revolutionary Guard missile site on Qeshm Island',
        'after Iranian drones struck a U.S. radar site in Bahrain. Iran then hit',
        'Kuwait’s Ali Al Salem air base and downed a U.S. MQ-9 near the strait.',
    ), 18, 'serif', 16.5, (LEFT, 328, 633, 384))
    page.text(664, 195, 'SHENZHEN — APEC SUMMIT', 'bold', 16, RED)
    page.lines(664, 225, ('Xi and Putin meet', 'as Trump heads for', 'three-way talks'),
               30, 'serif-bold', 28, (664, 200, RIGHT, 295))
    page.lines(664, 310, (
        'China’s Xi Jinping vowed to resist trade',
        'protectionism and Russia’s Vladimir Putin',
        'attacked Western sanctions as they opened',
        'APEC. Donald Trump is in Manila with',
        'President Marcos Jr. and Quad partners',
        'before flying to Shenzhen.',
    ), 18, 'serif', 15, (664, 295, RIGHT, 409))
    page.rect((664, 416, RIGHT, 513), outline=RULE)
    page.text(677, 436, 'TOMORROW', 'bold', 15, RED)
    page.rule(443, 677, 975)
    page.lines(677, 460, ('Trump–Xi–Putin trilateral in Shenzhen',
                          'Cyclone Akvan landfall due Friday',
                          'Nvidia rally faces its first full session'),
               18, 'semi', 15, (677, 445, 975, 510))


def strait(page):
    page.rect((LEFT, 387, 632, 513), BLUE)
    coast = '#46627e'
    page.polygon(((36, 387), (632, 387), (632, 406), (597, 414), (567, 412),
                  (536, 422), (509, 421), (482, 431), (456, 426), (433, 416),
                  (405, 420), (373, 415), (341, 419), (316, 411), (290, 414),
                  (256, 408), (224, 411), (194, 406), (151, 406), (112, 398),
                  (87, 405), (66, 424), (36, 428)), coast)
    page.polygon(((36, 436), (66, 428), (86, 438), (104, 454), (129, 459),
                  (153, 471), (186, 475), (217, 488), (240, 485), (244, 472),
                  (253, 468), (261, 478), (262, 491), (296, 494), (330, 486),
                  (357, 478), (393, 478), (412, 466), (432, 456), (449, 444),
                  (456, 448), (453, 463), (474, 476), (500, 482), (539, 489),
                  (563, 506), (632, 512), (632, 513), (36, 513)), coast)
    page.polygon(((399, 432), (421, 426), (437, 430), (430, 437), (407, 440)), coast)
    lane = ((118, 427), (169, 437), (244, 451), (322, 456), (380, 455),
            (432, 444), (477, 440), (529, 449), (597, 466))
    for start, end in zip(lane, lane[1:]):
        for index in range(4):
            dash = tuple(tuple(a + (b - a) * part / 8 for a, b in zip(start, end))
                         for part in (2 * index, 2 * index + 1))
            page.line(dash, '#dec282')
    for x, y, label, label_x, baseline in (
        (75, 437, 'KUWAIT', 89, 440), (222, 477, 'BAHRAIN', 166, 502),
        (419, 433, 'QESHM', 389, 413),
    ):
        page.dot(x, y, 4.5, PAPER)
        page.dot(x, y, 3.3, RED)
        page.text(label_x, baseline, label, 'bold', 12, PAPER, box=(36, 387, 632, 513))
    page.text(617, 503, 'THE STRAIT OF HORMUZ', 'semi', 13, PAPER, 'r')


WORLD = '''
...................#####....########..######..####........#########...#######..#############
.......###########.##########.####..########..#####..###.######################.###############
...####################.####.####..########...###...###..######################################
......#######################......#######.........######.###################################
.......###################..###.....####...........####.##################################
...####..###################..####...............#####.####################################
...........####################.................#########################################..##
............####################...............#########################################.##
.............################..#..............####.####.##############################..##
..............############..###...............###.#########..#######################...##
..............#########.###....................##########..######.##################...#
................########..###.................#############.#####....#############..##
.................########....................###############..##......####..######..#
...................######..##................################..........##....####...##
......................####...####............#############..............#.....###...#
.........................###.#######...........###########.....................###...##...###
............................##########...........########.......................####.##..#####
.............................###########..........######..........................######.##
..............................##########..........######.##...........................##..###
..............................#########............####..#..........................####..####
..............................########.............###............................#############
..............................#######.............................................#############..#
..............................#####...............................................#####..#####..##
.............................#####.........................................................##..##
.............................####.............................................................##
.............................###
..............................###.#
'''

LOCATIONS = (
    ('KERCH BRIDGE', .600, .250, 0, 0), ('HORMUZ', .655, .350, 0, 0),
    ('SHENZHEN', .817, .375, -8, -8), ('ALASKA', .083, .144, 0, 0),
    ('DR CONGO', .564, .511, 0, 0), ('COOK ISLANDS', .056, .556, 0, 0),
    ('KEMEROVO', .739, .194, 0, 0), ('PAPUA', .900, .533, 0, 0),
    ('GAZA', .595, .325, -14, 10), ('MANILA', .836, .419, 7, 9),
)


def world_map(page):
    page.rule(520, color=INK)
    page.text(LEFT, 535, 'NEWS ATLAS', 'bold', 15, RED)
    for row, marks in enumerate(WORLD.strip().splitlines()):
        for column, mark in enumerate(marks):
            if mark == '#':
                page.dot(LEFT + 12 + column * 9.55, 530 + row * 4.25, 1.25, '#7b8995')
    for number, (_, fx, fy, dx, dy) in enumerate(LOCATIONS, 1):
        x, y = LEFT + WIDTH * fx, 529 + 116 * fy
        if dx or dy:
            page.line(((x, y), (x + dx, y + dy)), RED)
            page.dot(x, y, 1.7, RED)
        x, y = x + dx, y + dy
        page.dot(x, y, 9.3, PAPER)
        page.dot(x, y, 8.1, RED)
        page.text(x, y + 3.8, str(number), 'bold', 11, PAPER, 'm')
    key = ' · '.join(f'{number} {place}' for number, (place, *_) in enumerate(LOCATIONS, 1))
    page.text(512, 663, key, 'semi', 13.5, BLUE, 'm', box=(LEFT, 649, RIGHT, 667))


def markets(page):
    tiles = (
        (124, 'S&P 500', '7,340.53', '-1.03%', '#ffa8a0'),
        (124, 'NASDAQ', '24,328.38', '-0.74%', '#ffa8a0'),
        (112, 'DOW', '-848.75 PTS', '', '#ffa8a0'),
        (124, 'NIKKEI', '59,024', '+0.28%', '#a8d8a5'),
        (94, 'BRENT', '$91.55', '', PAPER),
        (118, 'GOLD', '$3,775', '-2.3%', '#ffa8a0'),
        (256, 'NVIDIA', '$115.84B REVENUE', '+103%', '#e4bb56'),
    )
    page.rect((LEFT, 672, RIGHT, 725), INK)
    start = LEFT
    for width, name, value, change, color in tiles:
        end = start + width
        if start != LEFT:
            page.line(((start, 681), (start, 716)), GREY)
        center = (start + end) / 2
        box = (start + 3, 674, end - 3, 722)
        page.text(center, 690, name, 'bold', 15, color if name == 'NVIDIA' else PAPER,
                  'm', box=box)
        face, size = 'semi', 15
        advance = font(face, size).getlength(value) / SCALE
        change_width = font(face, size).getlength(change) / SCALE
        position = center - (advance + (5 + change_width if change else 0)) / 2
        page.text(position, 711, value, face, size, color if not change or name == 'NVIDIA' else PAPER,
                  box=box)
        if change:
            page.text(position + advance + 5, 711, change, face, size, color, box=box)
        start = end
    assert start == RIGHT


BRIEFS = (
    ('WAR & DIPLOMACY', (
        ('KERCH BRIDGE HIT AGAIN', 'Ukraine hit it for a second day; part of the road span fell into the strait.'),
        ('PUTIN ‘NOT READY’', 'NYT sources say Kremlin not ready for peace talks; Kyiv seeks jets and air defences.'),
        ('20 MILLION DRONES', 'Kyiv warns Russia plans to launch that many at Ukraine next year.'),
        ('HOUTHI DRONES', 'Five targeted Saudi East-West pipeline pumping stations near Riyadh.'),
        ('KNESSET SPEAKER', 'Israeli MPs elected Matan Kahana, an ally of PM-elect Gadi Eisenkot.'),
        ('BOARD OF PEACE', 'Trump’s board accused Israel and Hamas of failing to keep commitments.'),
        ('GAZA', 'Israeli strikes killed two Hamas commanders; cold is killing displaced people in tents.'),
    )),
    ('AMERICAS · HEALTH · SCIENCE', (
        ('SENATE FLIPS', 'Peltola beat Sullivan in Alaska; Democrats win 56–44, best since 2009.'),
        ('MEASLES MILESTONE', 'U.S. lost measles-free status after 26 years: 5,412 cases, 10 deaths this year.'),
        ('EBOLA SURGES', 'DR Congo tops 11,000 cases, 5,400 deaths; 3 in 4 patients under five die.'),
        ('ONE LIGHT-DAY', 'Voyager 1 reached ~16 billion miles from Earth, a first for any human-made object.'),
        ('OUTAGES', 'Agencies confirmed repeated U.S. computer outages reached even the NSA.'),
        ('JAVA FLAW', 'An AI system at security start-up Calif found a critical flaw in Java.'),
    )),
    ('WORLD IN BRIEF', (
        ('CYCLONE XAVIER', 'Category 5 hit the N. Cook Islands: 215 km/h winds, gusts to 315; shelters open.'),
        ('CYCLONE AKVAN', 'The Bay of Bengal storm bears down on India’s Andhra coast.'),
        ('SIBERIA CRASH', 'A Russian military plane crashed in Kemerovo, killing all 19 aboard.'),
        ('EARTHQUAKES', 'Magnitude 6.0 hit Papua New Guinea; a 5.3 tremor shook Romania.'),
        ('MYANMAR', 'World Court to rule on genocide case; Min Aung Hlaing reviews ASEAN ties.'),
        ('TRADE DEAL', 'Trump’s preliminary Thailand pact cuts some tariffs on U.S. goods to zero.'),
        ('SPORT', 'UCL: Atalanta 2–1 Chelsea, Napoli 2–1 Sporting. NBA: Knicks 111, Raptors 102.'),
    )),
)


def brief(page, left, right, baseline, heading, body):
    size = 14.5
    prefix = heading + ' — '
    bold = font('bold', size)
    start = left - min(0, bold.getbbox(prefix)[0]) / SCALE
    body_start = start + bold.getlength(prefix) / SCALE
    face = font('sans', size)
    first = []
    words = body.split()
    for word in words:
        candidate = ' '.join(first + [word])
        if body_start + face.getlength(candidate) / SCALE > right - 1:
            break
        first.append(word)
    second = ' '.join(words[len(first):])
    box = (left, baseline - 15, right, baseline + 19)
    page.text(start, baseline, prefix, 'bold', size, box=box)
    page.text(body_start, baseline, ' '.join(first), 'sans', size, box=box)
    if second:
        page.text(left, baseline + 15, second, 'sans', size, box=box)


def briefs(page):
    columns = ((36, 340), (360, 664), (684, 988))
    for separator in (350, 674):
        page.line(((separator, 735), (separator, 964)))
    for (left, right), (header, stories) in zip(columns, BRIEFS):
        page.text(left, 747, header, 'bold', 16, RED, box=(left, 731, right, 752))
        page.rule(753, left, right)
        for index, (heading, body) in enumerate(stories):
            brief(page, left, right, 768 + 30 * index, heading, body)


def main():
    page = Page()
    masthead(page)
    leaders(page)
    strait(page)
    world_map(page)
    markets(page)
    briefs(page)
    page.rule(970, color=INK)
    page.text(512, 984, 'Drawn entirely by program · Set in Noto Serif Display & Noto Sans Condensed · '
              'Tomorrow’s front page follows the Shenzhen trilateral', 'sans', 13, GREY, 'm')
    output = Path(__file__).resolve().with_name('entry.png')
    page.image.resize((1024, 1024), Image.Resampling.BICUBIC).save(output, compress_level=9)


if __name__ == '__main__':
    main()
