package com.jk.explore.dto.json;

import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.lang.reflect.RecordComponent;
import java.util.Collection;
import java.util.StringJoiner;

/**
 * <strong>A tiny JSON writer that does what a serialiser does: it walks every
 * field of whatever object it is given.</strong> It does not know which fields
 * were meant to be public. That is the point, and it is why a domain object
 * handed to a serialiser leaks everything it holds.
 */
public final class MiniJson {

    private MiniJson() {
    }

    public static String write(Object value) {
        StringBuilder out = new StringBuilder();
        append(out, value);
        return out.toString();
    }

    private static void append(StringBuilder out, Object value) {
        if (value == null) {
            out.append("null");
        } else if (value instanceof String s) {
            out.append('"').append(s.replace("\"", "\\\"")).append('"');
        } else if (value instanceof Number || value instanceof Boolean) {
            out.append(value);
        } else if (value instanceof Collection<?> items) {
            StringJoiner joiner = new StringJoiner(",", "[", "]");
            for (Object item : items) {
                StringBuilder inner = new StringBuilder();
                append(inner, item);
                joiner.add(inner);
            }
            out.append(joiner);
        } else if (value.getClass().isRecord()) {
            StringJoiner joiner = new StringJoiner(",", "{", "}");
            try {
                for (RecordComponent c : value.getClass().getRecordComponents()) {
                    c.getAccessor().setAccessible(true);
                    StringBuilder inner = new StringBuilder();
                    append(inner, c.getAccessor().invoke(value));
                    joiner.add('"' + c.getName() + "\":" + inner);
                }
            } catch (ReflectiveOperationException e) {
                throw new IllegalStateException(e);
            }
            out.append(joiner);
        } else {
            StringJoiner joiner = new StringJoiner(",", "{", "}");
            try {
                for (Field f : value.getClass().getDeclaredFields()) {
                    if (Modifier.isStatic(f.getModifiers())) {
                        continue;
                    }
                    f.setAccessible(true);
                    StringBuilder inner = new StringBuilder();
                    append(inner, f.get(value));
                    joiner.add('"' + f.getName() + "\":" + inner);
                }
            } catch (IllegalAccessException e) {
                throw new IllegalStateException(e);
            }
            out.append(joiner);
        }
    }

    /** What a client does: find the value of a key in a flat piece of JSON, or null if it is not there. */
    public static String field(String json, String key) {
        String marker = "\"" + key + "\":\"";
        int start = json.indexOf(marker);
        if (start < 0) {
            return null;
        }
        int from = start + marker.length();
        return json.substring(from, json.indexOf('"', from));
    }
}
