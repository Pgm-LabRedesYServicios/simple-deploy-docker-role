import os
import pytest
import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


@pytest.mark.parametrize("package", [
    ("docker-ce"),
    ("python-pip"),
])
def test_required_packages_exist(host, package):
    pkg = host.package(package)
    assert pkg.is_installed


@pytest.mark.parametrize("pip_package", [
    ("docker-py"),
])
def test_required_pip_packages_exist(host, pip_package):
    pip_packages = host.pip_package.get_packages()
    assert pip_package in pip_packages


# Test remotely build from image

def test_build_nginx_image_is_downloaded(host):
    with host.sudo():
        registry_exist = host.check_output(
            'docker inspect --type=image image-nginx',
        )
        assert not registry_exist == 'Error: No such image: ' + \
                                     'image-nginx'


def test_build_nginx_is_enabled_and_running(host):
    service = host.service('image-nginx')
    assert service.is_enabled
    assert service.is_running


def test_build_nginx_is_working(host):
    build_nginx_exist = host.check_output('curl localhost:8080')
    assert '<h1>Welcome to nginx!</h1>' in build_nginx_exist


# Test remotely build from git

def test_image_nginx_image_is_downloaded(host):
    with host.sudo():
        registry_exist = host.check_output(
            'docker inspect --type=image git-nginx',
        )
        assert not registry_exist == 'Error: No such image: ' + \
                                     'git-nginx'


def test_image_nginx_is_enabled_and_running(host):
    service = host.service('git-nginx')
    assert service.is_enabled
    assert service.is_running


def test_image_nginx_is_working(host):
    build_nginx_exist = host.check_output('curl localhost:8081')
    assert '<h1>Welcome to nginx!</h1>' in build_nginx_exist
