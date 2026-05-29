# Dictionary 1
student1 = {
    "name": "Alex",
    "age": 42,
    "course": "Data Analytics",
    "city": "Auckland",
    "status": "Lecturer"
} 
# Dictionary 2
student2 = {
    "name": "Sophia",
    "age": 29,
    "course": "Software Engineering",
    "city": "Wellington",
    "status": "Student"
}
# Dictionary 3
student3 = {
    "name": "Michael",
    "age": 35,
    "course": "Cyber Security",
    "city": "Christchurch",
    "status": "Researcher"
}
"""
test1
merged_dic = {
    **{k: v for k, v in zip(student1.keys(), student1.values())if "azw" in student1["name"].lower()},
    **{k: v for k, v in zip(student2.keys(), student2.values())if "azw" in student1["name"].lower()},
    **{k: v for k, v in zip(student3.keys(), student3.values())if "azw" in student1["name"].lower()}
    }
"""
"""
test2 
merged_dict = {
    **{k: v for k, v in student1.items() if v in "Alex"},
    **{k: v for k, v in student2.items() if v in "Alex"},
    **{k: v for k, v in student3.items() if v in "Alex"},
}
"""
merged_dict = {
    **{k: v for k, v in student1.items() if "ex" in student1["name"].lower()},
    **{k: v for k, v in student2.items() if "ex" in student2["name"].lower()},
    **{k: v for k, v in student3.items() if "ex" in student3["name"].lower()},
}

merged_dict2 = {
    **{k: v for k, v in student1.items() if student1["name"].lower() in "ex"},
    **{k: v for k, v in student2.items() if student2["name"].lower() in "ex"},
    **{k: v for k, v in student3.items() if student3["name"].lower() in "ex"},
}

merged_dict3 = {
    **{k: v for k, v in student1.items() if k == "name" and "o" in str(v)},
    **{k: v for k, v in student2.items() if k == "name" and "o" in str(v)},
    **{k: v for k, v in student3.items() if k == "name" and "o" in str(v)}
}

print(merged_dict3)