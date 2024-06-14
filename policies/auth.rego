package httpapi.authz
import rego.v1

default allow := true

# allow if {
#     input.request_method == "GET"
# }

# allow if {
#     input.request_method == "GET"
#     print(input.given_name)
# }

# allow if { 
#     input.request_method == "GET"
#     input.user == "Nicolas"
# }

deny if {
  some realm
  input.request_method == "GET"
  input.request_path = ["book", realm]
  input.aud != realm
}