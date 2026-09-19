# One JRE, and Tier 1's compiled classes. demo.sh compiles them first, so a reader
# waiting for a container learns about routing, not about Gradle.
FROM eclipse-temurin:21-jre-alpine
WORKDIR /app
COPY build/classes /app/classes
ENTRYPOINT ["java", "-cp", "/app/classes", "com.jk.explore.stranglerfig.real.ServiceMain"]
