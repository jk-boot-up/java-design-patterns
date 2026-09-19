package com.jk.explore.flagd;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import java.io.ByteArrayOutputStream;
import java.io.PrintStream;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;
import org.junit.jupiter.api.Test;

class FlagdTest {

    @Test
    void theFileCarriesEveryRuleInFlagdsFormat() {
        Map<String, Rule> flags = new TreeMap<>();
        flags.put("gift-wrap", new Rule.Percent(10));
        flags.put("new-search", new Rule.Only(List.of("c1", "c2")));
        String file = Flagd.file(flags);
        assertTrue(file.contains("\"fractional\":[[\"on\",10],[\"off\",90]]"), file);
        assertTrue(file.contains("[\"c1\",\"c2\"]"), file);
        assertTrue(file.startsWith("{\"$schema\""), file);
    }

    @Test
    void offAndOnDifferOnlyInTheirDefault() {
        assertTrue(new Rule.Off().json().contains("\"defaultVariant\":\"off\""));
        assertTrue(new Rule.On().json().contains("\"defaultVariant\":\"on\""));
    }

    @Test
    void theSixActsRunAgainstARealFlagd() throws Exception {
        assumeTrue(Flagd.toolsAvailable(), "needs Docker and the flagd image");
        PrintStream original = System.out;
        ByteArrayOutputStream captured = new ByteArrayOutputStream();
        try {
            System.setOut(new PrintStream(captured, true, StandardCharsets.UTF_8));
            FlagdDemo.main(new String[0]);
        } finally {
            System.setOut(original);
        }
        String out = captured.toString(StandardCharsets.UTF_8);
        for (String act : new String[]{"ONE.", "TWO.", "THREE.", "FOUR.", "FIVE.", "SIX."}) {
            assertTrue(out.contains(act), out);
        }
        assertTrue(out.contains("costs: 5000.\n  the flags file was edited"), out);
        assertTrue(out.contains("the same order costs: 5300"), out);
        assertTrue(out.contains("about a tenth"), out);
        assertTrue(out.contains("of 100 customers, got it: 2."), out);
        assertTrue(out.contains("turned it off. of 100 orders, failed: 0."), out);
        assertTrue(out.contains("flagd is stopped. an order of 5000: 5000."), out);
        assertEquals(1, out.split("possible combinations", -1).length - 1);
    }
}
