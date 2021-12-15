pipeline {
    agent any

    stages {
        stage('Setup') {
            steps {
                echo 'Setup...'
                sh """
                which python
                python3 -v
                whoami
                pwd
                python3 ./setup.py install --user
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                python3 -m coverage run ./mentor/tests_jenkins.py
                """
            }
        }
        stage('Safety Check') {
            steps {
                sh """
                python3 -m safety check -r requirements.txt
                """
            }
        }
        stage('SonarQube Analysis') {
            steps {
                def scannerHome = tool 'SonarScanner';
                withSonarQubeEnv('Goat Boat Sonar') {
                    sh "${scannerHome}/bin/sonar-scanner"
                }
            }
        }
    }
}