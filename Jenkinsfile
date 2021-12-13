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
                ls
                python3 ./setup.py install --user
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                python3 -m coverage run ./mentor/tests.py
                python3 -m coverage report -m
                """
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