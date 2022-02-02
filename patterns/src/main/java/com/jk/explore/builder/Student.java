package com.jk.explore.builder;

public class Student {
    final String name;
    final String id;

    public Student(Builder builder) {
        this.name = builder.name;
        this.id = builder.id;
    }

    public String getName() {
        return name;
    }

    public String getId() {
        return id;
    }

    public static class Builder {
        String id;
        String name;
        private Builder() {
            // private
        }
        public static Builder getInstance() {
            return new Builder();
        }

        Builder setName(String name) {
            this.name = name;
            return this;
        }
        Builder setId(String id) {
            this.id = id;
            return this;
        }

        Student build() {
            return new Student(this);
        }
    }

}


