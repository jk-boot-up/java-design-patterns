package com.jk.explore.valets3;

import java.net.URI;
import java.time.Duration;
import org.testcontainers.DockerClientFactory;
import org.testcontainers.localstack.LocalStackContainer;
import org.testcontainers.utility.DockerImageName;
import software.amazon.awssdk.auth.credentials.AwsBasicCredentials;
import software.amazon.awssdk.auth.credentials.StaticCredentialsProvider;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.regions.Region;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.S3Configuration;
import software.amazon.awssdk.services.s3.model.CreateBucketRequest;
import software.amazon.awssdk.services.s3.model.HeadObjectRequest;
import software.amazon.awssdk.services.s3.model.PutObjectRequest;
import software.amazon.awssdk.services.s3.presigner.S3Presigner;
import software.amazon.awssdk.services.s3.presigner.model.PutObjectPresignRequest;

/**
 * Object storage with the Amazon S3 API, played by LocalStack in a container that this demo starts and
 * stops itself. The shop holds the storage credentials; customers never do.
 */
public final class Storage implements AutoCloseable {

    /**
     * LocalStack 4.14.0. Held back on purpose: later images refuse to start without a LocalStack
     * account token, and 4.14.0 is the last one that runs without.
     */
    public static final String IMAGE = "localstack/localstack:4.14.0";
    public static final String BUCKET = "reviews";

    public static final String NO_RUNTIME_ADVICE =
            "This demo needs a container runtime, because it starts LocalStack, which plays Amazon S3.\n"
            + "Start Docker Desktop, or any Docker-compatible runtime, wait until it says it is running, and run ./gradlew run again.";

    public static final String WOULD_NOT_START_ADVICE =
            "The LocalStack container would not start. The image is " + IMAGE + ".\n"
            + "Check that the container runtime is running and can reach the internet, then run ./gradlew run again.";

    private final LocalStackContainer container = new LocalStackContainer(DockerImageName.parse(IMAGE)).withServices("s3")
            .withEnv("S3_SKIP_SIGNATURE_VALIDATION", "0");   // check presigned URLs as real S3 does
    private S3Client shop;
    private S3Presigner presigner;

    public static boolean containerRuntimeAvailable() {
        try {
            return DockerClientFactory.instance().isDockerAvailable();
        } catch (Throwable t) {
            return false;
        }
    }

    public void start() {
        container.start();
        URI endpoint = container.getEndpoint();
        StaticCredentialsProvider credentials = StaticCredentialsProvider.create(
                AwsBasicCredentials.create(container.getAccessKey(), container.getSecretKey()));
        S3Configuration pathStyle = S3Configuration.builder().pathStyleAccessEnabled(true).build();
        Region region = Region.of(container.getRegion());
        shop = S3Client.builder().endpointOverride(endpoint).credentialsProvider(credentials)
                .region(region).serviceConfiguration(pathStyle).build();
        presigner = S3Presigner.builder().endpointOverride(endpoint).credentialsProvider(credentials)
                .region(region).serviceConfiguration(pathStyle).build();
        shop.createBucket(CreateBucketRequest.builder().bucket(BUCKET).build());
    }

    /** The old way: the shop's own server writes the photo it was sent, with its own credentials. */
    public void putAsShop(String object, byte[] data) {
        shop.putObject(PutObjectRequest.builder().bucket(BUCKET).key(object).build(), RequestBody.fromBytes(data));
    }

    /**
     * A valet key: a URL signed with the shop's secret that allows one PUT, to one object, of exactly
     * {@code bytes} bytes, for a limited time.
     */
    public String presignedPut(String object, long bytes, Duration valid) {
        PutObjectRequest put = PutObjectRequest.builder().bucket(BUCKET).key(object).contentLength(bytes).build();
        return presigner.presignPutObject(PutObjectPresignRequest.builder()
                .signatureDuration(valid).putObjectRequest(put).build()).url().toString();
    }

    public String objectUrl(String object) {
        return container.getEndpoint() + "/" + BUCKET + "/" + object;
    }

    public long size(String object) {
        try {
            return shop.headObject(HeadObjectRequest.builder().bucket(BUCKET).key(object).build()).contentLength();
        } catch (RuntimeException e) {
            return -1;
        }
    }


    @Override
    public void close() {
        if (presigner != null) {
            presigner.close();
            shop.close();
        }
        container.stop();
    }
}
