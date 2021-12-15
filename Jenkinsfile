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
                sh '''
                python3 -m coverage run ./mentor/tests_jenkins.py
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}