pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "two-tier-app-flask"
  }

  stages {
    stage('Checkout') {
      steps {
        // for multibranch or Pipeline from SCM this will use the Jenkins-provided SCM
        checkout scm
      }
    }

    stage('Build image') {
      steps {
        script {
          // build image on the host docker
          sh "docker build -t ${DOCKER_IMAGE} ."
        }
      }
    }

    stage('Deploy with Docker Compose') {
      steps {
        script {
          // stop existing and bring up new stack (rebuild)
          sh '''
            docker compose down -v || true
            docker compose up -d --build
          '''
        }
      }
    }
  }

  post {
    success {
      echo "Pipeline finished successfully."
    }
    failure {
      echo "Pipeline failed — printing docker-compose logs for debugging."
      sh 'docker compose logs --tail=200 || true'
    }
  }
}
