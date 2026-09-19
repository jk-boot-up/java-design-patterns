package com.jk.explore.dependencyinjection.container;

/** Needs a Chicken. Together they are a circular dependency. */
public class Egg {

    public Egg(Chicken chicken) {
    }
}
