pipeline {
    agent any

    environment {
            MY_ENV = credentials('gb_atlas_env')
    }

    stages {
        stage('Setup') {
            steps {
                echo 'Setup...'
                sh """
                which python
                python3 -v
                whoami
                pwd
                ls
                python3 ./setup.py install --user
                """
            }
        }
        stage('Test') {
            steps {
                sh """
                echo "$MY_ENV" > .env
                ls -a
                cat .env
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