package com.jk.explore.tracingjaeger;

import io.opentelemetry.api.common.AttributeKey;
import io.opentelemetry.api.common.Attributes;
import io.opentelemetry.api.trace.propagation.W3CTraceContextPropagator;
import io.opentelemetry.context.propagation.ContextPropagators;
import io.opentelemetry.exporter.otlp.http.trace.OtlpHttpSpanExporter;
import io.opentelemetry.sdk.OpenTelemetrySdk;
import io.opentelemetry.sdk.common.Clock;
import io.opentelemetry.sdk.resources.Resource;
import io.opentelemetry.sdk.trace.SdkTracerProvider;
import io.opentelemetry.sdk.trace.export.BatchSpanProcessor;
import io.opentelemetry.sdk.trace.samplers.Sampler;
import java.time.Duration;
import java.util.concurrent.TimeUnit;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * One service's OpenTelemetry: its name, what it keeps, its clock, and how it sends.
 *
 * <p>Every service builds its own. Nothing here is shared between the two services, because in
 * a real system they are different programs, often written by different teams, and each one
 * reports its own spans to the collector. The collector is the only place the two meet.
 */
public final class Telemetry {

    /** How often a service sends what it has collected: every 5 seconds, OpenTelemetry's default. */
    public static final Duration BATCH_EVERY = Duration.ofSeconds(5);

    static final AttributeKey<String> SERVICE_NAME = AttributeKey.stringKey("service.name");

    static {
        // OpenTelemetry reports its own trouble through java.util.logging. A service that is
        // killed mid-batch is part of the lesson, not an error for the reader to decode, so the
        // demo says what happened itself.
        Logger.getLogger("io.opentelemetry").setLevel(Level.OFF);
    }

    private Telemetry() {
    }

    /** The settings that differ between the services and between the acts. */
    public record Settings(String serviceName, String otlpEndpoint, Sampler sampler,
                           long clockOffsetMillis, long idSeed) {

        public static Settings of(String serviceName, String otlpEndpoint, long idSeed) {
            return new Settings(serviceName, otlpEndpoint, Sampler.parentBased(Sampler.alwaysOn()), 0, idSeed);
        }

        public Settings keeping(Sampler newSampler) {
            return new Settings(serviceName, otlpEndpoint, newSampler, clockOffsetMillis, idSeed);
        }

        public Settings withClockOffBy(long millis) {
            return new Settings(serviceName, otlpEndpoint, sampler, millis, idSeed);
        }
    }

    public static OpenTelemetrySdk start(Settings settings) {
        Resource resource = Resource.getDefault()
                .merge(Resource.create(Attributes.of(SERVICE_NAME, settings.serviceName())));
        OtlpHttpSpanExporter exporter = OtlpHttpSpanExporter.builder()
                .setEndpoint(settings.otlpEndpoint())
                .build();
        SdkTracerProvider tracerProvider = SdkTracerProvider.builder()
                .setResource(resource)
                .setSampler(settings.sampler())
                .setIdGenerator(new SeededIds(settings.idSeed()))
                .setClock(new ClockOffBy(Clock.getDefault(), settings.clockOffsetMillis()))
                .addSpanProcessor(BatchSpanProcessor.builder(exporter)
                        .setScheduleDelay(BATCH_EVERY)
                        .build())
                .build();
        return OpenTelemetrySdk.builder()
                .setTracerProvider(tracerProvider)
                .setPropagators(ContextPropagators.create(W3CTraceContextPropagator.getInstance()))
                .build();
    }

    /** Sends whatever is still waiting, then stops. What a service does when it is shut down politely. */
    public static void stop(OpenTelemetrySdk sdk) {
        sdk.getSdkTracerProvider().shutdown().join(30, TimeUnit.SECONDS);
    }

    /**
     * A service clock that is wrong by a fixed amount, as a machine whose clock has drifted is.
     * The span's start time is read from this clock; its length is still measured correctly,
     * because OpenTelemetry measures a span's length with a stopwatch rather than the wall clock.
     */
    static final class ClockOffBy implements Clock {
        private final Clock real;
        private final long offsetNanos;

        ClockOffBy(Clock real, long offsetMillis) {
            this.real = real;
            this.offsetNanos = TimeUnit.MILLISECONDS.toNanos(offsetMillis);
        }

        @Override
        public long now() {
            return real.now() + offsetNanos;
        }

        @Override
        public long nanoTime() {
            return real.nanoTime();
        }
    }
}
