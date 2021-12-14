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
                ls
                python3 ./setup.py install --user
                """
            }
        }
        stage('Env') {
            steps {
                script {
                  withCredentials([
                    usernamePassword(credentialsId: 'gb_atlas_env',
                      usernameVariable: 'DB_USERNAME',
                      passwordVariable: 'DB_PASSWORD')
                  ]) {
                    print 'username=' + username + 'password=' + password
                  }
                }
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