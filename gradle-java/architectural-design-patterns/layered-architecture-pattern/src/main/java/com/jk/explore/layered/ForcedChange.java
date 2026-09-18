package com.jk.explore.layered;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;

/**
 * The cost of the forced change, counted rather than claimed.
 *
 * <p>Every project in this category performs the change its architecture says
 * it makes cheap, and prints the bill. Adjectives are free; a file count is
 * not. This class counts the files <em>on disk, at the moment the demo
 * runs</em>, so the number in the video and the number in the README cannot
 * drift apart from the number that is true.
 *
 * <p>The forced change for this project is: <strong>replace the storage
 * layer.</strong> Orders stop living in a map keyed by id and start living in
 * an append-only log read backwards. The two files that change are recorded
 * below, because which files a change touched is a fact about the change rather
 * than something that can be derived. Everything else is counted.
 *
 * <p>The count that carries the argument is the last one. Not "one file added",
 * which any architecture can manage, but the number of classes that were
 * <em>not opened</em> — because that is the number layering is spending its
 * indirection to buy.
 */
public final class ForcedChange {

    /** The four packages that make up the architecture proper. */
    private static final List<String> LAYERS =
            List.of("domain", "application", "infrastructure", "presentation");

    /** Added by the change: the new storage implementation. */
    private static final List<String> ADDED =
            List.of("infrastructure/AppendOnlyOrderTable.java");

    /**
     * Modified by the change: the composition root, which is this demo. One
     * line, the one that picks which store to construct. The composition root
     * is not in any layer, which is the point of having one.
     */
    private static final List<String> MODIFIED = List.of("PlaceAnOrderDemo.java");

    /** Measured with {@code git diff --stat} when the change was made. */
    private static final int LINES_CHANGED = 1;

    private static final Path SOURCE_ROOT =
            Path.of("src", "main", "java", "com", "jk", "explore", "layered");

    private ForcedChange() {
    }

    /**
     * The block the demo prints. The format is fixed for the whole category so
     * that the five projects' numbers can be read side by side.
     */
    public static String report() {
        List<String> lines = new ArrayList<>();
        lines.add("  FORCED CHANGE: replace the storage layer");
        lines.add("    a map keyed by order id  ->  an append-only log, read backwards");
        lines.add("");

        int inLayers = countClassesInLayers();
        if (inLayers < 0) {
            lines.add("    (source tree not beside this run, so nothing is counted;");
            lines.add("     run the demo from the project directory to see the bill)");
            return String.join("\n", lines);
        }

        lines.add("    files added     : " + ADDED.size() + "   " + ADDED.get(0));
        lines.add("    files modified  : " + MODIFIED.size() + "   " + MODIFIED.get(0)
                + " (the composition root)");
        lines.add("    lines changed   : " + LINES_CHANGED);
        lines.add("    classes in the four layers : " + inLayers);
        lines.add("    of those, opened           : " + ADDED.size());
        lines.add("    of those, never opened     : " + (inLayers - ADDED.size()));
        return String.join("\n", lines);
    }

    /**
     * What the shortcut cost. Kept separate from the block above because it is
     * not part of the architecture's bill — it is the bill for ignoring it.
     */
    public static String shortcutReport() {
        return String.join("\n", List.of(
                "  AND THE ONE THAT TOOK THE SHORTCUT",
                "    naive/presentation/OrderHistoryScreen.java imports InMemoryOrderTable",
                "    it went straight to storage, so the swap does not compile for it",
                "    every screen that went through the application layer: untouched"));
    }

    /**
     * Counts {@code .java} files under the four layer packages, on disk.
     *
     * @return the count, or -1 if the source tree is not where the demo is
     *         running from — in which case nothing is claimed rather than
     *         something being guessed.
     */
    static int countClassesInLayers() {
        if (!Files.isDirectory(SOURCE_ROOT)) {
            return -1;
        }
        int total = 0;
        for (String layer : LAYERS) {
            Path dir = SOURCE_ROOT.resolve(layer);
            if (!Files.isDirectory(dir)) {
                continue;
            }
            try (Stream<Path> files = Files.list(dir)) {
                total += (int) files.filter(p -> p.toString().endsWith(".java")).count();
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
        return total;
    }

    /** The files the change touched, as recorded, for a test to check still exist. */
    static List<String> touchedFiles() {
        List<String> all = new ArrayList<>(ADDED);
        all.addAll(MODIFIED);
        return all;
    }

    static Path sourceRoot() {
        return SOURCE_ROOT;
    }
}
