pipeline {
  agent {
    docker {
      image 'python:3.6'
    }
  }

  stages {
    stage('Build') {
      steps {
        sh 'python setup.py install'
      }
    }
    stage('Test') {
      steps {
        echo 'you suck, there\'s no tests'
      }
    }
  }
}
