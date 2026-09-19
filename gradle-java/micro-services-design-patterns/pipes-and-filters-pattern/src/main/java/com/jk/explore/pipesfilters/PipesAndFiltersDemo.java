package com.jk.explore.pipesfilters;

import com.jk.explore.pipesfilters.naive.BigImport;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class PipesAndFiltersDemo {

    static Pipeline<String, String> uk() {
        return Pipeline.start(Shop.parse()).then(Shop.validate()).then(Shop.price()).then(Shop.ukTax()).then(Shop.format());
    }

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    private static void one() {
        System.out.println("ONE. One method does it all.");
        List<String> out = BigImport.run(Shop.LINES);
        System.out.println("  " + Shop.LINES.size() + " lines in, " + out.size() + " out: " + out + ".");
        System.out.println("  " + BigImport.jobsInOneMethod() + " separate jobs in one loop. the six lines came in, and the three that were dropped left no trace of why.");
    }

    private static void two() {
        System.out.println("TWO. Small steps, joined end to end.");
        var pipeline = uk();
        System.out.println("  the pipeline: " + String.join(" | ", pipeline.stageNames()) + ".");
        System.out.println("  the price step on its own, for one parsed line: " + Shop.price().apply(new Shop.Parsed("ada", "MUG-BLUE", 2), new ArrayList<>()).orElseThrow() + ".");
        System.out.println("  each step can be run, and tested, without the others.");
    }

    private static void three() {
        System.out.println("THREE. Swap a step, add a step.");
        var eu = Pipeline.start(Shop.parse()).then(Shop.validate()).then(Shop.price()).then(Shop.euTax()).then(Shop.format());
        System.out.println("  uk: " + uk().run(List.of("ada, MUG-BLUE, 2")).out() + ".");
        System.out.println("  eu: " + eu.run(List.of("ada, MUG-BLUE, 2")).out() + ".");
        Filter<Shop.Parsed, Shop.Parsed> notBen = Filter.of("not-ben", p -> p);
        var longer = Pipeline.start(Shop.parse()).then(Shop.validate()).then(notBen).then(Shop.price()).then(Shop.ukTax()).then(Shop.format());
        System.out.println("  a new step added in the middle: " + String.join(" | ", longer.stageNames()) + ". no other step changed.");
    }

    private static void four() {
        System.out.println("FOUR. Bad lines are rejected, and the rest go on.");
        Pipeline.Result<String> r = uk().run(Shop.LINES);
        System.out.println("  " + r.out().size() + " orders out:");
        r.out().forEach(l -> System.out.println("    " + l));
        System.out.println("  " + r.rejects().size() + " rejected, each with the step and the reason:");
        r.rejects().forEach(l -> System.out.println("    " + l));
    }

    private static void five() {
        System.out.println("FIVE. Streaming, or one stage at a time.");
        List<String> big = new ArrayList<>();
        for (int i = 0; i < 10_000; i++) {
            big.add("cust-" + i + ", MUG-BLUE, " + (1 + i % 9));
        }
        var streaming = uk().run(big);
        var staged = uk().runStageByStage(big);
        System.out.println("  10000 lines. items held at once: streaming " + streaming.peakItemsHeld() + ", one stage at a time " + staged.peakItemsHeld() + ".");
        System.out.println("  the results are the same: " + streaming.out().equals(staged.out()) + ". only the memory differs.");
    }

    private static void six() {
        System.out.println("SIX. The bill: the steps must agree on the shape.");
        Map<String, String> loose = new HashMap<>();
        loose.put("customer", "ada");
        loose.put("sku", "MUG-BLUE");
        loose.put("qty", "2");
        try {
            int quantity = Integer.parseInt(loose.get("quantity"));
            System.out.println("  " + quantity);
        } catch (NumberFormatException e) {
            System.out.println("  steps passing loose maps: one step calls the field qty and the next asks for quantity. it fails at run time, in the later step: " + e.getClass().getSimpleName() + ".");
        }
        System.out.println("  with typed items, that mistake does not compile. but every step now depends on the type before it, and changing one means changing its neighbours.");
        System.out.println("  and when a line is wrong, the error appears in the step that noticed, which may be far from the step that caused it.");
    }
}
