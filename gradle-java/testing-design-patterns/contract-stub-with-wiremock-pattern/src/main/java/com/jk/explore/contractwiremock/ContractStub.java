package com.jk.explore.contractwiremock;

import static com.github.tomakehurst.wiremock.client.WireMock.aResponse;
import static com.github.tomakehurst.wiremock.client.WireMock.anyUrl;
import static com.github.tomakehurst.wiremock.client.WireMock.equalToJson;
import static com.github.tomakehurst.wiremock.client.WireMock.post;
import static com.github.tomakehurst.wiremock.client.WireMock.urlEqualTo;
import static com.github.tomakehurst.wiremock.core.WireMockConfiguration.wireMockConfig;

import com.github.tomakehurst.wiremock.WireMockServer;

/**
 * Real WireMock stub servers. One is built from the contract, one interaction per stub, and answers
 * nothing else. The other is the hand-written stub the checkout team once wrote: it approves anything.
 */
public final class ContractStub implements AutoCloseable {

    private final WireMockServer server = new WireMockServer(wireMockConfig().dynamicPort());

    private ContractStub() {
        server.start();
    }

    /** A stub made from the contract. */
    public static ContractStub fromContract(Contract contract) {
        ContractStub stub = new ContractStub();
        for (Contract.Interaction i : contract.interactions()) {
            stub.server.stubFor(post(urlEqualTo(i.url()))
                    .withRequestBody(equalToJson(i.requestBody()))
                    .willReturn(aResponse().withStatus(i.status()).withHeader("Content-Type", "application/json")
                            .withBody(i.responseBody())));
        }
        return stub;
    }

    /** Before: written once from the payment docs, never checked again. */
    public static ContractStub handWritten() {
        ContractStub stub = new ContractStub();
        stub.server.stubFor(post(anyUrl()).willReturn(aResponse().withStatus(200)
                .withHeader("Content-Type", "application/json").withBody("{\"result\":\"APPROVED\",\"reason\":\"\"}")));
        return stub;
    }

    public String url() {
        return server.baseUrl();
    }

    @Override
    public void close() {
        server.stop();
    }
}
