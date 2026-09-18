package com.jk.explore.sidecarjavaproxy;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.List;
import java.util.Locale;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;

/**
 * A test that reads the source rather than running it.
 *
 * <p>The claim under test is a claim about a file: the payments service carries no
 * cross-cutting code, and this project did not quietly put some back while swapping the
 * proxy. That is not something a behavioural test can check — a service could pass every
 * behavioural test here while having a retry loop nobody noticed — so this one opens
 * {@code PaymentsService.java} and looks.
 *
 * <p>It is a blunt instrument and it is meant to be. If a future change genuinely needs
 * one of these words in that file, this test failing is the conversation worth having.
 */
class ServiceStaysEmptyTest {

    private static final Path SERVICE = Path.of(
            "src/main/java/com/jk/explore/sidecarjavaproxy/PaymentsService.java");

    /** Words that would mean a concern had moved back into the service. */
    private static final List<String> FORBIDDEN =
            List.of("retry", "backoff", "keystore", "truststore", "timeout", "tls");

    @Test
    @DisplayName("the service source mentions no retrying, no backoff and no certificates")
    void theServiceCarriesNoCrossCuttingCode() throws IOException {
        String source = code(SERVICE);

        for (String word : FORBIDDEN) {
            assertTrue(!source.contains(word),
                    "PaymentsService should not mention '" + word + "'");
        }
    }

    @Test
    @DisplayName("the service never names either proxy type")
    void theServiceDoesNotKnowWhatIsNextDoor() throws IOException {
        String source = code(SERVICE);

        // The package is called sidecarjavaproxy, so look for the type names rather
        // than for the word, which would match the package declaration and prove
        // nothing either way.
        assertTrue(!source.contains("nginxproxy"));
        assertTrue(!source.contains("javaproxy("));
        assertTrue(!source.contains("proxy proxy"));
    }

    @Test
    @DisplayName("the whole program constructs a payments service exactly once")
    void thereIsOnePlaceAServiceCouldBeRestarted() throws IOException {
        long constructions = code(Path.of(
                "src/main/java/com/jk/explore/sidecarjavaproxy/ProxySwapDemo.java"))
                .lines()
                .filter(line -> line.contains("new paymentsservice("))
                .count();

        assertEquals(1, constructions);
    }

    /**
     * The file with its comments and its javadoc taken out, because the prose in this
     * project talks about retrying constantly and none of that is code.
     */
    private String code(Path path) throws IOException {
        StringBuilder kept = new StringBuilder();
        boolean inBlockComment = false;
        for (String line : Files.readAllLines(path)) {
            String trimmed = line.trim();
            if (inBlockComment) {
                inBlockComment = !trimmed.contains("*/");
                continue;
            }
            if (trimmed.startsWith("/*")) {
                inBlockComment = !trimmed.contains("*/");
                continue;
            }
            if (trimmed.startsWith("//")) {
                continue;
            }
            kept.append(line).append('\n');
        }
        return kept.toString().toLowerCase(Locale.ROOT);
    }
}
