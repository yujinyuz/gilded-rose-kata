# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose
from gilded_rose import Item


class GildedRoseTest(unittest.TestCase):
    def test_update_quality_lowers_sell_in_and_quality(self):
        items = [
            Item(name="sample-1", sell_in=2, quality=20),
        ]
        gr = GildedRose(items=items)

        # End of day 1
        gr.update_quality()

        assert gr.items[0].sell_in == 1
        assert gr.items[0].quality == 19

    def test_update_quality_lowers_sell_in_and_quality_degrades_twice_as_fast(self):
        items = [
            Item(name="sample-1", sell_in=1, quality=10),
        ]
        gr = GildedRose(items=items)

        # End of day 1
        gr.update_quality()
        assert gr.items[0].sell_in == 0
        assert gr.items[0].quality == 9

        # End of day 2
        gr.update_quality()
        assert gr.items[0].sell_in == -1
        assert gr.items[0].quality == 7  # quality degrades twice faster

        # End of day [3, 4, 5, 6]
        for _ in range(4):
            gr.update_quality()  # end of day 3

        assert gr.items[0].sell_in == -5
        assert gr.items[0].quality == 0  # never goes negative

    def test_update_quality_aged_brie_increases(self):
        items = [
            Item(name="Aged Brie", sell_in=2, quality=0),
        ]
        gr = GildedRose(items=items)

        gr.update_quality()
        assert gr.items[0].sell_in == 1
        assert gr.items[0].quality == 1

        gr.update_quality()
        assert gr.items[0].sell_in == 0
        assert gr.items[0].quality == 2

        gr.update_quality()
        assert gr.items[0].sell_in == -1
        assert gr.items[0].quality == 3

    def test_update_quality_never_more_than_50(self):
        items = [
            Item(name="Aged Brie", sell_in=2, quality=0),
        ]
        gr = GildedRose(items=items)

        days = 55
        for _ in range(days):
            gr.update_quality()

        for item in gr.items:
            assert item.quality == 50
            ...

    def test_update_quality_sulfuras_never_decreases(self):
        items = [
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=0, quality=80),
            Item(name="Sulfuras, Hand of Ragnaros", sell_in=-1, quality=80),
        ]

        gr = GildedRose(items=items)
        gr.update_quality()

        days = 50

        for _ in range(days):
            for index in range(len(gr.items)):
                # Should still be the same sell_in and quality
                assert items[index].sell_in == gr.items[index].sell_in
                assert items[index].quality == gr.items[index].quality

    def test_update_quality_backstage_increase_twice_10_days_or_less(self):
        items = [
            Item(
                name="Backstage passes to a TAFKAL80ETC concert",
                sell_in=10,
                quality=28,
            ),
        ]

        gr = GildedRose(items=items)
        gr.update_quality()

        assert gr.items[0].quality == 30
        assert gr.items[0].sell_in == 9

        sell_in = gr.items[0].sell_in

        for _ in range(sell_in + 1):  # after concert
            gr.update_quality()

        assert gr.items[0].sell_in == -1
        assert gr.items[0].quality == 0  # quality drops to zero after concert

    def test_update_quality_backstage_increase_thrice_5_days_or_less(self):
        items = [
            Item(
                name="Backstage passes to a TAFKAL80ETC concert",
                sell_in=5,
                quality=28,
            ),
        ]

        gr = GildedRose(items=items)
        gr.update_quality()

        assert gr.items[0].quality == 31
        assert gr.items[0].sell_in == 4

        sell_in = gr.items[0].sell_in

        for _ in range(sell_in + 1):  # after concert
            gr.update_quality()

        assert gr.items[0].sell_in == -1
        assert gr.items[0].quality == 0  # quality drops to zero after concert

    def test_update_quality_conjured_items_degrade_in_quality_twice_as_fast(self):
        items = [Item(name="Conjured Mana Cake", sell_in=3, quality=6)]

        gr = GildedRose(items=items)

        gr.update_quality()

        assert gr.items[0].sell_in == 2
        assert gr.items[0].quality == 4

        gr.update_quality()
        assert gr.items[0].sell_in == 1
        assert gr.items[0].quality == 2

        gr.update_quality()
        gr.update_quality()
        gr.update_quality()
        assert gr.items[0].quality == 0


if __name__ == "__main__":
    unittest.main()
