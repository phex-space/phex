# FROM gradle:jdk11 AS java-build-env

# RUN apt-get update && apt-get install -y curl && apt-get install -y maven && \
#     curl -fsSL https://deb.nodesource.com/setup_lts.x | bash - && apt-get -y install nodejs && \
#     mkdir /opt/identity

# ADD ./keycloak /opt/identity/keycloak/
# RUN cd /opt/identity/keycloak && \
#     ./gradlew build

# ADD ./ui /opt/identity/keycloak-ui/
# RUN cd /opt/identity/keycloak-ui &&  \
#     npm install &&  \
#     npm run keycloak

FROM jboss/keycloak:15.1.0

USER 1000

# COPY --from=java-build-env /opt/identity/keycloak/build/libs/identity-1.0-SNAPSHOT.jar /opt/jboss/keycloak/standalone/deployments/identity-1.0-SNAPSHOT.jar
# COPY --from=java-build-env /opt/identity/keycloak-ui/build_keycloak/target/keycloak-ui-keycloak-theme-0.1.0.jar /opt/jboss/keycloak/standalone/deployments/keycloak-ui-keycloak-theme-0.1.0.jar

COPY keycloak/configuration/standalone-ha.xml /opt/jboss/keycloak/standalone/configuration/standalone-ha.xml


ENTRYPOINT [ "/opt/jboss/tools/docker-entrypoint.sh" ]
