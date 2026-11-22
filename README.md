# 100 Days of DevOps Learning Challenge

![Days](https://img.shields.io/badge/days-50%2F100-blue)
![Last Updated](https://img.shields.io/badge/last%20updated-Nov%202026-informational)
![Stack](https://img.shields.io/badge/stack-Linux%20%7C%20K8s%20%7C%20AWS%20%7C%20CI%2FCD-orange)

Daily hands-on DevOps practice log — one topic a day, documented as I go. Each file covers the task, the commands used, and what actually broke along the way.

---

## Index

<!-- INDEX_START -->
| Day | Topic | Category | Date | Link |
|-----|-------|----------|------|------|
| 01 | Linux User Setup with Non-Interactive Shell | Linux / User Management | 2026-11-22 | [day-01-linux-user-non-interactive-shell.md](./day-01-linux-user-non-interactive-shell.md) |
| 02 | Temporary User Setup with Expiry | Linux / User Management | 2026-11-22 | [day-02-temporary-user-setup-with-expiry.md](./day-02-temporary-user-setup-with-expiry.md) |
| 03 | Secure Root SSH Access | Linux / Security | 2026-11-22 | [day-03-secure-root-ssh-access.md](./day-03-secure-root-ssh-access.md) |
| 04 | File Permissions - Making a Script Executable for All Users | Linux / File Permissions | 2026-09-15 | [day-04-file-permissions-executable.md](./day-04-file-permissions-executable.md) |
| 05 | SELinux Installation and Configuration | Linux / Security | 2026-09-15 | [day-05-selinux-configuration.md](./day-05-selinux-configuration.md) |
| 06 | Create a Cron Job | Linux / Scheduling | 2026-09-21 | [day-06-create-cron-job.md](./day-06-create-cron-job.md) |
| 07 | Linux SSH Authentication | Linux / Networking | 2026-09-21 | [day-07-linux-ssh-authentication.md](./day-07-linux-ssh-authentication.md) |
| 08 | Install Ansible | Automation / Configuration Management | 2026-09-21 | [day-08-install-ansible.md](./day-08-install-ansible.md) |
| 09 | MariaDB Troubleshooting | Linux / Databases / Troubleshooting | 2026-09-27 | [day-09-mariadb-troubleshooting.md](./day-09-mariadb-troubleshooting.md) |
| 10 | Linux Bash Scripts | Linux / Bash Scripting | 2026-09-21 | [day-10-linux-bash-scripts.md](./day-10-linux-bash-scripts.md) |
| 11 | Install and Configure Tomcat Server | Linux / Application Servers | 2026-09-25 | [day-11-install-configure-tomcat.md](./day-11-install-configure-tomcat.md) |
| 12 | Linux Network Services | Linux / Networking | 2026-09-27 | [day-12-linux-network-services.md](./day-12-linux-network-services.md) |
| 13 | IPtables Installation And Configuration | Linux / Security / Networking | 2026-09-27 | [day-13-iptables-installation-configuration.md](./day-13-iptables-installation-configuration.md) |
| 14 | Linux Process Troubleshooting | Linux / Troubleshooting | 2026-09-21 | [day-14-linux-process-troubleshooting.md](./day-14-linux-process-troubleshooting.md) |
| 15 | Setup SSL for Nginx | Linux / Networking / Security | 2026-09-25 | [day-15-setup-ssl-nginx.md](./day-15-setup-ssl-nginx.md) |
| 16 | Install and Configure Nginx as an LBR | Linux / Networking / Load Balancing | 2026-09-27 | [day-16-nginx-load-balancer.md](./day-16-nginx-load-balancer.md) |
| 17 | Install and Configure PostgreSQL | Databases / PostgreSQL | 2026-09-27 | [day-17-install-configure-postgresql.md](./day-17-install-configure-postgresql.md) |
| 18 | Configure LAMP Server | Linux / Web Stack | 2026-09-27 | [day-18-configure-lamp-server.md](./day-18-configure-lamp-server.md) |
| 19 | Install and Configure Web Application | Linux / Web Servers | 2026-09-27 | [day-19-install-configure-web-application.md](./day-19-install-configure-web-application.md) |
| 20 | Configure Nginx + PHP-FPM Using Unix Socket | Linux / Web Stack | 2026-09-27 | [day-20-nginx-php-fpm-unix-socket.md](./day-20-nginx-php-fpm-unix-socket.md) |
| 21 | Set Up Git Repository on Storage Server | Git / Version Control | 2026-09-27 | [day-21-setup-git-repository-storage-server.md](./day-21-setup-git-repository-storage-server.md) |
| 22 | Clone Git Repository on Storage Server | Git / Version Control | 2026-09-27 | [day-22-clone-git-repository-storage-server.md](./day-22-clone-git-repository-storage-server.md) |
| 23 | Fork a Git Repository | Git / Gitea | 2026-09-27 | [day-23-fork-git-repository.md](./day-23-fork-git-repository.md) |
| 24 | Git Create Branches | Git / Version Control | 2026-09-27 | [day-24-git-create-branches.md](./day-24-git-create-branches.md) |
| 25 | Git Merge Branches | Git / Version Control | 2026-09-27 | [day-25-git-merge-branches.md](./day-25-git-merge-branches.md) |
| 26 | Git Manage Remotes | Git / Version Control | 2026-09-29 | [day-26-git-manage-remotes.md](./day-26-git-manage-remotes.md) |
| 27 | Git Revert Some Changes | Git / Version Control | 2026-09-29 | [day-27-git-revert-changes.md](./day-27-git-revert-changes.md) |
| 28 | Git Cherry Pick Start | Git / Version Control | 2026-10-09 | [day-28-git-cherry-pick.md](./day-28-git-cherry-pick.md) |
| 29 | Manage Git Pull Requests | Git / Gitea / Code Review | 2026-10-09 | [day-29-manage-git-pull-requests.md](./day-29-manage-git-pull-requests.md) |
| 30 | Git Hard Reset | Git / Version Control | 2026-10-09 | [day-30-git-hard-reset.md](./day-30-git-hard-reset.md) |
| 31 | Git Stash | Git / Version Control | 2026-10-09 | [day-31-git-stash.md](./day-31-git-stash.md) |
| 32 | Git Rebase | Git / Version Control | 2026-10-09 | [day-32-git-rebase.md](./day-32-git-rebase.md) |
| 33 | Resolve Git Merge Conflicts | Git / Version Control | 2026-10-09 | [day-33-resolve-git-merge-conflicts.md](./day-33-resolve-git-merge-conflicts.md) |
| 34 | Git Hook | Git / Automation | 2026-10-09 | [day-34-git-hook.md](./day-34-git-hook.md) |
| 35 | Install Docker Packages and Start Docker Service | Docker / Containers | 2026-11-22 | [day-35-install-docker-start-service.md](./day-35-install-docker-start-service.md) |
| 36 | Deploy Nginx Container on Application Server | Docker / Containers | 2026-11-22 | [day-36-deploy-nginx-container.md](./day-36-deploy-nginx-container.md) |
| 37 | Copy File to Docker Container | Docker / Containers | 2026-11-22 | [day-37-copy-file-to-docker-container.md](./day-37-copy-file-to-docker-container.md) |
| 38 | Pull Docker Image | Docker / Containers | 2026-11-22 | [day-38-pull-docker-image.md](./day-38-pull-docker-image.md) |
| 39 | Create a Docker Image From Container | Docker / Containers | 2026-11-22 | [day-39-create-docker-image-from-container.md](./day-39-create-docker-image-from-container.md) |
| 40 | Docker EXEC Operations | Docker / Containers | 2026-11-22 | [day-40-docker-exec-operations.md](./day-40-docker-exec-operations.md) |
| 41 | Write a Docker File | Docker / Containers | 2026-11-22 | [day-41-write-a-dockerfile.md](./day-41-write-a-dockerfile.md) |
| 42 | Create a Docker Network | Docker / Networking | 2026-11-22 | [day-42-create-docker-network.md](./day-42-create-docker-network.md) |
| 43 | Docker Ports Mapping | Docker / Networking | 2026-11-22 | [day-43-docker-ports-mapping.md](./day-43-docker-ports-mapping.md) |
| 44 | Write a Docker Compose File | Docker / Docker Compose | 2026-11-22 | [day-44-write-docker-compose-file.md](./day-44-write-docker-compose-file.md) |
| 45 | Resolve Dockerfile Issues | Docker / Troubleshooting | 2026-11-22 | [day-45-resolve-dockerfile-issues.md](./day-45-resolve-dockerfile-issues.md) |
| 46 | Deploy an App on Docker Containers | Docker / Docker Compose | 2026-11-22 | [day-46-deploy-app-on-docker-containers.md](./day-46-deploy-app-on-docker-containers.md) |
| 47 | Docker Python App | Docker / Containers | 2026-11-22 | [day-47-docker-python-app.md](./day-47-docker-python-app.md) |
| 48 | Deploy Pods in Kubernetes Cluster | Kubernetes / Pods | 2026-11-22 | [day-48-deploy-pods-in-kubernetes-cluster.md](./day-48-deploy-pods-in-kubernetes-cluster.md) |
| 49 | Deploy Applications with Kubernetes Deployments | Kubernetes / Deployments | 2026-11-22 | [day-49-kubernetes-deployments.md](./day-49-kubernetes-deployments.md) |
| 50 | Set Resource Limits in Kubernetes Pods | Kubernetes / Resource Management | 2026-11-22 | [day-50-kubernetes-resource-limits.md](./day-50-kubernetes-resource-limits.md) |
<!-- INDEX_END -->

---

## Stack covered across this series

`Linux` `Kubernetes` `Terraform` `Docker` `Nginx` `Bash`

---

⭐ If any of these help you, a star is appreciated — and feel free to open an issue if something's outdated or wrong.

