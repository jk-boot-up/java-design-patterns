package com.jk.explore.bff;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

class SavingRulesTest {

    @Test
    @DisplayName("the current rule states the amount and the percentage")
    void currentRuleStatesBoth() {
        assertEquals("Save £12.00 (20%)",
                SavingRules.current().savingLabel(5999, 4799, true));
    }

    @Test
    @DisplayName("the current rule claims nothing when the higher price is too recent")
    void currentRuleIsSilentOnAYoungListPrice() {
        assertEquals("", SavingRules.current().savingLabel(5999, 4799, false));
    }

    @Test
    @DisplayName("the current rule ignores a saving too small to be worth claiming")
    void currentRuleIgnoresTinySavings() {
        assertEquals("", SavingRules.current().savingLabel(5999, 5899, true));
    }

    @Test
    @DisplayName("the copy is not broken; it passes its own tests and always did")
    void theCopyPassesItsOwnTests() {
        assertEquals("Save £12.00",
                SavingRules.copiedBeforeTheReview().savingLabel(5999, 4799, true));
    }

    @Test
    @DisplayName("the copy claims a saving the current rule refuses to claim")
    void theCopyDivergesExactlyWhereTheReviewChangedTheRule() {
        String current = SavingRules.current().savingLabel(5999, 4799, false);
        String copied = SavingRules.copiedBeforeTheReview().savingLabel(5999, 4799, false);

        assertEquals("", current);
        assertEquals("Save £12.00", copied);
    }
}
