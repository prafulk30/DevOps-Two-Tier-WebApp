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
            set -e

            # prefer "docker compose" (newer CLI), fallback to docker-compose (legacy)
            if docker compose version >/dev/null 2>&1; then
              echo "Using: docker compose"
              docker compose down --volumes || true
              docker compose up --detach --build
            elif docker-compose version >/dev/null 2>&1; then
              echo "Using: docker-compose"
              docker-compose down -v || true
              docker-compose up -d --build
            else
              echo "No Compose CLI found (docker compose or docker-compose). Exiting with error."
              exit 1
            fi
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
      echo "Pipeline failed — printing compose logs (recent) for debugging."
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
