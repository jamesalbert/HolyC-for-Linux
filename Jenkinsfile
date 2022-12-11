pipeline {
  agent {
    docker {
      image 'python:3.6'
      args '-u root:sudo'
    }
  }

  stages {
    stage('Build') {
      steps {
        sh 'python setup.py install'
      }
    }
    stage('Deploy') {
      steps {
        sh 'aws ecs deploy'
      }
    }
  }
}
