package com.jk.explore.pipesfilters;

import com.jk.explore.pipesfilters.naive.BigImport;
import org.junit.jupiter.api.Test;

import java.util.ArrayList;
import java.util.List;

import static org.junit.jupiter.api.Assertions.*;

class PipesAndFiltersTest {

    @Test
    void theBigMethodAndThePipelineAgreeOnTheGoodLines() {
        assertEquals(BigImport.run(Shop.LINES), PipesAndFiltersDemo.uk().run(Shop.LINES).out());
    }

    @Test
    void eachFilterCanBeTestedAlone() {
        List<String> rejects = new ArrayList<>();
        assertEquals(new Shop.Parsed("ada", "MUG-BLUE", 2), Shop.parse().apply("ada, MUG-BLUE, 2", rejects).orElseThrow());
        assertEquals(1600, Shop.price().apply(new Shop.Parsed("ada", "MUG-BLUE", 2), rejects).orElseThrow().netPence());
        assertEquals(1920, Shop.ukTax().apply(new Shop.Priced("a", "s", 1, 1600), rejects).orElseThrow().grossPence());
        assertEquals(1936, Shop.euTax().apply(new Shop.Priced("a", "s", 1, 1600), rejects).orElseThrow().grossPence());
        assertTrue(rejects.isEmpty());
    }

    @Test
    void badLinesAreRejectedWithTheirReasonAndTheRestContinue() {
        var r = PipesAndFiltersDemo.uk().run(Shop.LINES);
        assertEquals(3, r.out().size());
        assertEquals(3, r.rejects().size());
        assertTrue(r.rejects().get(0).startsWith("parse: quantity 'twelve'"));
        assertTrue(r.rejects().get(1).startsWith("validate: di asked for 50"));
        assertTrue(r.rejects().get(2).contains("does not have three fields"));
    }

    @Test
    void swappingTheTaxStepChangesOnlyTheTax() {
        var eu = Pipeline.start(Shop.parse()).then(Shop.validate()).then(Shop.price()).then(Shop.euTax()).then(Shop.format());
        assertEquals(List.of("ada: 2 x MUG-BLUE = £19.36"), eu.run(List.of("ada, MUG-BLUE, 2")).out());
        assertEquals(List.of("parse", "validate", "price", "eu-tax", "format"), eu.stageNames());
    }

    @Test
    void anAddedStepSitsWhereItWasPut() {
        Filter<Shop.Parsed, Shop.Parsed> extra = Filter.of("extra", p -> p);
        var p = Pipeline.start(Shop.parse()).then(Shop.validate()).then(extra).then(Shop.price()).then(Shop.ukTax()).then(Shop.format());
        assertEquals(List.of("parse", "validate", "extra", "price", "uk-tax", "format"), p.stageNames());
        assertEquals(1, p.run(List.of("ada, MUG-BLUE, 2")).out().size());
    }

    @Test
    void streamingAndStageByStageGiveTheSameAnswerWithVeryDifferentMemory() {
        List<String> big = new ArrayList<>();
        for (int i = 0; i < 1000; i++) big.add("c" + i + ", MUG-BLUE, " + (1 + i % 9));
        var s = PipesAndFiltersDemo.uk().run(big);
        var b = PipesAndFiltersDemo.uk().runStageByStage(big);
        assertEquals(s.out(), b.out());
        assertEquals(1, s.peakItemsHeld());
        assertEquals(2000, b.peakItemsHeld());
    }

    @Test
    void theBigMethodDropsBadLinesWithNoTrace() {
        assertEquals(5, BigImport.jobsInOneMethod());
        assertEquals(3, BigImport.run(Shop.LINES).size());
    }
}
