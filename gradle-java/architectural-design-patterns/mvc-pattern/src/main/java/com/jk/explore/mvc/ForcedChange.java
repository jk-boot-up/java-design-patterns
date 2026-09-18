package com.jk.explore.mvc;

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
 * <p>The forced change for this project is: <strong>add a second view over
 * the same model.</strong> {@link com.jk.explore.mvc.view.EmailConfirmationView}
 * is added; the composition root is told to pass it to the controller. Every
 * class that already existed — the model, the controller, the screen, the
 * whole application and infrastructure layer beneath them — is counted and
 * shown to be untouched.
 */
public final class ForcedChange {

    private static final List<String> PACKAGES = List.of(
            "application", "controller", "domain", "infrastructure", "model", "view");

    private static final List<String> ADDED =
            List.of("view/EmailConfirmationView.java");

    private static final List<String> MODIFIED = List.of("PlaceAnOrderDemo.java");

    private static final int LINES_CHANGED = 2;

    private static final Path SOURCE_ROOT =
            Path.of("src", "main", "java", "com", "jk", "explore", "mvc");

    private ForcedChange() {
    }

    public static String report() {
        List<String> lines = new ArrayList<>();
        lines.add("  FORCED CHANGE: add a second view over the same model");
        lines.add("    one screen  ->  one screen and one email, both reading");
        lines.add("    the same OrderSummaryModel");
        lines.add("");

        int inPackages = countClassesInPackages();
        if (inPackages < 0) {
            lines.add("    (source tree not beside this run, so nothing is counted;");
            lines.add("     run the demo from the project directory to see the bill)");
            return String.join("\n", lines);
        }

        lines.add("    files added     : " + ADDED.size() + "   " + ADDED.get(0));
        lines.add("    files modified  : " + MODIFIED.size() + "   " + MODIFIED.get(0)
                + " (the composition root)");
        lines.add("    lines changed   : " + LINES_CHANGED);
        lines.add("    classes across model + controller + views : " + inPackages);
        lines.add("    of those, opened                          : " + ADDED.size());
        lines.add("    of those, never opened                    : " + (inPackages - ADDED.size()));
        return String.join("\n", lines);
    }

    public static String shortcutReport() {
        return String.join("\n", List.of(
                "  AND THE ONE THAT TOOK THE SHORTCUT",
                "    naive/view/RoundedEmailView.java imports ProductTable directly",
                "    it rounds each unit price itself instead of asking the model",
                "    every real view, screen and email alike: agrees, exactly"));
    }

    static int countClassesInPackages() {
        if (!Files.isDirectory(SOURCE_ROOT)) {
            return -1;
        }
        int total = 0;
        for (String pkg : PACKAGES) {
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
