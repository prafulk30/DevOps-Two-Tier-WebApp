pipeline {
  agent any

  environment {
    DOCKER_IMAGE = "two-tier-app-flask"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build image') {
      steps {
        script {
          sh "docker build -t ${DOCKER_IMAGE} ."
        }
      }
    }

    stage('Deploy with Docker Compose') {
      steps {
        script {
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
      echo "Pipeline failed — printing docker-compose logs (most recent 200 lines) for debugging."
      sh '''
        set -e
        if docker compose version >/dev/null 2>&1; then
          docker compose logs 2>/dev/null | tail -n 200 || true
        elif docker-compose version >/dev/null 2>&1; then
          docker-compose logs 2>/dev/null | tail -n 200 || true
        else
          echo "No compose CLI available; skipping logs"
        fi
      '''
    }
  }
}
