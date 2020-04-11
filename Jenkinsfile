pipeline {
    agent { docker { image 'python' } }
    environment{
        SECRET_KEY = credentials('jenkins-rsd-secret-key')
        POSTGRES_USER = credentials('jenkins-rsd-postgres-user')
        POSTGRES_PASSWORD = credentials('jenkins-rsd-postgres-password')
    }
    stages {
        stage('test'){
            steps{
                sh 'python manage.py testserver'
            }
        }
        stage('deploy'){

        }
    }
}