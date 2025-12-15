pipeline {
  agent any

  environment {
    DEPLOY_HOST = "158.160.214.225"
    DEPLOY_DIR  = "/opt/mrus"
    REPO_URL    = "https://github.com/lilstepbruh/mrus.git"
    BRANCH      = "master"
  }

  stages {

    stage("Checkout (CI)") {
      steps {
        git branch: "${BRANCH}", url: "${REPO_URL}"
      }
    }

    stage("Deploy to VM") {
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
                echo ">>> First deploy: cloning repo"
                git clone ${REPO_URL} ${DEPLOY_DIR}
              fi

              cd ${DEPLOY_DIR}

              echo ">>> Updating code"
              git fetch origin
              git reset --hard origin/${BRANCH}

              echo ">>> Docker compose deploy"
              docker compose down
              docker compose up -d --build
            '
          """
        }
      }
    }
  }
}
