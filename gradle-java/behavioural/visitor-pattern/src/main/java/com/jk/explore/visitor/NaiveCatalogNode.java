package com.jk.explore.visitor;

import java.util.List;
import java.util.Map;

/**
 * The trap, kept for contrast: the same catalog tree, with the reports
 * written where the obvious place to write them is — on the nodes.
 *
 * <p>Nothing here is incompetent. Every one of these methods is the
 * shortest correct way to answer its question, and the first two reports
 * were a pleasure to write this way. The argument is about the fourth and
 * the fifth.
 *
 * <p>Count the methods. One is about the catalog. Four are about reports,
 * and each of the four had to be added to three classes on the day it was
 * asked for. That is the deal being compared against {@link CatalogVisitor}:
 * there, a new report is a new file and the model is untouched; here, a new
 * report edits the domain model, and {@link NaiveProduct} — a class about a
 * thing on a shelf — ends up knowing that a comma inside a CSV field means
 * the field needs quoting.
 *
 * <p>Two of the copies below were not finished. That is not a coincidence
 * either; it is what four near-identical implementations of the same idea
 * do over eighteen months.
 */
public interface NaiveCatalogNode {

    /** The only method here that is about the catalog. */
    String name();

    /** Report one. */
    Money inventoryValue();

    /** Report two. */
    void countInto(Map<String, Integer> counts, String path);

    /** Report three. */
    void appendCsvTo(StringBuilder out, String path);

    /** Report four. */
    void auditInto(List<String> findings, String path);
}
