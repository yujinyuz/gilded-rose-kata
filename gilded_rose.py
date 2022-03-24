# -*- coding: utf-8 -*-
from typing import List
from typing import Optional


def _update_quality(self):
    for item in self.items:
        if (
            item.name != "Aged Brie"
            and item.name != "Backstage passes to a TAFKAL80ETC concert"
        ):
            if item.quality > 0:
                if item.name != "Sulfuras, Hand of Ragnaros":
                    item.quality = item.quality - 1
        else:
            if item.quality < 50:
                item.quality = item.quality + 1
                if item.name == "Backstage passes to a TAFKAL80ETC concert":
                    if item.sell_in < 11:
                        if item.quality < 50:
                            item.quality = item.quality + 1
                    if item.sell_in < 6:
                        if item.quality < 50:
                            item.quality = item.quality + 1
        if item.name != "Sulfuras, Hand of Ragnaros":
            item.sell_in = item.sell_in - 1
        if item.sell_in < 0:
            if item.name != "Aged Brie":
                if item.name != "Backstage passes to a TAFKAL80ETC concert":
                    if item.quality > 0:
                        if item.name != "Sulfuras, Hand of Ragnaros":
                            item.quality = item.quality - 1
                else:
                    item.quality = item.quality - item.quality
            else:
                if item.quality < 50:
                    item.quality = item.quality + 1


class GildedRose(object):
    def __init__(self, items: Optional[List["Item"]] = None):
        if items is None:
            items = []
        self.items = items

    def update_quality(self):
        items_with_exceptions = [
            "Aged Brie",
            "Backstage passes to a TAFKAL80ETC concert",
            "Sulfuras, Hand of Ragnaros",
            "Conjured Mana Cake",
        ]

        for item in self.items:

            # Just process items without exceptions normally
            if item.name not in items_with_exceptions:
                item.sell_in -= 1
                # Item quality should never be greater 50 or less than 0
                if item.quality < 50 and item.quality > 0:
                    item.quality -= 1
                    if item.sell_in < 0 and item.quality > 0:
                        item.quality -= 1
                continue

            # A legendary item we don't want to deal with
            if item.name == "Sulfuras, Hand of Ragnaros":
                continue

            if item.name == "Aged Brie":
                if item.quality < 50:
                    item.quality += 1
                item.sell_in -= 1
                continue

            if item.name == "Backstage passes to a TAFKAL80ETC concert":
                item.sell_in -= 1
                if item.quality < 50:
                    item.quality += 1

                # If sell in <= 10 days then increase quality by another
                if item.quality < 50 and item.sell_in <= 10:
                    item.quality += 1

                # If sell in <= 5 days then increase quality by another
                if item.quality < 50 and item.sell_in <= 5:
                    item.quality += 1

                if item.sell_in < 0:
                    item.quality = 0

                continue

            if item.name == "Conjured Mana Cake":
                item.sell_in -= 1
                # Item quality should never be greater 50 or less than 0
                if item.quality < 50 and item.quality > 0:
                    # Degrades twice as fast
                    item.quality -= 2
                    if item.sell_in < 0 and item.quality > 0:
                        item.quality -= 1
                continue






class Item:
    def __init__(self, name: str, sell_in: int, quality: int):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
