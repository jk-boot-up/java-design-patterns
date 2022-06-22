package com.jk.explore.patterns.abstractfactory;

public abstract class AbstractCarFactory {

    CarFactory getCarFactory(String make, String madeInCountry) {
        if(make == "BMW") {
            if(madeInCountry == "INDIA") {
                return new BMWIndiaCarFactory();
            } else if(madeInCountry == "USA") {
                return new BMWUSCarFactory();
            }
        }
        if(make == "AUDI") {
            if(madeInCountry == "INDIA") {
                return new AUDIIndiaCarFactory();
            } else if(madeInCountry == "USA") {
                return new AUDIUSCarFactory();
            }
        }
        return null;
    }

}
