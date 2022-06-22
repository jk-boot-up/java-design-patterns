package com.jk.explore.patterns.abstractfactory;

public class BMWIndiaCarFactory implements CarFactory{

    @Override
    public Car createCar(String model) {
        if(model == "MINI") {
            return new MINICar("BMW", "India", model);
        }
        if(model == "SUV") {
            return new SUVCar("BMW", "India", model);
        }
        return null;
    }
}
