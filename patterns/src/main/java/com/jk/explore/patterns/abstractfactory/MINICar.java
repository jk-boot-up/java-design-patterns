package com.jk.explore.patterns.abstractfactory;

public class MINICar implements Car {
    private final String make;
    private final String madeInCountry;
    private final String model;

    public MINICar(String make, String madeInCountry, String model) {
        this.make = make;
        this.madeInCountry = madeInCountry;
        this.model = model;
    }


    @Override
    public String getMake() {
        return make;
    }

    @Override
    public String getMadeInCountry() {
        return madeInCountry;
    }

    @Override
    public String getModel() {
        return model;
    }
}
