package com.jk.explore.servant;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotEquals;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvSource;

class ShippingServantTest {

    private final ShippingServant servant = new ShippingServant(120, 160);

    @ParameterizedTest
    @CsvSource({"1, 280", "1000, 280", "1001, 440", "2300, 600", "180000, 28920"})
    void chargesPerStartedKilo(int grams, long pence) {
        assertEquals(pence, servant.postage(new Items.Parcel("x", grams, "y")));
    }

    @Test
    void sameWeightSamePriceWhateverTheItem() {
        assertEquals(servant.postage(new Items.Letter("a", 80, "b")),
                servant.postage(new Items.GiftCard("a", 80, "b", 1000)));
    }

    @Test
    void labelHasEverything() {
        assertEquals("PARCEL-1 | 2300 g | to Leeds | £6.00", servant.label(ServantDemo.PARCEL));
    }

    @Test
    void copiesDrifted() {
        assertNotEquals(servant.postage(ServantDemo.LETTER), CopiedPostage.letter(ServantDemo.LETTER));
        assertEquals(servant.postage(ServantDemo.PARCEL), CopiedPostage.parcel(ServantDemo.PARCEL));
    }
}
