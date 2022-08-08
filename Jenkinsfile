pipeline {
    agent {label 'standard-slave'}
    parameters {
        choice(name: 'TEST', choices: ['scalability', 'endurance', 'load', 'stress', 'spike'], description: 'Select a test')
        string(name: 'URL', defaultValue: '', description: 'Url')
        string(name: 'PORT', defaultValue: '8080', description: 'Port')
        string(name: 'CONCURRENCY', defaultValue: '0', description: 'Target concurrecy')
        string(name: 'RAMP_UP', defaultValue: '0', description: 'Ramp up time')
        string(name: 'STEPS', defaultValue: '0', description: 'Ramp up steps')
        string(name: 'TIME', defaultValue: '0', description: 'Hold target rate time')
        choice(name: 'ENDPOINT', choices: ['0', '1', '2', '3', '4', '5'], description: 'Select a endpoint')

    }

    stages{
        stage ("Building docker image"){
            steps {
                withCredentials([
                    usernamePassword(credentialsId: 'perfexp-credentials-training', usernameVariable: "USER", passwordVariable: "PWD"),
                    usernamePassword(credentialsId: 'git-credentials', usernameVariable: "GIT_USER", passwordVariable: "GIT_PASS")
                ]){
                    echo "User ${USER}"
                    echo "Pass ${PWD}"
                    sh "docker build --build-arg git_user=${GIT_USER} --build-arg git_pass=${GIT_PASS} --build-arg perfexp_username=${USER} --build-arg perfexp_password=${PWD} . -t image-test" 
                }
            }
        }

        stage('Run container'){
            steps {	
                echo "${URL}"
                echo "${TEST}"
                echo "${PORT}"
                echo "${CONCURRENCY}"
                echo "${RAMP_UP}"
                echo "${STEPS}"
                echo "${TIME}"
                echo "${ENDPOINT}"
                sh "docker run -d image-test python3.7 /usr/perfexp-tutorial/prueba.py ${URL} ${PORT} ${ENDPOINT} ${TEST} ${CONCURRENCY} ${RAMP_UP} ${STEPS} ${TIME}"
            }
        }
    } 
}