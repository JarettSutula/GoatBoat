pipeline {
    agent any

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
                sh """
                which python
                whoami
                rm -rf GoatBoat
                git clone https://github.com/JarettSutula/GoatBoat
                export PATH=$HOME/GoatBoat/.local/bin:$PATH
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