import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


inactiveuser = 'inactiveuser'
removeuser = 'removeuser'
testuser = 'testuser'


def test_inactive_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert not passwd.contains(inactiveuser)
    assert not group.contains(inactiveuser)


def test_removed_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert not passwd.contains(removeuser)
    assert not group.contains(removeuser)


def test_active_user(host):
    passwd = host.file('/etc/passwd')
    group = host.file('/etc/group')

    assert passwd.contains(testuser)
    assert group.contains(testuser)


def test_sudoers_removed(host):
    inactive_sudoer = host.file('/etc/sudoers.d/' + inactiveuser)
    remove_sudoer = host.file('/etc/sudoers.d/' + removeuser)
    test_sudoer = host.file('/etc/sudoers.d/' + testuser)

    assert not inactive_sudoer.exists
    assert not remove_sudoer.exists
    assert not test_sudoer.exists
