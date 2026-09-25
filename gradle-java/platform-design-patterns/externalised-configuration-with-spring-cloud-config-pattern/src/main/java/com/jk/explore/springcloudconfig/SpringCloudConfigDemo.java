package com.jk.explore.springcloudconfig;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.LocalDateTime;
import java.util.Comparator;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * Six acts with a real Spring Cloud Config Server, started and stopped by this program.
 *
 * <p>The shop gives free delivery above a threshold. The threshold lives in a git repository,
 * a config server hands it out over HTTP, and the shop fetches it. Nothing here needs a
 * container: the config server is a second Java process, and the git repository is created in
 * a temporary folder with a fixed author and time on every commit, so the output is the same on
 * every run.
 */
public class SpringCloudConfigDemo {

    static final String BASKET = "48.00";
    static final int QUOTES_AFTER_THE_TYPO = 5;

    private static final String APP = "checkout-service";

    public static void main(String[] args) throws IOException {
        Path work = Files.createTempDirectory("shop-config-").toRealPath();
        try (ConfigRepository repo = ConfigRepository.createIn(work.resolve("repo"))) {
            run(repo, work);
        } finally {
            deleteQuietly(work);
        }
    }

    private static void run(ConfigRepository repo, Path work) {
        String first = repo.commit("50.00", "4.99", "Priya in engineering",
                LocalDateTime.of(2025, 3, 3, 10, 0), "Free delivery over 50 pounds");

        ConfigServerProcess server = ConfigServerProcess.start(repo.uri(), work);
        Shop shop = null;
        try {
            // ---------------------------------------------------------------- Act 1
            System.out.println("Act 1 - the setting lives in git, and a config server hands it out over HTTP");
            System.out.println("  git commit " + first + " by Priya in engineering: free-over 50.00");
            System.out.println("  the config server is a separate Java process. asked for " + APP + ", it answers:");
            System.out.println("    " + served(server));
            shop = Shop.start(server.url(), Shop.WhenServerIsDown.REFUSE_TO_START);
            long startedAt = shop.startedAt();
            System.out.println("  the shop starts and fetches its settings from the server.");
            System.out.println("    quote:  " + shop.quote(BASKET).body());
            System.out.println("    banner: " + shop.banner());

            // ---------------------------------------------------------------- Act 2
            System.out.println();
            System.out.println("Act 2 - marketing commits a weekend promotion: free delivery over 35.00");
            String promo = repo.commit("35.00", "4.99", "Maya in marketing",
                    LocalDateTime.of(2025, 3, 7, 16, 30), "Weekend promotion: free delivery over 35 pounds");
            System.out.println("  git commit " + promo + " by Maya in marketing: free-over 35.00");
            System.out.println("  the config server answers at once:");
            System.out.println("    " + served(server));
            System.out.println("  the running shop has not asked again:");
            System.out.println("    quote:  " + shop.quote(BASKET).body());
            System.out.println("  committed, and served, but not in force. The shop fetched its settings once, when it started.");

            // ---------------------------------------------------------------- Act 3
            System.out.println();
            System.out.println("Act 3 - the refresh: POST /actuator/refresh, and no restart");
            System.out.println("  the shop fetches again and reports what changed: " + changedKeys(shop.refresh()));
            System.out.println("    quote:  " + shop.quote(BASKET).body());
            System.out.println("  the same running shop: " + (shop.startedAt() == startedAt
                    ? "yes, still the copy started in act 1. restarts: 0." : "no"));

            // ---------------------------------------------------------------- Act 4
            System.out.println();
            System.out.println("Act 4 - the surprise: the refresh reached the checkout, and not the banner");
            System.out.println("    quote:  " + shop.quote(BASKET).body());
            System.out.println("    banner: " + shop.banner());
            System.out.println("  one running shop, two thresholds. The banner copied the value into a field when the shop started,");
            System.out.println("  and a refresh only rebuilds the objects marked @RefreshScope.");
            shop.close();
            shop = Shop.start(server.url(), Shop.WhenServerIsDown.REFUSE_TO_START);
            System.out.println("  after a restart of the shop:");
            System.out.println("    banner: " + shop.banner());

            // ---------------------------------------------------------------- Act 5
            System.out.println();
            System.out.println("Act 5 - the bill: somebody commits -1 on Saturday morning");
            String typo = repo.commit("-1", "4.99", "Maya in marketing",
                    LocalDateTime.of(2025, 3, 8, 9, 12), "Free delivery for everyone?");
            System.out.println("  git commit " + typo + " by Maya in marketing: free-over -1");
            System.out.println("  the config server does not check values. it serves:");
            System.out.println("    " + served(server));
            Http.Reply refreshed = shop.refresh();
            System.out.println("  the refresh answers " + refreshed.status() + " and reports: " + changedKeys(refreshed));
            int failed = 0;
            int status = 0;
            for (int i = 0; i < QUOTES_AFTER_THE_TYPO; i++) {
                Http.Reply r = shop.quote(BASKET);
                if (!r.ok()) {
                    failed++;
                    status = r.status();
                }
            }
            System.out.println("  the next " + QUOTES_AFTER_THE_TYPO + " quotes: " + failed + " failed, each with HTTP status " + status + ".");
            System.out.println("  the range check refused -1, and with nothing to fall back to, every quote now fails.");
            String fix = repo.commit("35.00", "4.99", "Sam on call",
                    LocalDateTime.of(2025, 3, 8, 9, 40), "Put the weekend promotion back");
            System.out.println("  git commit " + fix + " by Sam on call: free-over 35.00, then a refresh: " + changedKeys(shop.refresh()));
            System.out.println("    quote:  " + shop.quote(BASKET).body());
            System.out.println("  the history is git's own. who changed what, newest first:");
            for (String line : repo.log()) {
                System.out.println("    " + line);
            }

            // ---------------------------------------------------------------- Act 6
            System.out.println();
            System.out.println("Act 6 - the bill: the config server stops");
            server.close();
            System.out.println("  the config server process has stopped.");
            System.out.println("  a refresh of the running shop now answers " + shop.refresh().status() + ".");
            System.out.println("  the running shop keeps what it already fetched:");
            System.out.println("    quote:  " + shop.quote(BASKET).body());
            System.out.println("  a new copy of the shop, told to fail fast:");
            try (Shop refused = Shop.start(server.url(), Shop.WhenServerIsDown.REFUSE_TO_START)) {
                System.out.println("    it started, which it should not have.");
            } catch (RuntimeException e) {
                System.out.println("    refused to start: " + firstLine(e));
            }
            System.out.println("  a new copy of the shop, told the config server is optional:");
            try (Shop optional = Shop.start(server.url(), Shop.WhenServerIsDown.START_ON_LOCAL_DEFAULTS)) {
                System.out.println("    quote:  " + optional.quote(BASKET).body());
                System.out.println("  it started on the default packed inside it. the promotion is gone, with no error.");
            }
        } finally {
            if (shop != null) {
                shop.close();
            }
            server.close();
        }
        System.out.println();
        System.out.println("stopped: the config server process, and all " + Shop.started() + " copies of the shop that started."
                + " still running: " + (Shop.running() + (server.running() ? 1 : 0)) + ".");
    }

    private static final Pattern VERSION = Pattern.compile("\"version\":\"([0-9a-f]{7})");
    private static final Pattern FREE_OVER = Pattern.compile("\"delivery\\.free-over\":([-0-9.]+)");

    /** The two parts of the server's JSON answer that matter here: which commit, and the value. */
    private static String served(ConfigServerProcess server) {
        String json = server.settingsFor(APP, "default");
        return "version " + find(VERSION, json) + ", delivery.free-over " + find(FREE_OVER, json);
    }

    private static String find(Pattern p, String text) {
        Matcher m = p.matcher(text);
        return m.find() ? m.group(1) : "(missing)";
    }

    /** The refresh answers with a JSON list of the keys that changed. Printed sorted. */
    private static String changedKeys(Http.Reply reply) {
        String inner = reply.body().replace("[", "").replace("]", "").replace("\"", "");
        return String.join(", ", Stream.of(inner.split(",")).map(String::trim).sorted().toList());
    }

    /** The outermost message of a failed start, which is the sentence Spring gives a person. */
    private static String firstLine(Throwable e) {
        Throwable t = e;
        while (t.getCause() != null && t.getMessage() != null
                && t.getMessage().startsWith("Unable to load config data")) {
            t = t.getCause();
        }
        return t.getMessage();
    }

    private static void deleteQuietly(Path folder) {
        try (Stream<Path> paths = Files.walk(folder)) {
            paths.sorted(Comparator.reverseOrder()).forEach(p -> p.toFile().delete());
        } catch (IOException e) {
            // A temporary folder that could not be removed is left for the system to clear.
        }
    }
}
