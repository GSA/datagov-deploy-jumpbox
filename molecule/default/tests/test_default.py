import os
import re

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


testuser = 'testuser'
testuser_public_key = 'testuser-public-key-string'


def test_operators_group(host):
    operators = host.group('operators')

    assert operators.exists


def test_ubuntu_user(host):
    """Test ubuntu user exists and is part of the operators group."""
    user = host.user('ubuntu')

    assert user.exists
    assert 'operators' in user.groups
    assert 'ubuntu' in user.groups
    assert user.expiration_date is None
    assert user.password == '!', 'user password should be locked'


def test_datagov_configuration_dir(host):
    datagov = host.file('/etc/datagov')

    assert datagov.is_directory
    assert datagov.mode == 0o750
    assert datagov.user == 'root'
    assert datagov.group == 'operators'


def test_ansible_cfg(host):
    ansible_cfg = host.file('/etc/datagov/ansible.cfg')

    assert ansible_cfg.is_file
    assert ansible_cfg.mode == 0o644
    assert ansible_cfg.user == 'root'
    assert ansible_cfg.group == 'operators'


def test_user_created(host):
    user = host.user(testuser)

    assert user.expiration_date is None
    assert user.home
    assert 'operators' in user.groups
    assert user.shell == '/bin/bash'
    assert user.password == '!', 'user password should be locked'


def test_authorized_keys(host):
    user = host.user(testuser)
    authorized_keys = host.file('%s/.ssh/authorized_keys' % user.home)

    assert authorized_keys.exists
    assert authorized_keys.contains(testuser_public_key)


def test_chage(host):
    chage = host.check_output('chage -l testuser')

    assert re.search(r'Account expires\s+: never', chage)
    assert re.search(r'Password expires\s+: never', chage)
    assert re.search(r'Password inactive\s+: never', chage)


def test_dsh_all_group(host):
    group = host.file('/etc/dsh/group/all')

    assert group.exists
    assert group.mode == 0o644
    assert group.user == 'root'
    assert group.group == 'root'
    assert group.contains("jumpbox1\njumpbox2")


def test_dsh_jumpbox_group(host):
    group = host.file('/etc/dsh/group/jumpbox')

    assert group.exists
    assert group.mode == 0o644
    assert group.user == 'root'
    assert group.group == 'root'
    assert group.contains("jumpbox1\njumpbox2")
