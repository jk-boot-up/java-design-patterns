package com.jk.explore.frontcontroller.naive;

import com.jk.explore.frontcontroller.Journal;
import com.jk.explore.frontcontroller.Request;
import com.jk.explore.frontcontroller.Response;

/**
 * Three handlers that each look after themselves: their own login check, their own logging. The orders
 * handler was written on a Friday and has neither.
 */
public class NaiveHandlers {

    private final Journal journal;

    public NaiveHandlers(Journal journal) {
        this.journal = journal;
    }

    public Response products(Request r) {
        journal.add("GET /products");
        return Response.ok("the catalogue: mug, tea, machine");
    }

    public Response orders(Request r) {
        return Response.ok("ada's orders: ORD-1, ORD-2");
    }

    public Response account(Request r) {
        if (r.token() == null) {
            return new Response(401, "please sign in");
        }
        journal.add("GET /account");
        return Response.ok("ada's account: ada@example.com");
    }
}
