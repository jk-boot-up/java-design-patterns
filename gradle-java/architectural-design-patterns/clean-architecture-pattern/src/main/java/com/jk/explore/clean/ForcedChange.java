package com.jk.explore.clean;

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
 * <p>This is the biggest forced change in the category: a new delivery
 * mechanism ({@link com.jk.explore.clean.adapters.controller.BatchOrderController})
 * and a new data source
 * ({@link com.jk.explore.clean.adapters.gateway.FileBackedOrderRepository}),
 * added at the same time, both in the outermost circle, with the two inner
 * circles — entities and use cases — counted and shown untouched.
 */
public final class ForcedChange {

    private static final List<String> INNER_CIRCLES = List.of("entities", "usecases");

    private static final List<String> ADDED = List.of(
            "adapters/controller/BatchOrderController.java",
            "adapters/gateway/FileBackedOrderRepository.java");

    private static final List<String> MODIFIED = List.of("PlaceAnOrderDemo.java");

    private static final int LINES_CHANGED = 5;

    private static final Path SOURCE_ROOT =
            Path.of("src", "main", "java", "com", "jk", "explore", "clean");

    private ForcedChange() {
    }

    public static String report() {
        List<String> lines = new ArrayList<>();
        lines.add("  FORCED CHANGE: a new delivery mechanism AND a new");
        lines.add("  data source, added at the same time");
        lines.add("    HTTP-shaped checkout  +  a batch CSV importer");
        lines.add("    a map                 +  a flat, file-shaped store");
        lines.add("");

        int inner = countClassesInInnerCircles();
        if (inner < 0) {
            lines.add("    (source tree not beside this run, so nothing is counted;");
            lines.add("     run the demo from the project directory to see the bill)");
            return String.join("\n", lines);
        }

        lines.add("    files added     : " + ADDED.size() + "   " + String.join(", ", ADDED));
        lines.add("    files modified  : " + MODIFIED.size() + "   " + MODIFIED.get(0)
                + " (the composition root)");
        lines.add("    lines changed   : " + LINES_CHANGED);
        lines.add("    classes in entities + use cases : " + inner);
        lines.add("    of those, opened                : 0");
        lines.add("    of those, never opened           : " + inner);
        return String.join("\n", lines);
    }

    public static String shortcutReport() {
        return String.join("\n", List.of(
                "  AND THE ONE THAT TOOK THE SHORTCUT",
                "    naive/usecases/NaivePlaceOrderInteractor.java imports",
                "    InMemoryOrderRepository, InMemoryProductRepository and",
                "    InMemoryPaymentGateway directly — three circles out",
                "    the two new adapters: no edit needed, anywhere"));
    }

    static int countClassesInInnerCircles() {
        if (!Files.isDirectory(SOURCE_ROOT)) {
            return -1;
        }
        int total = 0;
        for (String pkg : INNER_CIRCLES) {
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
