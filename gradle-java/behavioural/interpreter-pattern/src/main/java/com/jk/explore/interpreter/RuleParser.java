package com.jk.explore.interpreter;

import java.util.ArrayList;
import java.util.List;

/**
 * Turns a written rule into a tree of {@link Rule} objects.
 *
 * <p>Strictly speaking the parser is <em>not</em> the Interpreter pattern — the
 * pattern is the tree and its {@code matches} method, and the Gang of Four say
 * plainly that how you build the tree is your own business. It is here because
 * a rule language nobody can write in is not much of a rule language, and
 * because it is what lets a promotion be a line of text that marketing edits
 * rather than a Java change that waits for a release.
 *
 * <p>The grammar is deliberately tiny, and there are no brackets:
 *
 * <pre>
 *   rule       :=  group ( "or" group )*
 *   group      :=  condition ( "and" condition )*
 *   condition  :=  [ "not" ] terminal
 *   terminal   :=  "basket over" N | "country is" X | "items at least" N
 *                  | "first order"
 * </pre>
 *
 * <p>Splitting on {@code or} first and {@code and} second is what gives
 * <em>and</em> the tighter grip, so "A and B or C" reads as "(A and B) or C"
 * the way a person would say it. Without brackets that is the only precedence
 * there is, which is a real limit and is written down as one.
 *
 * <p>Anything it cannot read, it refuses, naming the phrase. A rule language
 * that guesses is worse than no rule language: a typo should stop the promotion
 * being saved on Wednesday, not quietly stop matching on Friday.
 */
public final class RuleParser {

    private RuleParser() {
    }

    public static Rule parse(String text) {
        if (text == null || text.isBlank()) {
            throw new IllegalArgumentException("a rule cannot be empty");
        }
        return parseOr(text.trim());
    }

    private static Rule parseOr(String text) {
        List<Rule> parts = new ArrayList<>();
        for (String piece : text.split("(?i)\\s+or\\s+")) {
            parts.add(parseAnd(piece.trim()));
        }
        return parts.size() == 1 ? parts.get(0) : new OrRule(parts);
    }

    private static Rule parseAnd(String text) {
        List<Rule> parts = new ArrayList<>();
        for (String piece : text.split("(?i)\\s+and\\s+")) {
            parts.add(parseCondition(piece.trim()));
        }
        return parts.size() == 1 ? parts.get(0) : new AndRule(parts);
    }

    private static Rule parseCondition(String text) {
        String lower = text.toLowerCase();
        if (lower.startsWith("not ")) {
            return new NotRule(parseCondition(text.substring(4).trim()));
        }
        if (lower.equals("first order")) {
            return new FirstOrder();
        }
        if (lower.startsWith("basket over ")) {
            return new BasketOver(number(text, text.substring(12).trim()));
        }
        if (lower.startsWith("items at least ")) {
            return new ItemsAtLeast(number(text, text.substring(15).trim()));
        }
        if (lower.startsWith("country is ")) {
            return new CountryIs(text.substring(11).trim());
        }
        throw new IllegalArgumentException("I do not understand \"" + text + "\"");
    }

    private static int number(String whole, String digits) {
        try {
            return Integer.parseInt(digits);
        } catch (NumberFormatException e) {
            throw new IllegalArgumentException(
                    "\"" + digits + "\" is not a number, in \"" + whole + "\"");
        }
    }
}
