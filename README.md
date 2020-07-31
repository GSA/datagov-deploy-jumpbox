[![CircleCI](https://circleci.com/gh/GSA/datagov-deploy-jumpbox.svg?style=svg)](https://circleci.com/gh/GSA/datagov-deploy-jumpbox)

# gsa.datagov-deploy-jumpbox

This role configures the jumpbox host for access by operators.

- User accounts are locked
- Users have password-less sudo access
- Users are allowed SSH access by the specified public key

## Requirements

- [Ansible](https://www.ansible.com/) 2.6+

## Usage

Add gsa.datagov-deploy-jumpbox to your requirements.yml and install with
ansible-galaxy.

Example Playbook
-------------------------

```
---
- name: Jumpbox
  hosts: all
  roles:
    - role: jumpbox
```


### Variables

**jumpbox_operators** list<object>

The user accounts to create on the jumpbox. User objects should include
a `username`, `email`, and `public_key` (contents of the users id_rsa.pub). The user's `authorized_keys` is set exclusively to this key, so any modifications to
`authorized_keys` will be overridden the next time this role is run.

```
jumpbox_operators:
  - username: userone
    email: userone@example.com
    public_key: ssh-rsa aabbccddeeff1234567890 comment
```

- `username` (required) name of the user account to create
- `email` (required) email address of the user
- `public_key` (required) the public SSH key for the user (contents of
  id_rsa.pub)
