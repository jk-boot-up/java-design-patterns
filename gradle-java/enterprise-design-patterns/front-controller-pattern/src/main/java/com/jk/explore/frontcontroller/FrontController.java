package com.jk.explore.frontcontroller;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.function.Function;

/**
 * The one entry point. Every request comes here first. It runs the filters, then finds the handler in
 * a routing table, and it turns a failure into an answer that says nothing it should not. What a request
 * needs before it reaches a handler is written once, here, and cannot be forgotten by a new handler.
 */
public class FrontController {

    private final Map<String, Map<String, Handler>> routes = new HashMap<>();
    private final List<Filter> filters = new ArrayList<>();
    private final Journal journal;

    public FrontController(Journal journal) {
        this.journal = journal;
    }

    public FrontController route(String method, String path, Handler handler) {
        routes.computeIfAbsent(path, p -> new HashMap<>()).put(method, handler);
        return this;
    }

    public FrontController filter(Filter filter) {
        filters.add(filter);
        return this;
    }

    public Response handle(Request request) {
        Function<Request, Response> chain = this::dispatch;
        for (int i = filters.size() - 1; i >= 0; i--) {
            Filter filter = filters.get(i);
            Function<Request, Response> next = chain;
            chain = r -> filter.apply(r, next);
        }
        try {
            return chain.apply(request);
        } catch (RuntimeException e) {
            journal.add("error on " + request.path() + ": " + e.getMessage());
            return new Response(500, "something went wrong");
        }
    }

    private Response dispatch(Request request) {
        Map<String, Handler> byMethod = routes.get(request.path());
        if (byMethod == null) {
            return new Response(404, "no such page");
        }
        Handler handler = byMethod.get(request.method());
        if (handler == null) {
            return new Response(405, "method not allowed");
        }
        return handler.handle(request);
    }

    /** The filters the store wants on every request: log it, then check who is asking. */
    public static FrontController forTheStore(Journal journal) {
        return new FrontController(journal)
                .filter(Filters.logging(journal))
                .filter(Filters.authentication(java.util.Set.of("/products")))
                .route("GET", "/products", Handlers.products())
                .route("GET", "/orders", Handlers.orders())
                .route("GET", "/account", Handlers.account())
                .route("GET", "/broken", Handlers.faulty());
    }
}
