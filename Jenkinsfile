podTemplate(yaml:  """
apiVersion: v1
kind: Pod
spec:
  containers:
  - name: python
    image: python:3
    commnad: ['cat']
    tty: true
  - name: kubectl
    image: lachlanevenson/k8s-kubectl:v1.14.0 # use a version that matches your K8s version
    command: ['cat']
    tty: true
  - name: docker
    image: docker:latest
    command: ['cat']
    tty: true
    volumeMounts:
    - name: dockersock
      mountPath: /var/run/docker.sock
  nodeSelector:
    kubernetes.io/arch: amd64
  volumes:
  - name: dockersock
    hostPath:
      path: /var/run/docker.sock
 """
 ) {
  node(POD_LABEL) {
    def CONTAINER_REGISTRY = "docker.local.pw10n.pw"
    def SERVICE_CONTAINER_NAME = "ec2manager"
    def STATICASSETS_CONTAINER_NAME = "ec2manager-staticassets"

    def serviceImageName = "$CONTAINER_REGISTRY/$SERVICE_CONTAINER_NAME" 
    def serviceImageVersionTag = "$serviceImageName:$BUILD_NUMBER"
    def staticassetsImageName = "$CONTAINER_REGISTRY/$STATICASSETS_CONTAINER_NAME" 
    def staticassetsImageVersionTag = "$staticassetsImageName:$BUILD_NUMBER"

    stage("checkout") {
      checkout scm
    }

    stage("collect staticassets"){
        container('python'){
            sh('make install-requirements')
            sh('make staticassets')
        }
    }

    def serviceImage
    def staticassetsImage
    
    stage("build image") {
      container('docker'){
        serviceImage = docker.build(serviceImageVersionTag, "-f build/service/Dockerfile .")
        staticassetsImage = docker.build(staticassetsImageVersionTag, "-f build/staticassets/Dockerfile .")
      }
    }

    stage("create deploy config"){
      sh('cat deploy/config.yaml.template | sed "s/{{BUILD_NUMBER}}/$BUILD_NUMBER/g" > deploy/config.yaml')
      sh('cat deploy/deploy.yaml.template | sed "s/{{BUILD_NUMBER}}/$BUILD_NUMBER/g" > deploy/deploy.yaml')
    }

    if (env.BRANCH_NAME == "main"){
      stage("push image") {
        container('docker'){
          serviceImage.push()
          staticassetsImage.push()
          serviceImage.push('latest')
          staticassetsImage.push('latest')
        }
      }
      stage("deploy") {
        container('kubectl') {
          sh('kubectl apply -f deploy/config.yaml')
          sh('kubectl apply -f deploy/deploy.yaml')
        }
      }
    }

  }
}