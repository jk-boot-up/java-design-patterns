package com.jk.explore.frontcontroller;

/** Does the work for one route, and nothing else: no login check, no logging, no error handling. */
public interface Handler {
    Response handle(Request request);
}
