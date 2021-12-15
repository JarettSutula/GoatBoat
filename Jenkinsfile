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
                withSonarQubeEnv('Goat Boat Sonar') {
                    sh "/bitnami/jenkins/home/tools/hudson.plugins.sonar.SonarRunnerInstallation/SonarQubeScanner/sonar-scanner-4.6.2.2472-linux/bin/sonar-scanner -Dsonar.projectKey=Goat-Boat"
                }
            }
        }
    }
}