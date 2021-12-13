pipeline {
    agent any

    stages {
        stage('setup') {
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
        stage('test') {
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
        stage('Build') {
            steps {
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo 'Testing..'
            }
        }


        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}