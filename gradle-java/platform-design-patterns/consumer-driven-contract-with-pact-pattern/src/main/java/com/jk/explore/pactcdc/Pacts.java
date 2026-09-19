package com.jk.explore.pactcdc;

import au.com.dius.pact.consumer.ConsumerPactBuilder;
import au.com.dius.pact.consumer.MockServer;
import au.com.dius.pact.consumer.PactTestRun;
import au.com.dius.pact.consumer.PactVerificationResult;
import au.com.dius.pact.consumer.dsl.LambdaDsl;
import au.com.dius.pact.consumer.model.MockProviderConfig;
import au.com.dius.pact.core.model.PactSpecVersion;
import au.com.dius.pact.core.model.RequestResponsePact;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.function.Function;

/**
 * Each consumer writes down what it reads, with Pact's consumer DSL. Pact then runs the consumer's own
 * client against a mock of the catalog to check that the consumer really behaves that way, and writes
 * the pact file that the provider will be verified against.
 */
public class Pacts {

    public static final Path FOLDER = Path.of("build", "pacts");

    /** checkout reads sku, a string, and priceCents, an integer. */
    static RequestResponsePact checkout() {
        return ConsumerPactBuilder.consumer("checkout").hasPactWith("catalog")
                .uponReceiving("checkout asks for the price of a mug")
                .path("/prices/MUG").method("GET")
                .willRespondWith().status(200).headers(java.util.Map.of("Content-Type", "application/json"))
                .body(LambdaDsl.newJsonBody(b -> b.stringType("sku", "MUG").integerType("priceCents", 1600)).build())
                .toPact();
    }

    /** reports reads only sku. */
    static RequestResponsePact reports() {
        return ConsumerPactBuilder.consumer("reports").hasPactWith("catalog")
                .uponReceiving("reports asks for the sku of a mug")
                .path("/prices/MUG").method("GET")
                .willRespondWith().status(200).headers(java.util.Map.of("Content-Type", "application/json"))
                .body(LambdaDsl.newJsonBody(b -> b.stringType("sku", "MUG")).build())
                .toPact();
    }

    /** Runs the consumer's real client against Pact's mock, and, if it agrees, writes the pact file. */
    public static boolean write(RequestResponsePact pact, Function<String, Boolean> consumerCode) throws IOException {
        Files.createDirectories(FOLDER);
        PactVerificationResult result = au.com.dius.pact.consumer.ConsumerPactRunnerKt.runConsumerTest(pact,
                MockProviderConfig.createDefault(PactSpecVersion.V3), (PactTestRun<Boolean>) (MockServer server, au.com.dius.pact.consumer.PactTestExecutionContext ctx) ->
                        consumerCode.apply(server.getUrl()));
        boolean ok = result instanceof PactVerificationResult.Ok;
        if (ok) {
            pact.write(FOLDER.toString(), PactSpecVersion.V3);
        }
        return ok;
    }

    public static boolean writeBoth() throws IOException {
        boolean a = write(checkout(), url -> new CheckoutClient(url).total("MUG", 1) == 1600);
        boolean b = write(reports(), url -> "MUG".equals(new ReportsClient(url).skuOf("MUG")));
        return a && b;
    }

    public static File file(String consumer) {
        return FOLDER.resolve(consumer + "-catalog.json").toFile();
    }

    private static final java.util.regex.Pattern RULE = java.util.regex.Pattern.compile("\"\\$\\.(\\w+)\"\\s*:\\s*\\{[^}]*?\"match\"\\s*:\\s*\"(\\w+)\"");

    /** What a pact file says its consumer reads: each field, and the type it must have. */
    public static java.util.Map<String, String> expectations(String consumer) throws IOException {
        java.util.Map<String, String> fields = new java.util.TreeMap<>();
        java.util.regex.Matcher m = RULE.matcher(Files.readString(file(consumer).toPath()));
        while (m.find()) {
            fields.put(m.group(1), m.group(2).equals("type") ? "string" : m.group(2));
        }
        return fields;
    }
}
