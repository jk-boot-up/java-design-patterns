package com.jk.explore.modularmonolith;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * Checks the rule Java cannot: code in one module may not use another module's internal package.
 *
 * <p>It reads each source file's imports. A file in module {@code orders} that
 * imports anything from {@code payments.internal} is a violation. Tools such
 * as ArchUnit or Java's own module system do this in real projects.
 */
public final class BoundaryCheck {

    private static final String BASE = "com.jk.explore.modularmonolith.";
    private static final Pattern IMPORT = Pattern.compile("^import\\s+" + Pattern.quote(BASE) + "(\\w+)\\.internal\\.", Pattern.MULTILINE);

    /** Every violation in the source tree, as "file imports module.internal". */
    public static List<String> scan(Path sourceRoot) {
        List<String> found = new ArrayList<>();
        try (Stream<Path> files = Files.walk(sourceRoot)) {
            for (Path f : files.filter(p -> p.toString().endsWith(".java")).toList()) {
                found.addAll(check(moduleOf(sourceRoot.relativize(f)), f.getFileName().toString(), Files.readString(f)));
            }
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
        return found;
    }

    /** Violations in one file's text, given which module the file belongs to. */
    public static List<String> check(String module, String fileName, String source) {
        List<String> found = new ArrayList<>();
        Matcher m = IMPORT.matcher(source);
        while (m.find()) {
            if (!m.group(1).equals(module)) {
                found.add(fileName + " imports " + m.group(1) + ".internal");
            }
        }
        return found;
    }

    private static String moduleOf(Path relative) {
        return relative.getNameCount() > 1 ? relative.getName(0).toString() : "";
    }

    private BoundaryCheck() {
    }
}
