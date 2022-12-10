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
    stage('Test') {
      steps {
        sh 'python -m unittest tests/test_char.py'
      }
    }
  }
}
