package com.jk.explore.locatorconsul;

import com.jk.explore.locatorconsul.consul.Address;
import com.jk.explore.locatorconsul.gateway.ServiceInstance;
import com.jk.explore.locatorconsul.nginx.NginxFront;
import org.junit.jupiter.api.Assumptions;
import org.junit.jupiter.api.Test;

import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.List;

import static org.junit.jupiter.api.Assertions.assertEquals;

/** Runs a real nginx container. Skipped, not failed, when Docker or the nginx image is not available. */
class NginxServerSideDiscoveryTest {

    private static boolean ok(HttpClient http, String url) throws Exception {
        return http.send(HttpRequest.newBuilder(URI.create(url + "/charge?pence=9000")).build(),
                HttpResponse.BodyHandlers.ofString()).statusCode() == 200;
    }

    @Test
    void theCallerIsGivenOneAddressAndSurvivesAnInstanceDying() throws Exception {
        Assumptions.assumeTrue(NginxFront.available(), "docker or the nginx image is not available");
        try (ServiceInstance a = new ServiceInstance("a"); ServiceInstance b = new ServiceInstance("b");
             NginxFront nginx = NginxFront.start(List.of(new Address("127.0.0.1", a.port()), new Address("127.0.0.1", b.port())))) {
            HttpClient http = HttpClient.newHttpClient();
            for (int i = 0; i < 4; i++) {
                assertEquals(true, ok(http, nginx.url()));
            }
            assertEquals(2, a.hits());
            assertEquals(2, b.hits());
            a.stop();
            int before = b.hits();
            for (int i = 0; i < 4; i++) {
                assertEquals(true, ok(http, nginx.url()));
            }
            assertEquals(4, b.hits() - before, "nginx retried the surviving instance every time");
        }
    }
}
