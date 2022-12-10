pipeline {
  agent {
    docker {
      image 'python:3.6'
      args '-u root:sudo'
    }
  }

  stages {
    stage('Install') {
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
