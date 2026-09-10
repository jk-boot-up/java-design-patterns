package com.jk.explore.interpreter;

/**
 * One node of a promotion rule — the abstract expression of the pattern.
 *
 * <p>Every rule, from the smallest ("country is UK") to the largest, is one of
 * these. That is the whole idea: a big rule and a small rule have the same type,
 * so a big rule can be built out of small ones without anything needing to know
 * how deep it goes.
 *
 * <p>Two methods, and the second one is not decoration. {@link #describe} lets a
 * tree print itself back as the sentence it was built from, which is what makes
 * "why did this order get 15% off?" a question the code can answer.
 */
public interface Rule {

    /** Does this order satisfy the rule? */
    boolean matches(Order order);

    /** The rule as a sentence, rebuilt from the tree rather than remembered. */
    String describe();
}
