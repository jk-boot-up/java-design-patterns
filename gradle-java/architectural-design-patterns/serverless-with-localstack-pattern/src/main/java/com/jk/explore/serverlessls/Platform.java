package com.jk.explore.serverlessls;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URI;
import java.time.Duration;
import java.util.function.BooleanSupplier;
import java.util.zip.ZipEntry;
import java.util.zip.ZipOutputStream;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.core.SdkBytes;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.lambda.LambdaClient;
import software.amazon.awssdk.services.lambda.model.CreateFunctionRequest;
import software.amazon.awssdk.services.lambda.model.FunctionCode;
import software.amazon.awssdk.services.lambda.model.GetFunctionRequest;
import software.amazon.awssdk.services.lambda.model.InvokeRequest;
import software.amazon.awssdk.services.lambda.model.InvokeResponse;
import software.amazon.awssdk.services.lambda.model.Runtime;
import software.amazon.awssdk.services.lambda.model.State;

/** LocalStack in Docker, which runs each Lambda copy in a real container of its own, and the SDK calls to use it. */
public class Platform implements AutoCloseable {

    public static final String IMAGE = "localstack/localstack:4.14.0";
    public static final String RUNTIME_IMAGE = "public.ecr.aws/lambda/python:3.12";
    private static final String CONTAINER = "patterns-localstack";

    /** How long a copy may sit idle before LocalStack removes it. */
    public static final int IDLE_SECONDS = 5;

    private LambdaClient lambda;

    public record Call(String body, boolean failed, long millis) {
        public String field(String name) {
            java.util.regex.Matcher m = java.util.regex.Pattern.compile("\"" + name + "\"\\s*:\\s*\"?([^\",}]+)").matcher(body);
            return m.find() ? m.group(1) : null;
        }
    }

    public static boolean toolsAvailable() {
        return Shell.works("docker", "info")
                && (Shell.works("docker", "image", "inspect", IMAGE) || Shell.works("docker", "pull", "-q", IMAGE))
                && (Shell.works("docker", "image", "inspect", RUNTIME_IMAGE) || Shell.works("docker", "pull", "-q", RUNTIME_IMAGE));
    }

    /** LocalStack starts a container for each running copy. They outlive it if it is removed, so remove them too. */
    static void removeCopies() {
        String ids = Shell.run("docker", "ps", "-aq", "--filter", "name=" + CONTAINER + "-lambda");
        for (String id : ids.split("\\s+")) {
            if (!id.isBlank()) {
                Shell.works("docker", "rm", "-f", id);
            }
        }
    }

    public void start() {
        Shell.works("docker", "rm", "-f", CONTAINER);
        removeCopies();
        Shell.run("docker", "run", "-d", "--rm", "--name", CONTAINER, "-p", "127.0.0.1:4566:4566",
                "-v", "/var/run/docker.sock:/var/run/docker.sock",
                "-e", "SERVICES=lambda", "-e", "LAMBDA_KEEPALIVE_MS=" + IDLE_SECONDS * 1000,
                IMAGE);
        lambda = LambdaClient.builder().endpointOverride(URI.create("http://127.0.0.1:4566")).region(Region.EU_WEST_2)
                .credentialsProvider(StaticCredentialsProvider.create(AwsBasicCredentials.create("test", "test"))).build();
        waitUntil(() -> {
            try {
                lambda.listFunctions();
                return true;
            } catch (Exception e) {
                return false;
            }
        }, 120);
    }

    static byte[] zipOf(String fileName, String source) throws IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        try (ZipOutputStream zip = new ZipOutputStream(out)) {
            zip.putNextEntry(new ZipEntry(fileName));
            zip.write(source.getBytes(java.nio.charset.StandardCharsets.UTF_8));
            zip.closeEntry();
        }
        return out.toByteArray();
    }

    static String handlerSource() throws IOException {
        try (InputStream in = Platform.class.getResourceAsStream("/handler.py")) {
            return new String(in.readAllBytes(), java.nio.charset.StandardCharsets.UTF_8);
        }
    }

    /** Uploads the receipt function, and waits until the platform says it is ready. */
    public void deploy(String name, int timeoutSeconds) throws IOException {
        lambda.createFunction(CreateFunctionRequest.builder().functionName(name).runtime(Runtime.PYTHON3_12).handler("handler.handler")
                .role("arn:aws:iam::000000000000:role/lambda-role").timeout(timeoutSeconds)
                .code(FunctionCode.builder().zipFile(SdkBytes.fromByteArray(zipOf("handler.py", handlerSource()))).build()).build());
        waitUntil(() -> lambda.getFunction(GetFunctionRequest.builder().functionName(name).build()).configuration().state() == State.ACTIVE, 120);
    }

    public Call invoke(String name, String payload) {
        long start = System.nanoTime();
        InvokeResponse r = lambda.invoke(InvokeRequest.builder().functionName(name).payload(SdkBytes.fromUtf8String(payload)).build());
        long millis = (System.nanoTime() - start) / 1_000_000;
        return new Call(r.payload().asUtf8String(), r.functionError() != null, millis);
    }

    /** How many copies of the function are running, counted as the containers LocalStack has started for it. */
    public int copies() {
        String out = Shell.run("docker", "ps", "--filter", "name=" + CONTAINER + "-lambda", "--format", "{{.Names}}");
        return out.isBlank() ? 0 : out.split("\n").length;
    }

    public static void waitUntil(BooleanSupplier condition, int seconds) {
        long end = System.nanoTime() + Duration.ofSeconds(seconds).toNanos();
        while (System.nanoTime() < end) {
            if (condition.getAsBoolean()) {
                return;
            }
            try {
                Thread.sleep(250);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                return;
            }
        }
        throw new IllegalStateException("the platform did not settle in " + seconds + " seconds");
    }

    @Override
    public void close() {
        if (lambda != null) {
            lambda.close();
        }
        Shell.works("docker", "rm", "-f", CONTAINER);
        removeCopies();
    }
}
