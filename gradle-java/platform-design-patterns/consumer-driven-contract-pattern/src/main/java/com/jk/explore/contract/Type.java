package com.jk.explore.contract;

public enum Type {
    STRING, INTEGER, BOOLEAN;

    public boolean matches(Object value) {
        return switch (this) {
            case STRING -> value instanceof String;
            case INTEGER -> value instanceof Integer;
            case BOOLEAN -> value instanceof Boolean;
        };
    }
}
