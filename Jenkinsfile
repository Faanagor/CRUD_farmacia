pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                sh 'poetry install'
            }
        }
        stage('Test') {
            steps {
                sh 'pytest --cov=app tests/'
            }
        }
        stage('Dockerize') {
            steps {
                sh 'docker build -t pharmacy-crud .'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}
