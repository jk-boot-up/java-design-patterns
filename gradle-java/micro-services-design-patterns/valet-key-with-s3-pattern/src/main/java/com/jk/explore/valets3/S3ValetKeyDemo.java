package com.jk.explore.valets3;

import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

/**
 * The five acts, against the S3 API, played by LocalStack, started and stopped by this program.
 */
public final class S3ValetKeyDemo {

    public static void main(String[] args) throws Exception {
        if (!Storage.containerRuntimeAvailable()) {
            System.out.println(Storage.NO_RUNTIME_ADVICE);
            return;
        }
        for (String line : run()) {
            System.out.println(line);
        }
    }

    /** Every line the demo prints, so the tests can check each one. */
    public static List<String> run() throws Exception {
        List<String> out = new ArrayList<>();
        try (Storage storage = new Storage()) {
            try {
                storage.start();
            } catch (RuntimeException e) {
                out.add(Storage.WOULD_NOT_START_ADVICE);
                return out;
            }
            Browser browser = new Browser();
            byte[] photo = new byte[2_000_000];

            out.add("ONE. Review photos carried through the shop's app server.");
            long carried = 0;
            for (int i = 1; i <= 10; i++) {
                carried += photo.length;                     // in from the customer
                storage.putAsShop("R-" + i + "/photo.jpg", photo);
                carried += photo.length;                     // out to the storage
            }
            out.add("  10 customers upload a 2 MB photo each: the app server carried " + carried / 1_000_000 + " MB");

            out.add("");
            out.add("TWO. A valet key: a presigned URL for one PUT.");
            String key = storage.presignedPut("R-11/photo.jpg", photo.length, Duration.ofMinutes(5));
            int status = browser.put(key, photo);
            out.add("  the shop signs: PUT reviews/R-11/photo.jpg, exactly 2000000 bytes, for 5 minutes");
            out.add("  the browser uploads straight to S3: HTTP " + status + ", stored " + storage.size("R-11/photo.jpg") + " bytes");
            out.add("  the app server carried " + (key.length() < 2000 ? "under 2 KB" : "more than 2 KB") + ": just the key");

            out.add("");
            out.add("THREE. The key allows that, and nothing else.");
            out.add("  read the photo with it:      HTTP " + browser.get(key));
            out.add("  upload over review R-3:      HTTP " + browser.put(key.replace("R-11", "R-3"), photo));
            out.add("  a 6 MB file with the key:    HTTP " + browser.put(key, new byte[6_000_000]));
            out.add("  no signature at all:         HTTP " + browser.put(storage.objectUrl("R-12/photo.jpg"), new byte[10])
                    + " here; LocalStack does not enforce bucket permissions, real S3 refuses it with 403");

            out.add("");
            out.add("FOUR. The key runs out.");
            String shortKey = storage.presignedPut("R-14/photo.jpg", 10, Duration.ofSeconds(1));
            long signedAt = System.currentTimeMillis();
            while (System.currentTimeMillis() - signedAt < 2_000) {
                Thread.onSpinWait();   // the only wait here is the clock itself running past the expiry
            }
            out.add("  a key valid for 1 s, used after 2 s: HTTP " + browser.put(shortKey, new byte[10]));

            out.add("");
            out.add("FIVE. The bill: whoever holds the key can use it.");
            String leaked = storage.presignedPut("R-15/photo.jpg", 10, Duration.ofMinutes(5));
            out.add("  the key is pasted into a public chat; a stranger uses it: HTTP " + browser.put(leaked, new byte[10])
                    + ", stored " + storage.size("R-15/photo.jpg") + " bytes");
            out.add("  it works until it expires: keep keys short-lived and narrow, keep them out of logs,");
            out.add("  and sign with credentials that can be revoked if one leaks");
        }
        return out;
    }

    private S3ValetKeyDemo() {
    }
}
