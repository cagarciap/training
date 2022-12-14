FROM ubuntu:18.04

WORKDIR /test
RUN mkdir /usr/perfexp-tutorial
COPY . /usr/perfexp-tutorial 

RUN apt-get update && apt-get install -y python3.7 python3-pip git wget unzip curl

ARG perfexp_username
ARG perfexp_password
ARG git_usr
ARG git_pwd

RUN python3.7 -m pip install --no-cache-dir --upgrade git+https://$git_usr:$git_pwd@github.com/pslcorp/psl-performance-cli@v1.14.0#egg=psl-perfexp

RUN psl-perfexp configure -url "https://api.performance-explorer.psl.xyz" -usr $perfexp_username -pass $perfexp_password
RUN psl-perfexp login

RUN apt-get install -y openjdk-8-jdk && \
    apt-get install -y ant && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/oracle-jdk8-installer;

RUN apt-get update && \
    apt-get install -y ca-certificates-java && \
    apt-get clean && \
    update-ca-certificates -f && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /var/cache/oracle-jdk8-installer;


ENV JAVA_HOME /usr/lib/jvm/java-8-openjdk-amd64/

RUN export JAVA_HOME
RUN wget https://downloads.apache.org//jmeter/binaries/apache-jmeter-5.5.zip
RUN unzip apache-jmeter-5.5.zip
RUN mv apache-jmeter-5.5 jmeter
RUN rm apache-jmeter-5.5.zip
RUN cd /test/jmeter/lib/
RUN wget http://search.maven.org/remotecontent?filepath=kg/apc/cmdrunner/2.2/cmdrunner-2.2.jar -O cmdrunner-2.2.jar
RUN cd /test/jmeter/lib/ext/
RUN curl -O https://repo1.maven.org/maven2/kg/apc/jmeter-plugins-manager/1.6/jmeter-plugins-manager-1.6.jar
RUN mv /test/cmdrunner-2.2.jar /test/jmeter/lib/
RUN mv jmeter-plugins-manager-1.6.jar /test/jmeter/lib/ext/
RUN java -cp /test/jmeter/lib/ext/jmeter-plugins-manager-1.6.jar org.jmeterplugins.repository.PluginManagerCMDInstaller

RUN /test/jmeter/bin/PluginsManagerCMD.sh install-for-jmx /usr/perfexp-tutorial/load_test.jmx
RUN /test/jmeter/bin/PluginsManagerCMD.sh install-for-jmx /usr/perfexp-tutorial/stress_test.jmx
RUN /test/jmeter/bin/PluginsManagerCMD.sh install-for-jmx /usr/perfexp-tutorial/spike_test.jmx
RUN /test/jmeter/bin/PluginsManagerCMD.sh install-for-jmx /usr/perfexp-tutorial/endurance_test.jmx

CMD 