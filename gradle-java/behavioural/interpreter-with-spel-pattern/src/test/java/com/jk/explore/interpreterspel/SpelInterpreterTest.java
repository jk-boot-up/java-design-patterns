package com.jk.explore.interpreterspel;

import org.junit.jupiter.api.Test;
import org.springframework.expression.ExpressionException;
import org.springframework.expression.spel.SpelEvaluationException;
import org.springframework.expression.spel.SpelParseException;

import java.util.List;

import static com.jk.explore.interpreterspel.SpelPromotionsApplication.*;
import static org.junit.jupiter.api.Assertions.*;

class SpelInterpreterTest {

    private final PromotionBook book = new PromotionBook(false, PROMOTIONS);

    @Test
    void rulesGiveTheExpectedPromotions() {
        assertEquals(List.of("UKBIG (15% off)"), book.applicableTo(ASHA));
        assertEquals(List.of("WELCOME10 (10% off)", "NOTUK (5% off)"), book.applicableTo(BEN));
        assertEquals(List.of("UKBIG (15% off)", "BULK (20% off)"), book.applicableTo(CAROL));
    }

    @Test
    void conditionalAndMethodCallAndRemainderWork() {
        PromotionBook b = new PromotionBook(false,
                "SMALLUK | 5 | country == 'UK' ? basketPence < 5000 : false",
                "VOUCHER | 8 | voucher != null and voucher matches 'SPR.*'",
                "MODULO | 1 | items % 2 == 0");
        assertEquals(List.of("VOUCHER (8% off)"), b.applicableTo(BEN));
        assertEquals(List.of("MODULO (1% off)"), b.applicableTo(ASHA));
    }

    @Test
    void invalidSyntaxFailsAtBuildTime() {
        assertThrows(SpelParseException.class, () -> new PromotionBook(false, "X | 1 | country == 'UK' and and 1"));
    }

    @Test
    void misspelledPropertyFailsOnlyAtEvaluationTime() {
        PromotionBook b = new PromotionBook(false, "X | 1 | contry == 'UK'");
        assertThrows(SpelEvaluationException.class, () -> b.applicableTo(ASHA));
    }

    @Test
    void fullContextRunsStaticMethodsAndReadOnlyRefuses() {
        String rule = "X | 1 | T(java.lang.System).getProperty('java.specification.version') != null";
        assertEquals(1, new PromotionBook(true, rule).applicableTo(ASHA).size());
        assertThrows(ExpressionException.class, () -> new PromotionBook(false, rule).applicableTo(ASHA));
    }

    @Test
    void readOnlyContextRefusesMethodCalls() {
        assertThrows(ExpressionException.class, () -> new PromotionBook(false, "X | 1 | voucher != null and voucher.length() > 3").applicableTo(BEN));
        assertEquals(1, new PromotionBook(true, "X | 1 | voucher != null and voucher.length() > 3").applicableTo(BEN).size());
    }

    @Test
    void nullVoucherFailsWithoutSafeNavigationAndIsFalseWith() {
        assertThrows(ExpressionException.class, () -> new PromotionBook(false, "X | 1 | voucher.empty == false").applicableTo(ASHA));
        PromotionBook safe = new PromotionBook(false, "X | 1 | voucher?.empty == false");
        assertEquals(List.of(), safe.applicableTo(ASHA));
        assertEquals(List.of("X (1% off)"), safe.applicableTo(BEN));
    }
}
