pipeline {
    agent {
          docker {
            image 'python:3'
            label 'my-build-agent'
          }
    }

    stages {
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
        stage('setup') {
            steps {
                echo 'Setup...'
                sh """
                which python
                python --version
                python ./setup.py
                """
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying....'
            }
        }
    }
}