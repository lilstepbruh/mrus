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
    stage("Checkout from GitHub") {
      steps {
        git branch: "${BRANCH}", url: "${REPO_URL}"
      }
    }

    stage("Deploy to VM (docker compose)") {
      steps {
        sshagent(credentials: ['deploy-ssh']) {
          sh """
          ssh -o StrictHostKeyChecking=no ${DEPLOY_USER}@${DEPLOY_HOST} 'bash -s' <<'EOF'
            set -e
            if [ ! -d "${DEPLOY_DIR}/.git" ]; then
              git clone ${REPO_URL} ${DEPLOY_DIR}
            fi
            cd ${DEPLOY_DIR}
            git fetch --all
            git reset --hard origin/${BRANCH}

            docker compose down
            docker compose up -d --build
            docker ps
          EOF
          """
        }
      }
    }
  }
}
