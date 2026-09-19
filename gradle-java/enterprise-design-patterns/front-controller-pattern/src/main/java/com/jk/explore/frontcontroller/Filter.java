package com.jk.explore.frontcontroller;

import java.util.function.Function;

/** Something that runs around every request: it may answer for the request itself, or pass it on. */
public interface Filter {
    Response apply(Request request, Function<Request, Response> next);
}
