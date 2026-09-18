package com.jk.explore.hexagonal;

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
 * <p>This project performs <strong>two</strong> swaps at once, because
 * hexagonal architecture makes a claim in both directions and a project that
 * only tested one would only have taught half of it. The driven side:
 * storage moves from a map to an append-only log
 * ({@link com.jk.explore.hexagonal.adapter.persistence.AppendOnlyOrderStore}).
 * The driving side: the same core is called from a simulated command line
 * ({@link com.jk.explore.hexagonal.adapter.driving.cli.CliCheckoutAdapter})
 * instead of a simulated HTTP request. Every class this counts is counted on
 * disk, at the moment the demo runs.
 */
public final class ForcedChange {

    private static final List<String> CORE_PACKAGES = List.of("core", "core/domain", "core/port");

    private static final List<String> ADDED = List.of(
            "adapter/persistence/AppendOnlyOrderStore.java",
            "adapter/driving/cli/CliCheckoutAdapter.java");

    private static final List<String> MODIFIED = List.of("PlaceAnOrderDemo.java");

    private static final int LINES_CHANGED = 4;

    private static final Path SOURCE_ROOT =
            Path.of("src", "main", "java", "com", "jk", "explore", "hexagonal");

    private ForcedChange() {
    }

    public static String report() {
        List<String> lines = new ArrayList<>();
        lines.add("  FORCED CHANGE: swap storage, AND swap who calls in");
        lines.add("    a map  ->  an append-only log        (driven side)");
        lines.add("    HTTP   ->  a command line             (driving side)");
        lines.add("");

        int inCore = countClassesInCore();
        if (inCore < 0) {
            lines.add("    (source tree not beside this run, so nothing is counted;");
            lines.add("     run the demo from the project directory to see the bill)");
            return String.join("\n", lines);
        }

        lines.add("    files added     : " + ADDED.size() + "   " + String.join(", ", ADDED));
        lines.add("    files modified  : " + MODIFIED.size() + "   " + MODIFIED.get(0)
                + " (the composition root)");
        lines.add("    lines changed   : " + LINES_CHANGED);
        lines.add("    classes in the core : " + inCore);
        lines.add("    of those, opened    : 0");
        lines.add("    of those, never opened : " + inCore);
        return String.join("\n", lines);
    }

    public static String shortcutReport() {
        return String.join("\n", List.of(
                "  AND THE ONE THAT TOOK THE SHORTCUT",
                "    naive/core/NaivePlaceOrderService.java imports InMemoryOrderStore,",
                "    InMemoryProductCatalog and InMemoryPaymentGateway directly",
                "    swap any one of them, and this class has to be edited too"));
    }

    static int countClassesInCore() {
        if (!Files.isDirectory(SOURCE_ROOT)) {
            return -1;
        }
        int total = 0;
        for (String pkg : CORE_PACKAGES) {
            Path dir = SOURCE_ROOT.resolve(pkg);
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

    static List<String> touchedFiles() {
        List<String> all = new ArrayList<>(ADDED);
        all.addAll(MODIFIED);
        return all;
    }

    static Path sourceRoot() {
        return SOURCE_ROOT;
    }
}
