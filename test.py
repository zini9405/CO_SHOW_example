import json

# Mapping 데이터를 JSON 파일로 저장
mappings = {
    "RECIPE_ID": recipe_mapping,
    "EQP_ID_MODULE_NAME": eqp_mapping
}

# JSON 파일 저장
mapping_file_path = "mappings.json"
with open(mapping_file_path, "w") as json_file:
    json.dump(mappings, json_file, indent=4)

print(f"Mapping data saved to {mapping_file_path}")