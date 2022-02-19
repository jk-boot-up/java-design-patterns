package com.jk.explore.patterns.abstractfactory;

public class AUDIUSCarFactory implements CarFactory {

    @Override
    public Car createCar(String model) {
        if(model == "MINI") {
            return new MINICar("AUDI", "India", model);
        }
        if(model == "SUV") {
            return new SUVCar("AUDI", "India", model);
        }
        return null;
    }
}
