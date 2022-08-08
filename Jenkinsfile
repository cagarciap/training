pipeline {
    agent {label 'standard-slave'}
    parameters {
        choice(name: 'TEST', choices: ['scalability', 'endurance', 'load', 'stress', 'spike'], description: 'Select a test')
        string(name: 'HOST', defaultValue: '', description: 'Host address')
        string(name: 'PORT', defaultValue: '8080', description: 'Port number')
        string(name: 'CONCURRENCY', defaultValue: '0', description: 'Target concurrecy')
        string(name: 'RAMP_UP', defaultValue: '0', description: 'Ramp up time')
        string(name: 'STEPS', defaultValue: '0', description: 'Ramp up steps')
        string(name: 'TIME', defaultValue: '0', description: 'Hold target rate time')
        choice(name: 'ENDPOINT', choices: ['0', '1', '2', '3', '4', '5'], description: 'Select a endpoint')

    }
    stages {
        stage ("Building docker image"){
            steps {
                withCredentials([
                    usernamePassword(credentialsId: "perfexp-credentials-training", usernameVariable: "USER", passwordVariable: "PWD"),
                    usernamePassword(credentialsId: "git-credentials", usernameVariable: "GIT_USR", passwordVariable: "GIT_PWD"),
                    
                ]){
                    sh """
                            docker build --build-arg git_usr=${GIT_USR} --build-arg git_pwd=${GIT_PWD} --build-arg perfexp_username=${USER} --build-arg perfexp_password=${PWD} . -t image-test 
                        """
                }
            }
        }
        stage('Run container'){
            steps {		 
                sh """
                        docker run image-test python3.7 /usr/perfexp-tutorial/prueba.py -url ${HOST} -port ${PORT} -script ${TEST} -c ${CONCURRENCY} -rt ${RAMP_UP} -rs ${STEPS} -t ${TIME} -endpoint ${ENDPOINT}
                    """
                
            }
        }
    }
}