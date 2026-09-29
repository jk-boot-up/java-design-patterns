package com.jk.explore.contextmap;

import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * The pattern's map: which contexts exist, how each pair is related, and a check that the code's imports agree.
 */
public final class ContextMap {

    public record Relationship(String from, String to, String kind) {
        @Override
        public String toString() {
            return from + " -> " + to + ": " + kind;
        }
    }

    public static final List<Relationship> RELATIONSHIPS = List.of(
            new Relationship("catalog", "sales", "customer/supplier (sales asks catalogue for prices)"),
            new Relationship("kernel", "sales", "shared kernel (Address, Money)"),
            new Relationship("kernel", "shipping", "shared kernel (Address, Money)"));

    /** What each context may import, read from the map. */
    static final Map<String, Set<String>> ALLOWED = Map.of(
            "sales", Set.of("catalog", "kernel"),
            "shipping", Set.of("kernel"),
            "catalog", Set.of("kernel"),
            "kernel", Set.of());

    private static final Pattern IMPORT = Pattern.compile("^import com\\.jk\\.explore\\.contextmap\\.(\\w+)\\.", Pattern.MULTILINE);

    /** Imports between contexts that the map does not allow. */
    public static List<String> surprises(Path root) {
        List<String> found = new ArrayList<>();
        for (String context : ALLOWED.keySet()) {
            try (Stream<Path> files = Files.walk(root.resolve(context))) {
                for (Path f : files.filter(p -> p.toString().endsWith(".java")).toList()) {
                    found.addAll(check(context, f.getFileName().toString(), Files.readString(f)));
                }
            } catch (IOException e) {
                throw new UncheckedIOException(e);
            }
        }
        return found;
    }

    public static List<String> check(String context, String file, String source) {
        List<String> found = new ArrayList<>();
        Matcher m = IMPORT.matcher(source);
        while (m.find()) {
            String other = m.group(1);
            if (!other.equals(context) && !ALLOWED.getOrDefault(context, Set.of()).contains(other)) {
                found.add(context + "/" + file + " imports " + other + ", which the map does not allow");
            }
        }
        return found;
    }

    private ContextMap() {
    }
}
