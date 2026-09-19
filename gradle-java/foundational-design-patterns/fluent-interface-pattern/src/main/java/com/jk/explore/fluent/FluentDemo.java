package com.jk.explore.fluent;

import java.lang.reflect.Method;
import java.util.Arrays;
import java.util.List;

public class FluentDemo {

    public static void main(String[] args) {
        one();
        two();
        three();
        four();
        five();
        six();
    }

    static List<String> methodNames(Class<?> type) {
        return Arrays.stream(type.getDeclaredMethods()).map(Method::getName).sorted().toList();
    }

    private static void one() {
        System.out.println("ONE. A long list of arguments.");
        System.out.println("  find(\"mugs\", 2500, true, true, 10): " + Catalog.find("mugs", 2500, true, true, 10) + ".");
        System.out.println("  find(\"mugs\", 2500, false, true, 10) has the two booleans the other way round: " + Catalog.find("mugs", 2500, false, true, 10) + ".");
        System.out.println("  both compile. which is in stock, and which is the sort? you must count the arguments to know.");
    }

    private static void two() {
        System.out.println("TWO. A query that reads like a sentence.");
        List<String> names = Query.search().category("mugs").under(2500).inStock().cheapestFirst().first(10).run();
        System.out.println("  search().category(\"mugs\").under(2500).inStock().cheapestFirst().first(10): " + names + ".");
        System.out.println("  the same answer as the long call, and every part names itself.");
    }

    private static void three() {
        System.out.println("THREE. Leave out what you do not need.");
        System.out.println("  category only: " + Query.search().category("tea").run() + ".");
        System.out.println("  under 1000, any category: " + Query.search().under(1000).run() + ".");
        System.out.println("  the order of the optional parts does not matter: " + Query.search().inStock().under(2500).category("mugs").run() + ".");
    }

    private static void four() {
        System.out.println("FOUR. Does a call change the query?");
        Query mugs = Query.search().category("mugs");
        Query cheap = mugs.under(1000);
        Query dear = mugs.under(3000);
        System.out.println("  never changing: cheap " + cheap.run() + ", dear " + dear.run() + ", the base still " + mugs.run() + ".");
        MutableQuery base = new MutableQuery().category("mugs");
        MutableQuery cheapM = base.under(1000);
        MutableQuery dearM = base.under(3000);
        System.out.println("  changing itself: cheap " + cheapM.run() + ", dear " + dearM.run() + ". they are the same object: " + (cheapM == dearM) + ". the cheap query was spoiled by the dear one.");
    }

    private static void five() {
        System.out.println("FIVE. Guided steps.");
        System.out.println("  at the start, the only thing offered is: " + methodNames(Steps.NeedsCategory.class) + ".");
        System.out.println("  then: " + methodNames(Steps.NeedsMax.class) + ". then: " + methodNames(Steps.Ready.class) + ".");
        System.out.println("  " + Steps.search().category("mugs").under(2500).inStock().cheapestFirst().run() + ". a call out of order does not compile.");
    }

    private static void six() {
        System.out.println("SIX. The bill.");
        Query wrong = Query.search().category("mugs").under(-5).inStock();
        System.out.println("  under(-5) was accepted. nothing complained.");
        try {
            wrong.run();
        } catch (IllegalStateException e) {
            System.out.println("  it failed at run(): \"" + e.getMessage() + "\". the mistake and the report are on different steps of one long line.");
        }
        System.out.println("  a debugger cannot stop between the calls of one chain, and a stack trace names the line, not the step.");
        System.out.println("  and it is a small language that someone designed: this one has " + methodNames(Query.class).stream().filter(n -> !n.startsWith("lambda")).count() + " methods to learn, and to keep.");
    }
}
