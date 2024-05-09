include "root" {
  path = find_in_parent_folders()
}

inputs = {
  parameter_names = ["guardian-api-key", "openai-api-key", "medium-api-key"]
}
