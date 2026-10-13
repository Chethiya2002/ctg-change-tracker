
pipeline {
  agent any

  environment {
    IMAGE = "chethiya02/ctg-change-tracker"
    APP_IP = "172.31.15.56"
    ANSIBLE_HOST_KEY_CHECKING = "False"
  }

  stages {
    // FR-024 checklist: change received and recorded (Git commit = evidence)
    stage('Checkout') {
      steps { checkout scm }
    }

    // FR-024: testing before release (ISO 27001 A.8.25, A.8.29)
    stage('Test') {
      steps { sh 'python3 -m pytest -v' }
    }

    // FR-024: standard build prepared
    stage('Build Image') {
      steps { sh 'docker build -t $IMAGE:$BUILD_NUMBER .' }
    }

    // Versioned image kept for rollback (previous tag)
    stage('Push Image') {
      steps {
        withCredentials([usernamePassword(credentialsId: 'dockerhub', usernameVariable: 'U', passwordVariable: 'P')]) {
          sh 'echo "$P" | docker login -u "$U" --password-stdin'
          sh 'docker push $IMAGE:$BUILD_NUMBER'
        }
      }
    }

    // FR-024: scheduled deployment (ISO 27001 A.8.9, A.8.31)
    stage('Deploy with Ansible') {
      steps {
        sh 'ansible-playbook -i inventory.ini deploy.yml -e image=$IMAGE:$BUILD_NUMBER'
      }
    }

    // FR-024: post-deployment verification
    stage('Verify') {
      steps { sh 'sleep 5; curl -f http://$APP_IP/health' }
    }
  }

  post {
    success { echo "Release $BUILD_NUMBER deployed and verified." }
    failure { echo "Release $BUILD_NUMBER failed. Previous image tag is still available for rollback." }
  }
}