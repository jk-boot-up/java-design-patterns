package com.jk.explore.valets3;

import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.junit.jupiter.api.Assumptions.assumeTrue;

import org.junit.jupiter.api.Test;

/** The whole demo against LocalStack's S3; skipped, not failed, without a container runtime. */
class DemoRunsTest {

    @Test
    void acts() throws Exception {
        assumeTrue(Storage.containerRuntimeAvailable(), "needs a container runtime");
        String all = String.join("\n", S3ValetKeyDemo.run());
        assertTrue(all.contains("the app server carried 40 MB"), all);
        assertTrue(all.contains("the browser uploads straight to S3: HTTP 200, stored 2000000 bytes"), all);
        assertTrue(all.contains("read the photo with it:      HTTP 403"), all);
        assertTrue(all.contains("upload over review R-3:      HTTP 403"), all);
        assertTrue(all.contains("a 6 MB file with the key:    HTTP 403"), all);
        assertTrue(all.contains("used after 2 s: HTTP 403"), all);
        assertTrue(all.contains("a stranger uses it: HTTP 200, stored 10 bytes"), all);
    }

    @Test
    void adviceIsASentenceNotAStackTrace() {
        assertTrue(Storage.NO_RUNTIME_ADVICE.contains("Start Docker Desktop"));
    }
}
