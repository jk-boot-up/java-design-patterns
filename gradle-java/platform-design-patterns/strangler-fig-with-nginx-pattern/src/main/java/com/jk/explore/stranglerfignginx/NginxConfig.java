package com.jk.explore.stranglerfignginx;

import java.util.ArrayList;
import java.util.List;

/**
 * The router's whole configuration, as NGINX reads it. This class writes the text; the demo
 * copies it into the container and tells NGINX to reload.
 *
 * <p>Every route starts on the old shop, through one catch-all rule, {@code location /}. Moving
 * a route to the new service means adding one more {@code location} block for that route's
 * prefix. Nothing else changes, which is the whole of the pattern.
 *
 * <p>A configuration is a value: each method returns a new one, so every act can say exactly
 * which configuration it is running.
 */
public final class NginxConfig {

    /** The address NGINX uses, from inside its container, to reach this machine. */
    public static final String HOST = "host.testcontainers.internal";

    /** The rule an old configuration carried for years: cache catalogue reads for a minute. */
    public static final String LEGACY_CACHE_RULE = "location ~ ^/api/(prices|stock)/";

    /**
     * One route moved to the new service.
     *
     * @param prefix         the start of the path, such as {@code /api/prices/}
     * @param stopLooking    write {@code ^~} before the prefix, which tells NGINX not to try
     *                       any regular-expression rule once this prefix has matched
     * @param trailingSlash  write the new service's address with a slash after it, which tells
     *                       NGINX to cut the matched prefix off the path it passes on
     */
    public record Move(String prefix, boolean stopLooking, boolean trailingSlash) {

        String block() {
            return "        location " + (stopLooking ? "^~ " : "") + prefix + " {\n"
                    + "            proxy_pass http://new_service" + (trailingSlash ? "/" : "") + ";\n"
                    + "        }\n";
        }

        public String locationLine() {
            return "location " + (stopLooking ? "^~ " : "") + prefix;
        }

        public String proxyPassLine() {
            return "proxy_pass http://new_service" + (trailingSlash ? "/" : "") + ";";
        }
    }

    private final boolean everythingToNew;
    private final boolean legacyCacheRule;
    private final List<Move> moves;

    private NginxConfig(boolean everythingToNew, boolean legacyCacheRule, List<Move> moves) {
        this.everythingToNew = everythingToNew;
        this.legacyCacheRule = legacyCacheRule;
        this.moves = List.copyOf(moves);
    }

    /** Where every migration starts: NGINX in front, and every route to the old shop. */
    public static NginxConfig everythingOnTheOldShop() {
        return new NginxConfig(false, false, List.of());
    }

    /** The big bang: one line sends every route to the new service at once. */
    public static NginxConfig bigBang() {
        return new NginxConfig(true, false, List.of());
    }

    /** The same configuration, with the old caching rule for catalogue reads added. */
    public NginxConfig withLegacyCacheRule() {
        return new NginxConfig(everythingToNew, true, moves);
    }

    /** Moves one route, written the way most people first write it. */
    public NginxConfig move(String prefix) {
        return with(new Move(prefix, false, false));
    }

    /** Moves one route with {@code ^~}, so no regular-expression rule can take it back. */
    public NginxConfig moveAndStopLooking(String prefix) {
        return with(new Move(prefix, true, false));
    }

    /** Moves one route with a slash after the new service's address. */
    public NginxConfig moveWithTrailingSlash(String prefix) {
        return with(new Move(prefix, true, true));
    }

    public List<Move> moves() {
        return moves;
    }

    private NginxConfig with(Move move) {
        List<Move> all = new ArrayList<>(moves);
        all.add(move);
        return new NginxConfig(everythingToNew, legacyCacheRule, all);
    }

    /**
     * The full text of nginx.conf.
     *
     * @param generation a number that goes up with every configuration, served back on
     *                   {@code /router/generation} so the demo can tell when a reload has
     *                   really taken effect
     */
    public String render(int generation, int oldShopPort, int newServicePort) {
        StringBuilder s = new StringBuilder();
        s.append("# Written by the demo. Generation ").append(generation).append(".\n");
        // One worker, so that the second act can count worker processes exactly.
        s.append("worker_processes 1;\n");
        s.append("events { worker_connections 64; }\n");
        s.append("http {\n");
        s.append("    access_log off;\n");
        s.append("    upstream old_shop    { server ").append(HOST).append(':').append(oldShopPort).append("; }\n");
        s.append("    upstream new_service { server ").append(HOST).append(':').append(newServicePort).append("; }\n");
        s.append("    server {\n");
        s.append("        listen 8080;\n");
        s.append("        location = /router/generation { return 200 \"").append(generation).append("\"; }\n");
        if (legacyCacheRule) {
            s.append("        # Written years ago: let browsers cache catalogue reads for a minute.\n");
            s.append("        ").append(LEGACY_CACHE_RULE).append(" {\n");
            s.append("            proxy_pass http://old_shop;\n");
            s.append("            add_header Cache-Control \"max-age=60\";\n");
            s.append("        }\n");
        }
        for (Move move : moves) {
            s.append(move.block());
        }
        s.append("        location / {\n");
        s.append("            proxy_pass http://").append(everythingToNew ? "new_service" : "old_shop").append(";\n");
        s.append("        }\n");
        s.append("    }\n");
        s.append("}\n");
        return s.toString();
    }
}
