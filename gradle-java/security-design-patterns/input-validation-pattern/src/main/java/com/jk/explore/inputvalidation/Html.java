package com.jk.explore.inputvalidation;

/**
 * Output encoding: make text safe to put inside a web page, whatever it contains.
 */
public final class Html {

    public static String escape(String text) {
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                .replace("\"", "&quot;").replace("'", "&#39;");
    }

    private Html() {
    }
}
