include "root" {
  path = find_in_parent_folders()
}

inputs = {
  parameter_names = [
    "/news-for-kids/guardian-api-key", 
    "/news-for-kids/openai-api-key", 
    "/news-for-kids/medium-api-key",
    "/news-for-kids/openai-organization",
    "/news-for-kids/openai-project"
    ]
}
