package com.jk.explore.tracingjaeger;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.nio.file.Path;
import java.util.concurrent.TimeUnit;

/**
 * Starts {@link RecommendationsService} as a second Java program, and stops it again, either
 * politely or by killing it.
 */
public final class RecommendationsProcess implements AutoCloseable {

    private final Process process;
    private final BufferedReader out;
    private final int port;
    private boolean finished;

    private RecommendationsProcess(Process process) {
        this.process = process;
        this.out = new BufferedReader(new InputStreamReader(process.getInputStream(), StandardCharsets.UTF_8));
        this.port = readPort();
    }

    /**
     * Starts the service.
     *
     * @param otlpEndpoint where it sends its spans
     * @param clockOffsetMillis how wrong its clock is; 0 for a correct clock
     * @param ownMillis its own work around the ranking model
     * @param rankingMillis the ranking model's work
     * @param idSeed where its span ids start
     */
    public static RecommendationsProcess start(String otlpEndpoint, long clockOffsetMillis,
                                               long ownMillis, long rankingMillis, long idSeed) {
        String java = Path.of(System.getProperty("java.home"), "bin", "java").toString();
        ProcessBuilder builder = new ProcessBuilder(java, "-cp", System.getProperty("java.class.path"),
                RecommendationsService.class.getName(), otlpEndpoint, Long.toString(clockOffsetMillis),
                Long.toString(ownMillis), Long.toString(rankingMillis), Long.toString(idSeed));
        builder.redirectErrorStream(true);
        try {
            return new RecommendationsProcess(builder.start());
        } catch (IOException e) {
            throw new IllegalStateException("could not start the recommendations service", e);
        }
    }

    private int readPort() {
        try {
            String line;
            while ((line = out.readLine()) != null) {
                if (line.startsWith("listening on port ")) {
                    return Integer.parseInt(line.substring("listening on port ".length()).trim());
                }
            }
        } catch (IOException e) {
            throw new IllegalStateException(e);
        }
        throw new IllegalStateException("the recommendations service exited before it was listening");
    }

    public String baseUrl() {
        return "http://127.0.0.1:" + port;
    }

    /** A polite stop: close its input, let it send what it holds, and wait for it to exit. */
    public void stop() {
        if (finished) {
            return;
        }
        finished = true;
        try {
            process.getOutputStream().close();
            if (!process.waitFor(60, TimeUnit.SECONDS)) {
                process.destroyForcibly();
                throw new IllegalStateException("the recommendations service did not stop");
            }
        } catch (IOException e) {
            throw new IllegalStateException(e);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            throw new IllegalStateException(e);
        }
    }

    /** A crash: the operating system ends the program at once. It sends nothing more. */
    public void kill() {
        if (finished) {
            return;
        }
        finished = true;
        process.destroyForcibly();
        try {
            process.waitFor(60, TimeUnit.SECONDS);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
        }
    }

    @Override
    public void close() {
        kill();
    }
}
