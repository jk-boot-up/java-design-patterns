package com.jk.explore.interpreter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** The nodes themselves, built by hand so the tree is visible in the test. */
class RuleTest {

    private static final Order UK_BIG = new Order(120, "UK", 4, false);
    private static final Order US_SMALL = new Order(30, "US", 1, true);

    @Test
    @DisplayName("a terminal is one comparison and nothing else")
    void terminalsAnswerOnTheirOwn() {
        assertTrue(new BasketOver(50).matches(UK_BIG));
        assertFalse(new BasketOver(500).matches(UK_BIG));
        assertTrue(new CountryIs("UK").matches(UK_BIG));
        assertTrue(new ItemsAtLeast(4).matches(UK_BIG));
        assertTrue(new FirstOrder().matches(US_SMALL));
    }

    @Test
    @DisplayName("country matching ignores case, because people type both")
    void countryIsNotFussyAboutCase() {
        assertTrue(new CountryIs("uk").matches(UK_BIG));
        assertTrue(new CountryIs("Uk").matches(UK_BIG));
    }

    @Test
    @DisplayName("and needs every part; or needs one")
    void nonTerminalsCombineTheirParts() {
        Rule ukAndBig = new AndRule(List.of(new CountryIs("UK"), new BasketOver(100)));
        assertTrue(ukAndBig.matches(UK_BIG));
        assertFalse(ukAndBig.matches(US_SMALL));

        Rule ukOrFirst = new OrRule(List.of(new CountryIs("UK"), new FirstOrder()));
        assertTrue(ukOrFirst.matches(UK_BIG));
        assertTrue(ukOrFirst.matches(US_SMALL));
    }

    @Test
    @DisplayName("not turns any rule, however big, into its opposite")
    void notWrapsWhateverItIsGiven() {
        Rule ukAndBig = new AndRule(List.of(new CountryIs("UK"), new BasketOver(100)));

        assertFalse(new NotRule(ukAndBig).matches(UK_BIG));
        assertTrue(new NotRule(ukAndBig).matches(US_SMALL));
    }

    @Test
    @DisplayName("a rule made of rules is used exactly like a small one")
    void treesNestWithoutAnybodyNoticing() {
        // (UK and over £100) or (first order and 1 item) — three levels deep,
        // and the caller still only calls matches().
        Rule rule = new OrRule(List.of(
                new AndRule(List.of(new CountryIs("UK"), new BasketOver(100))),
                new AndRule(List.of(new FirstOrder(), new ItemsAtLeast(1)))));

        assertTrue(rule.matches(UK_BIG));
        assertTrue(rule.matches(US_SMALL));
        assertFalse(rule.matches(new Order(10, "US", 1, false)));
    }

    @Test
    @DisplayName("a tree can say what it is, by asking its parts")
    void describeIsRebuiltFromTheTree() {
        Rule rule = new OrRule(List.of(
                new AndRule(List.of(new CountryIs("UK"), new BasketOver(100))),
                new NotRule(new FirstOrder())));

        assertEquals("country is UK and basket over 100 or not first order",
                rule.describe());
    }
}
