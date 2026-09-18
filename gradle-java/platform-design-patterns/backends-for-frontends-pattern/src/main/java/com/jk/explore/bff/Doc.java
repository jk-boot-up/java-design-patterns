package com.jk.explore.bff;

import java.nio.charset.StandardCharsets;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * A response document: ordered field names, and values that are strings, numbers,
 * booleans, lists or nested documents.
 *
 * <p>This is not a JSON library and is not trying to be one. It exists so that the
 * project has one honest measurement. The whole argument for this pattern is that the
 * same product, asked for by two different screens, should come back two different
 * sizes -- and an argument about size is worth nothing if the sizes are quoted from
 * memory. Every byte count in the demo is {@link #bytes()} on a document the program
 * actually built.
 *
 * <p>Fields keep the order they were added, because a document that reorders itself
 * would change size between runs for no reason anybody could explain.
 */
public final class Doc {

    private final Map<String, Object> fields = new LinkedHashMap<>();

    public static Doc doc() {
        return new Doc();
    }

    public Doc put(String name, Object value) {
        fields.put(name, value);
        return this;
    }

    public boolean has(String name) {
        return fields.containsKey(name);
    }

    public Object get(String name) {
        return fields.get(name);
    }

    public List<String> names() {
        return List.copyOf(fields.keySet());
    }

    /**
     * Every field in this document, including nested ones, named the way a client
     * developer would name them in conversation: {@code reviews.average}.
     */
    public List<String> paths() {
        List<String> found = new ArrayList<>();
        collectPaths("", found);
        return found;
    }

    private void collectPaths(String prefix, List<String> into) {
        for (Map.Entry<String, Object> field : fields.entrySet()) {
            String path = prefix.isEmpty() ? field.getKey() : prefix + "." + field.getKey();
            if (field.getValue() instanceof Doc nested) {
                nested.collectPaths(path, into);
            } else {
                into.add(path);
            }
        }
    }

    /**
     * The part of this document a screen actually renders.
     *
     * <p>A field is kept if it is named, or if it is nested inside something named --
     * so {@code reviews} keeps the whole review block, and {@code reviews.average}
     * keeps one number out of it. Anything not named is dropped, which is the point:
     * the difference in size between the whole document and this one is the part that
     * travelled over somebody's mobile data and was thrown away on arrival.
     */
    public Doc select(List<String> wanted) {
        return selectFrom("", wanted);
    }

    private Doc selectFrom(String prefix, List<String> wanted) {
        Doc kept = doc();
        for (Map.Entry<String, Object> field : fields.entrySet()) {
            String path = prefix.isEmpty() ? field.getKey() : prefix + "." + field.getKey();
            boolean named = wanted.contains(path);
            if (field.getValue() instanceof Doc nested) {
                Doc keptNested = named ? nested : nested.selectFrom(path, wanted);
                if (named || !keptNested.fields.isEmpty()) {
                    kept.put(field.getKey(), keptNested);
                }
            } else if (named || isUnderNamedParent(path, wanted)) {
                kept.put(field.getKey(), field.getValue());
            }
        }
        return kept;
    }

    private static boolean isUnderNamedParent(String path, List<String> wanted) {
        return wanted.stream().anyMatch(name -> path.startsWith(name + "."));
    }

    /** The document as it would go on the wire: no spaces, no line breaks. */
    public String compact() {
        StringBuilder out = new StringBuilder("{");
        boolean first = true;
        for (Map.Entry<String, Object> field : fields.entrySet()) {
            if (!first) {
                out.append(',');
            }
            first = false;
            out.append('"').append(field.getKey()).append("\":");
            writeValue(out, field.getValue());
        }
        return out.append('}').toString();
    }

    private static void writeValue(StringBuilder out, Object value) {
        if (value instanceof Doc nested) {
            out.append(nested.compact());
        } else if (value instanceof List<?> list) {
            out.append('[');
            for (int i = 0; i < list.size(); i++) {
                if (i > 0) {
                    out.append(',');
                }
                writeValue(out, list.get(i));
            }
            out.append(']');
        } else if (value instanceof String text) {
            out.append('"').append(text.replace("\"", "\\\"")).append('"');
        } else {
            out.append(value);
        }
    }

    /** What the response costs on the wire, in bytes. */
    public int bytes() {
        return compact().getBytes(StandardCharsets.UTF_8).length;
    }

    /** The document laid out for a human, used only by the demo's printing. */
    public String pretty() {
        StringBuilder out = new StringBuilder();
        writePretty(out, this, "");
        return out.toString();
    }

    private static void writePretty(StringBuilder out, Doc doc, String indent) {
        out.append("{\n");
        int remaining = doc.fields.size();
        for (Map.Entry<String, Object> field : doc.fields.entrySet()) {
            out.append(indent).append("  \"").append(field.getKey()).append("\": ");
            Object value = field.getValue();
            if (value instanceof Doc nested) {
                writePretty(out, nested, indent + "  ");
            } else {
                writeValue(out, value);
            }
            out.append(--remaining > 0 ? ",\n" : "\n");
        }
        out.append(indent).append('}');
    }

    @Override
    public String toString() {
        return compact();
    }
}
