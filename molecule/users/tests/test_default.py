import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


inactiveuser = 'inactiveuser'
testuser = 'testuser'
ubuntu_user = 'ubuntu'


def test_inactive_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert not passwd.contains(inactiveuser)
    assert not group.contains(inactiveuser)


def test_active_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert passwd.contains(testuser)
    assert group.contains(testuser)


def test_sudoers_removed(host):
    inactive_sudoer = host.file('/etc/sudoers.d/' + inactiveuser)
    test_sudoer = host.file('/etc/sudoers.d/' + testuser)

    assert not inactive_sudoer.exists
    assert not test_sudoer.exists


def test_ubuntu_kept(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert passwd.contains(ubuntu_user)
    assert group.contains(ubuntu_user)
