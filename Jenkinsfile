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
                python3 ./mentor/userform/tests.py
                python3 ./mentor/formtests.py
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