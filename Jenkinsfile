pipeline {
    agent { label 'django-blog-api-ec2' }
    stages {
        stage('build') {
            steps {
                sh 'cd /home/ubuntu/jenkins/workspace/django-blog-api_main'
                sh 'sudo apt install python3-virtualenv'
                sh 'sudo apt update'
                sh '. env/bin/activate'
                sh 'pip install -r requirements.txt'
            }
        }
        stage('tesing') {
            steps {
                sh 'cd /home/ubuntu/jenkins/workspace/django-blog-api_main'
                sh '. env/bin/activate'
                sh 'python3 manage.py makemigrations'
                sh 'python3 manage.py migrate --run-syncdb'
                sh 'python3 manage.py collectstatic --noinput'
                sh 'python3 manage.py test'
            }
        }
        stage('deploy') {
            steps {
                sh 'sudo service nginx restart'
                sh 'sudo service gunicorn restart'
            }
        }
    }
}