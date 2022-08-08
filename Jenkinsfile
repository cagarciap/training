node {
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

    stage ("Building docker image"){
        steps {
            withCredentials([
                usernamePassword(credentials: 'perfexp-credentials-training', usernameVariable: USER, passwordVariable: PWD)
            ]){
                sh "docker build --build-arg perfexp_username=${USER} --build-arg perfexp_password=${PWD} . -t image-test" 
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
            sh "docker run -e url=ec2-3-21-207-134.us-east-2.compute.amazonaws.com -e port=8080 -e endpoint=1 -e script=load -e target_concurrency=100 -e ramp_up_time=10 -e ramp_up_steps=10 -e hold_target_rate_time=10 -d image-test"
        }
    }

    
}