package com.jk.explore.pactcdc;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintStream;
import java.util.ArrayList;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import org.junit.platform.engine.TestExecutionResult;
import org.junit.platform.engine.discovery.DiscoverySelectors;
import org.junit.platform.launcher.Launcher;
import org.junit.platform.launcher.LauncherDiscoveryRequest;
import org.junit.platform.launcher.TestExecutionListener;
import org.junit.platform.launcher.TestIdentifier;
import org.junit.platform.launcher.core.LauncherDiscoveryRequestBuilder;
import org.junit.platform.launcher.core.LauncherFactory;

/** Starts one release of the catalog, and runs Pact's provider verification against it, as a build would. */
public class Verifier {

    /** What the verification found: which interactions it replayed, and which failed and why. */
    public record Outcome(int checked, List<String> problems) {
        public boolean passed() {
            return problems.isEmpty();
        }
    }

    static {
        System.setProperty("pact_do_not_track", "true");
    }

    private static final Pattern CONSUMER = Pattern.compile("between (\\w+) and catalog");
    private static final Pattern BODY = Pattern.compile("\\d+\\.\\d+\\) (body: .*)");

    /** Pact's failure report is long. This keeps the consumer's name and the first line that says what differed. */
    static String summary(String message) {
        Matcher consumer = CONSUMER.matcher(message);
        Matcher body = BODY.matcher(message);
        String who = consumer.find() ? consumer.group(1) : "a consumer";
        String what = body.find() ? body.group(1).replace("$ ", "") : "did not match";
        return who + " - " + what;
    }

    public static Outcome verify(Release release) throws IOException {
        PrintStream console = System.out;
        System.setOut(new PrintStream(new ByteArrayOutputStream()));
        try (Catalog catalog = new Catalog(release)) {
            CatalogVerification.port = catalog.port();
            LauncherDiscoveryRequest request = LauncherDiscoveryRequestBuilder.request()
                    .selectors(DiscoverySelectors.selectClass(CatalogVerification.class)).build();
            Launcher launcher = LauncherFactory.create();
            List<String> problems = new ArrayList<>();
            int[] checked = {0};
            launcher.execute(request, new TestExecutionListener() {
                @Override
                public void executionFinished(TestIdentifier id, TestExecutionResult result) {
                    if (id.isTest()) {
                        checked[0]++;
                        if (result.getStatus() != TestExecutionResult.Status.SUCCESSFUL) {
                            problems.add(summary(result.getThrowable().map(Throwable::getMessage).orElse("failed")));
                        }
                    }
                }
            });
            return new Outcome(checked[0], problems);
        } finally {
            System.setOut(console);
        }
    }
}
