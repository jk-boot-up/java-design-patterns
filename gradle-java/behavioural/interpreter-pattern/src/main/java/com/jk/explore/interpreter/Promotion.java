package com.jk.explore.interpreter;

/**
 * One promotion: a code, a percentage, and the rule that decides who gets it.
 *
 * <p>A promotion is written as one line of text — {@code "SAVE10 | 10 | country
 * is UK and basket over 50"} — because that is the whole point of building the
 * language. The line can live in a database, a spreadsheet or a config file,
 * and nothing about adding one involves a compiler.
 */
public record Promotion(String code, int percentOff, Rule rule) {

    public static Promotion fromLine(String line) {
        String[] fields = line.split("\\|");
        if (fields.length != 3) {
            throw new IllegalArgumentException(
                    "expected CODE | PERCENT | RULE, got \"" + line + "\"");
        }
        return new Promotion(fields[0].trim(),
                Integer.parseInt(fields[1].trim()),
                RuleParser.parse(fields[2].trim()));
    }

    public boolean appliesTo(Order order) {
        return rule.matches(order);
    }

    /** What to write in the audit log, straight out of the tree. */
    public String explain() {
        return code + " (" + percentOff + "% off) applies when " + rule.describe();
    }
}
