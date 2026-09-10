package com.jk.explore.interpreter;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.List;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/** Reading a written rule, and refusing one that cannot be read. */
class RuleParserTest {

    @Test
    @DisplayName("a single condition parses to a single node")
    void oneConditionIsNotWrappedInAnything() {
        assertEquals(new BasketOver(50), RuleParser.parse("basket over 50"));
        assertEquals(new FirstOrder(), RuleParser.parse("first order"));
        assertEquals(new CountryIs("UK"), RuleParser.parse("country is UK"));
        assertEquals(new ItemsAtLeast(3), RuleParser.parse("items at least 3"));
    }

    @Test
    @DisplayName("and binds tighter than or, the way a person would read it")
    void andBindsTighterThanOr() {
        Rule rule = RuleParser.parse("country is UK and basket over 100 or first order");

        assertEquals(new OrRule(List.of(
                new AndRule(List.of(new CountryIs("UK"), new BasketOver(100))),
                new FirstOrder())), rule);
    }

    @Test
    @DisplayName("not applies to the condition it sits in front of")
    void notTakesTheConditionAfterIt() {
        Rule rule = RuleParser.parse("not country is UK and basket over 50");

        assertEquals(new AndRule(List.of(
                new NotRule(new CountryIs("UK")), new BasketOver(50))), rule);
        assertTrue(rule.matches(new Order(120, "US", 1, false)));
        assertFalse(rule.matches(new Order(120, "UK", 1, false)));
    }

    @Test
    @DisplayName("keywords are read whatever case they are typed in")
    void keywordsAreCaseInsensitive() {
        Rule rule = RuleParser.parse("Country is UK AND Basket over 50");

        assertTrue(rule.matches(new Order(60, "UK", 1, false)));
    }

    @Test
    @DisplayName("what was written comes back out of the tree unchanged")
    void parsingAndDescribingRoundTrip() {
        List<String> written = List.of(
                "country is UK and basket over 50",
                "basket over 200 or items at least 10",
                "first order and not country is UK",
                "country is UK and basket over 100 or first order and items at least 2");

        for (String text : written) {
            assertEquals(text, RuleParser.parse(text).describe(),
                    "the tree does not say the same thing as the line it was read from");
        }
    }

    @Test
    @DisplayName("a rule it cannot read is refused, naming the phrase")
    void nonsenseIsRefusedLoudly() {
        IllegalArgumentException typo = assertThrows(IllegalArgumentException.class,
                () -> RuleParser.parse("country is UK and basket ovr 50"));
        assertTrue(typo.getMessage().contains("basket ovr 50"), typo.getMessage());

        IllegalArgumentException notANumber = assertThrows(IllegalArgumentException.class,
                () -> RuleParser.parse("basket over fifty"));
        assertTrue(notANumber.getMessage().contains("fifty"), notANumber.getMessage());

        assertThrows(IllegalArgumentException.class, () -> RuleParser.parse("   "));
    }
}
