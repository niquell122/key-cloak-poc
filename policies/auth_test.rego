# filename - auth_test.rego
package authz

# Test allow rule for writer
test_allow_admin_write {
  allow with input as {"role": "admin", "access": "write"}
}

test_allow_admin_read {
  allow with input as {"role": "admin", "access": "read"}
}

# Test allow rule for user
test_allow_user_read {
  allow with input as {"role": "user", "access": "read"}
}

test_deny_user_write {
  not allow with input as {"role": "user", "access": "write"}
}

# Test default deny
test_default_deny {
  not allow with input as {"role": "unknown", "access": "something"}
}

# Test allow rule for default-roles-master
test_allow_default_roles_master_read {
  allow with input as {"role": "default-roles-master", "access": "read"}
}

# Test allow rule for default-roles-master
test_deny_default_roles_master {
  not allow with input as {"role": "default-roles-master", "access": "some-random-action"}
}

