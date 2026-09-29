package com.jk.explore.servant;

import java.util.ArrayList;
import java.util.List;

/**
 * The five acts: copied postage code, one servant, a new kind of item, testing the servant alone, and the bill.
 */
public final class ServantDemo {

    static final Items.Parcel PARCEL = new Items.Parcel("PARCEL-1", 2300, "Leeds");
    static final Items.Letter LETTER = new Items.Letter("LETTER-1", 80, "Bath");
    static final Items.GiftCard GIFT = new Items.GiftCard("GIFTCARD-1", 20, "York", 5000);

    public static void main(String[] args) {
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() {
        List<String> out = new ArrayList<>();

        out.add("ONE. Each item carries its own copy of the postage sum.");
        out.add("  the carrier's new rates: 120p, plus 160p per started kilo");
        out.add("  parcel, 2300 g: " + ShippingServant.pounds(CopiedPostage.parcel(PARCEL)) + " (copy updated)");
        out.add("  letter, 80 g: " + ShippingServant.pounds(CopiedPostage.letter(LETTER)) + " (copy missed, should be £2.80)");
        out.add("  gift card, 20 g: " + ShippingServant.pounds(CopiedPostage.giftCard(GIFT)) + " (copy missed)");
        out.add("  a shared parent class would tie every item into one family tree just to be posted");

        out.add("");
        out.add("TWO. One shipping servant serves every item.");
        ShippingServant servant = new ShippingServant(120, 160);
        for (Shippable item : List.<Shippable>of(PARCEL, LETTER, GIFT)) {
            out.add("  " + servant.label(item));
        }
        out.add("  the rates live in one place; the items hold no shipping code at all");

        out.add("");
        out.add("THREE. A new kind of item, shipped with no new shipping code.");
        Items.Pallet pallet = new Items.Pallet("PALLET-1", 180000, "Hull");
        out.add("  " + servant.label(pallet));
        out.add("  the pallet only had to say its name, weight and city");

        out.add("");
        out.add("FOUR. The servant can be tested on its own.");
        Shippable testItem = new Shippable() {
            public String name() {
                return "TEST";
            }

            public int grams() {
                return 1001;
            }

            public String city() {
                return "Anywhere";
            }
        };
        out.add("  a made-up item of 1001 g: " + ShippingServant.pounds(servant.postage(testItem))
                + ", two started kilos");
        out.add("  one servant object served every item and kept no state between them");

        out.add("");
        out.add("FIVE. The bill: the behaviour is not on the item.");
        out.add("  there is no parcel.postage(): you must know the servant exists to find it");
        out.add("  and every item must now show its weight and city to anyone who asks");
        return out;
    }

    private ServantDemo() {
    }
}
