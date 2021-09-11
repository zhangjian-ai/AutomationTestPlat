pipeline {
    agent any
    options {
        disableConcurrentBuilds()
    }
    environment {
        PATH = "$PATH:/usr/local/bin"
    }
    stages {
        stage("close container") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================关闭老版本容器=================="
                    sh script: "docker-compose down"
                }
            }
        }
        stage("clean environment") {
            steps {
                // 当前stage报错时，设置构建结果为成功，保证后续stage继续执行
                catchError(buildResult: 'SUCCESS', stageResult: 'FAILURE'){
                    echo "==================清理环境=================="
                    sh script: "docker rmi \$(docker images | grep 'none' | awk '{print \$3}')"
                    sh script: "docker stop \$(docker ps -a | grep 'Exited' | awk '{print \$1 }')"
                    sh script: "docker rm \$(docker ps -a | grep 'Exited' | awk '{print \$1 }')"
                }
                echo "==================拷贝redis.conf到挂载目录=================="
                // 在子目构建时，要用&&链接cd 的命令，因为每一个sh执行完之后，都会回到默认工作目录
                sh script: "cp redis.conf /var/local/test_plat/redis/conf/redis.conf"
            }
        }
        stage("build images") {
            steps {
                echo "==================构建镜像=================="
                // 在子目构建时，要用&&链接cd 的命令，因为每一个sh执行完之后，都会回到默认工作目录
                sh label: "构建镜像", script: "cd backend && docker build -t backend:latest ."

                echo "==================构建前端服务器=================="
                sh label: "构建镜像", script: "cd frontend && docker build -t frontend:latest ."
            }
        }
        stage("start service") {
            steps {
                echo "==================启动容器=================="
                sh script: "docker-compose up -d"
            }
        }
    }
}
