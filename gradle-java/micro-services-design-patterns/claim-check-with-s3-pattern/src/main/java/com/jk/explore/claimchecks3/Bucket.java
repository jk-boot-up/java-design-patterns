package com.jk.explore.claimchecks3;

import java.util.List;
import software.amazon.awssdk.core.sync.RequestBody;
import software.amazon.awssdk.services.s3.S3Client;
import software.amazon.awssdk.services.s3.model.BucketVersioningStatus;
import software.amazon.awssdk.services.s3.model.ExpirationStatus;
import software.amazon.awssdk.services.s3.model.LifecycleRule;
import software.amazon.awssdk.services.s3.model.ListObjectVersionsResponse;
import software.amazon.awssdk.services.s3.model.ObjectVersion;
import software.amazon.awssdk.services.s3.model.PutObjectResponse;

/**
 * One bucket on Amazon S3: the left-luggage office where the invoices wait.
 *
 * <p>S3 stores a file of any size under a name, called a key, and hands it back to anyone
 * who asks with that key. A stored file is called an object. That is all the claim check
 * needs from it: somewhere big to put the luggage, and a name to fetch it by.
 */
public class Bucket {

    /** What S3 says back after storing an object. */
    public record Stored(String key, String versionId, String expiry) {
    }

    private final S3Client s3;
    private final String name;

    private Bucket(S3Client s3, String name) {
        this.s3 = s3;
        this.name = name;
    }

    public static Bucket create(S3Client s3, String name) {
        s3.createBucket(b -> b.bucket(name));
        return new Bucket(s3, name);
    }

    public String name() {
        return name;
    }

    /**
     * Asks S3 to keep every version of every object, so that storing under a key that is
     * already used adds a new version instead of replacing the old one. S3 calls this
     * versioning.
     */
    public Bucket keepEveryVersion() {
        s3.putBucketVersioning(b -> b.bucket(name).versioningConfiguration(v -> v.status(BucketVersioningStatus.ENABLED)));
        return this;
    }

    /**
     * A rule that S3 itself applies: remove every object a number of whole days after it was
     * stored. S3 calls this a lifecycle rule. Its unit is a day; there is nothing smaller.
     */
    public Bucket removeEverythingAfterDays(int days) {
        s3.putBucketLifecycleConfiguration(b -> b.bucket(name).lifecycleConfiguration(l -> l.rules(
                LifecycleRule.builder().id("remove-uncollected-invoices").status(ExpirationStatus.ENABLED)
                        .filter(f -> f.prefix("")).expiration(e -> e.days(days)).build())));
        return this;
    }

    public Stored put(String key, byte[] bytes) {
        PutObjectResponse response = s3.putObject(b -> b.bucket(name).key(key), RequestBody.fromBytes(bytes));
        return new Stored(key, response.versionId(), response.expiration());
    }

    /** The expiry S3 has stamped on a stored object, in S3's own words, or null if none. */
    public String expiryOf(String key) {
        return s3.headObject(b -> b.bucket(name).key(key)).expiration();
    }

    /** The newest version of the object under this key. */
    public byte[] get(String key) {
        return s3.getObjectAsBytes(b -> b.bucket(name).key(key)).asByteArray();
    }

    /** One exact version of the object under this key, whatever has been stored there since. */
    public byte[] get(String key, String versionId) {
        return s3.getObjectAsBytes(b -> b.bucket(name).key(key).versionId(versionId)).asByteArray();
    }

    /**
     * Deletes by key. In a bucket that keeps every version this removes nothing: it adds a
     * marker saying the key is deleted, and every stored version stays where it was.
     */
    public void delete(String key) {
        s3.deleteObject(b -> b.bucket(name).key(key));
    }

    /** Deletes one exact version, which really does remove its bytes. */
    public void delete(String key, String versionId) {
        s3.deleteObject(b -> b.bucket(name).key(key).versionId(versionId));
    }

    /** How many keys a listing shows. A key whose newest entry is a delete marker is not shown. */
    public int keysListed() {
        return s3.listObjectsV2(b -> b.bucket(name)).keyCount();
    }

    /** How many stored versions exist, listed or not. Every one of them is stored, and billed. */
    public int versionsStored() {
        return versions().versions().size();
    }

    public int deleteMarkers() {
        return versions().deleteMarkers().size();
    }

    public List<String> versionIds(String key) {
        return versions().versions().stream().filter(v -> v.key().equals(key)).map(ObjectVersion::versionId).toList();
    }

    private ListObjectVersionsResponse versions() {
        return s3.listObjectVersions(b -> b.bucket(name));
    }
}
