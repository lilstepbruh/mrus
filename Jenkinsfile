pipeline {
  agent any

  environment {
    DEPLOY_USER = "stepbruh"
    DEPLOY_HOST = "158.160.142.78"
    DEPLOY_DIR  = "/opt/mrus"
    REPO_URL    = "https://github.com/lilstepbruh/mrus.git"
    BRANCH      = "master"
  }

  stages {
    stage("Checkout") {
      steps {
        git branch: 'main', url: "${REPO_URL}"
      }
    }

    stage("Deploy") {
      steps {
        withCredentials([
          sshUserPrivateKey(
            credentialsId: 'deploy-ssh',
            keyFileVariable: 'SSH_KEY',
            usernameVariable: 'SSH_USER'
          )
        ]) {
          sh """
            ssh -i $SSH_KEY -o StrictHostKeyChecking=no $SSH_USER@${DEPLOY_HOST} '
              set -e
              if [ ! -d ${DEPLOY_DIR}/.git ]; then
                git clone ${REPO_URL} ${DEPLOY_DIR}
              fi
              cd ${DEPLOY_DIR}
              git fetch --all
              git reset --hard origin/master
              docker compose down
              docker compose up -d --build
            '
          """
        }
      }
    }
  }
}
