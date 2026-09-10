package com.jk.explore.interpreter;

/**
 * The context: one order, and everything a promotion rule is allowed to ask
 * about.
 *
 * <p>In the pattern's own vocabulary this is the <em>context</em> — the thing
 * an expression is interpreted against. It is a record because nothing about an
 * order changes while a rule is being evaluated, and because a rule that cannot
 * modify the order it is judging is much easier to trust.
 *
 * <p>Its four accessors are also the whole vocabulary of the rule language.
 * Anything the language can ask, it asks here; add a fifth field and you have
 * added a word marketing can use.
 */
public record Order(int basketPounds, String country, int itemCount, boolean firstOrder) {

    @Override
    public String toString() {
        return "£" + basketPounds + ", " + country + ", " + itemCount + " items, "
                + (firstOrder ? "first order" : "returning shopper");
    }
}
