pipeline {
  agent {
    docker {
      image 'python3:latest'
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
