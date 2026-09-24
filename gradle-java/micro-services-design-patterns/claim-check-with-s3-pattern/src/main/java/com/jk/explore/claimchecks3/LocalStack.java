package com.jk.explore.claimchecks3;

import java.util.LinkedHashMap;
import java.util.Map;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.localstack.LocalStackContainer;
import org.testcontainers.utility.DockerImageName;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.core.interceptor.Context;
import software.amazon.awssdk.core.interceptor.ExecutionAttributes;
import software.amazon.awssdk.core.interceptor.ExecutionInterceptor;
import software.amazon.awssdk.core.interceptor.SdkExecutionAttribute;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.sqs.SqsClient;

/**
 * Amazon S3 and Amazon SQS, played by LocalStack in one container that this demo starts and
 * stops itself.
 *
 * <p>LocalStack is a program that answers the same web requests the real Amazon services
 * answer, with the same limits and the same error messages, on your own machine and with no
 * account. The code in this project is ordinary AWS code: point the same clients at Amazon
 * instead and it runs unchanged.
 */
public class LocalStack implements AutoCloseable {

    /**
     * LocalStack 4.14.0. Held back on purpose: from the 2026 releases onward the image refuses
     * to start without a LocalStack account token, and 4.14.0 is the last one that runs without.
     */
    public static final String IMAGE = "localstack/localstack:4.14.0";

    /** What to say when there is no container runtime, in words a beginner can act on. */
    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts LocalStack, which plays Amazon S3 and SQS.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    /** What to say when the runtime is there but LocalStack will not come up. */
    public static final String WOULD_NOT_START_ADVICE =
            "The LocalStack container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final LocalStackContainer container =
            new LocalStackContainer(DockerImageName.parse(IMAGE)).withServices("s3", "sqs");

    /** Every request either client sends, counted by its name, such as PutObject or SendMessage. */
    private final Map<String, Integer> requests = new LinkedHashMap<>();

    private S3Client s3;
    private SqsClient sqs;

    /**
     * True when there is a container runtime this demo can use. Checked before anything
     * starts, so a machine without one gets a sentence rather than a stack trace.
     */
    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container.start();
        StaticCredentialsProvider credentials = StaticCredentialsProvider.create(
                AwsBasicCredentials.create(container.getAccessKey(), container.getSecretKey()));
        ExecutionInterceptor counter = new ExecutionInterceptor() {
            @Override
            public void afterExecution(Context.AfterExecution context, ExecutionAttributes attributes) {
                count(attributes.getAttribute(SdkExecutionAttribute.OPERATION_NAME));
            }
        };
        s3 = S3Client.builder()
                .endpointOverride(container.getEndpoint())
                .region(Region.of(container.getRegion()))
                .credentialsProvider(credentials)
                // LocalStack serves every bucket from one address, so the bucket goes in the path.
                .forcePathStyle(true)
                .overrideConfiguration(c -> c.addExecutionInterceptor(counter))
                .build();
        sqs = SqsClient.builder()
                .endpointOverride(container.getEndpoint())
                .region(Region.of(container.getRegion()))
                .credentialsProvider(credentials)
                .overrideConfiguration(c -> c.addExecutionInterceptor(counter))
                .build();
    }

    private synchronized void count(String operation) {
        requests.merge(operation, 1, Integer::sum);
    }

    public S3Client s3() {
        return s3;
    }

    public SqsClient sqs() {
        return sqs;
    }

    /** Forgets every request counted so far. */
    public synchronized void resetCount() {
        requests.clear();
    }

    /** The requests sent since the last reset, by name, in the order each was first sent. */
    public synchronized Map<String, Integer> requests() {
        return new LinkedHashMap<>(requests);
    }

    public synchronized int requestTotal() {
        return requests.values().stream().mapToInt(Integer::intValue).sum();
    }

    @Override
    public void close() {
        if (s3 != null) {
            s3.close();
        }
        if (sqs != null) {
            sqs.close();
        }
        container.stop();
    }
}
