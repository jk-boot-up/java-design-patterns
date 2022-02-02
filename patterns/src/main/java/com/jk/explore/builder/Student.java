package com.jk.explore.builder;

public class Student {
    private final String name;
    private final String id;

    private Student(Builder builder) {
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
        private String id;
        private String name;
        private Builder() {
            // private
        }
        public static Builder getInstance() {
            return new Builder();
        }

        public Builder setName(String name) {
            this.name = name;
            return this;
        }
        public Builder setId(String id) {
            this.id = id;
            return this;
        }

        public Student build() {
            return new Student(this);
        }
    }

}


