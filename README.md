Deploy docker as a service
==========================

This is a simplified copy of [this
role](https://git.digitales.cslabrecha.org/ansible-roles/deploy-docker).

It only builds the docker on the remote machine and it doesn't interact with any
registry.

Downloads a git repository which has a Dockerfile, builds it locally (or
remotely) or just download a Docker image.

Also create a systemd service to manage it.

Requirements
------------

* Pip installed on host
* Docker installed on the host
* Docker installed on the device that is running ansible
* A registry where you can log in

Role Variables
--------------

* `git_repository`: The repository in which the dockerfile is located.
* `git_repository_destination`: Local path in which to clone the git repository.
* `git_repository_extra_path`: Extra path inside the cloned repo to the
  directory containing the Dockerfile
* `git_repository_tag`: Version to use of the git repository.
* `service_name`: Name of the systemd service. If it's empty it wont install the
  service
* `docker_image`: If you want to download a docker image and not a git repository
* `docker_image_tag`: Docker tag.
* `docker_command`: Docker command used to launch the container.
* `create_service`: Boolean to decide if you want to install the systemd service
  (Default: `True`)
* `skip_git_clone`: Boolean to decide if you want to skip the repository clone,
  useful in case you want to clone it and do operations before the build.

Dependencies
------------

None.

Example Playbook
----------------

```yaml
- hosts: servers
  vars:
    remote_build: True
    git_repository: https://github.com/nginxinc/docker-nginx
    git_repository_destination: /tmp/docker-nginx
    git_repository_extra_path: stable/stretch
    git_repository_tag: master
    service_name: git-nginx
    docker_image_tag: latest
    docker_command: /usr/bin/docker run --rm -i --name "{{ service_name }}" -p 8081:80 "{{ docker_registry_read }}/{{ service_name }}"
  roles:
    - { role: deploy-docker}
```

Testing
-------

To test the role you need [molecule](http://molecule.readthedocs.io/en/latest/).

And vagrant installed with libvirt

```bash
molecule test
```

License
-------

GPL3

Author Information
------------------

lyz [ EN ] riseup.net
drymer [ EN ] autistici.org
