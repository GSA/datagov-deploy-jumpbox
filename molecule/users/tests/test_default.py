import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


inactiveuser = 'inactiveuser'
removeduser = 'removeduser'
testuser = 'testuser'


def test_inactive_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert not passwd.contains(inactiveuser)
    assert not group.contains(inactiveuser)


def test_removed_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert not passwd.contains(removeduser)
    assert not group.contains(removeduser)


def test_active_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert passwd.contains(testuser)
    assert group.contains(testuser)
