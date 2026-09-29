package com.jk.explore.translator;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

import org.junit.jupiter.api.Test;

class TranslatorTest {

    @Test
    void everyFormatBecomesTheSameShape() {
        assertEquals(new OrderMessage("W-1", "KETTLE-1", 1, 3000), Translators.WEB.translate(MessageTranslatorDemo.WEB));
        assertEquals(new OrderMessage("A-77", "MUG-1", 2, 1600), Translators.MARKET_A.translate(MessageTranslatorDemo.CSV));
        assertEquals(new OrderMessage("B-9", "TEAPOT-1", 1, 2500), Translators.MARKET_B.translate(MessageTranslatorDemo.JSON));
        assertEquals(new OrderMessage("C-5", "KETTLE-1", 1, 3000), Translators.MARKET_C.translate(MessageTranslatorDemo.XML));
    }

    @Test
    void normalizerPicksByFormat() {
        Normalizer n = Normalizer.standard();
        assertEquals("marketplace A (CSV)", n.formatOf(MessageTranslatorDemo.CSV));
        assertEquals("A-77", n.normalize(MessageTranslatorDemo.CSV).orderId());
    }

    @Test
    void unknownFormatIsRefused() {
        assertThrows(IllegalArgumentException.class, () -> Normalizer.standard().normalize(MessageTranslatorDemo.XML));
    }
}
