import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

# Initialize tokenizer and model
model_name = "ammarnasr/codegen-350M-mono-swift"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

def generate_unit_test(code_snippet, class_name):
    test_prompt = f"""
// Swift Unit Test
// Write a unit test for the following Swift code:

{code_snippet}

// Requirements:
// 1. Use XCTest framework
// 2. Test the main functionality of the class
// 3. Include assertions to verify expected behavior
// 4. Follow Swift naming conventions for test methods (test_functionName)

import XCTest
@testable import MyApp

class {class_name}Tests: XCTestCase {{

    // MARK: - Test Cases

    // TODO: Implement test cases here

}}
"""
    input_ids = tokenizer.encode(test_prompt, return_tensors='pt')

    try:
        with torch.no_grad():
            output = model.generate(
                input_ids,
                max_length=1000,
                num_return_sequences=1,
                do_sample=False,
                temperature=0.7,
                top_k=50,
                top_p=0.95,
                repetition_penalty=1.2,
                pad_token_id=tokenizer.eos_token_id,
                no_repeat_ngram_size=3
            )

        test_code = tokenizer.decode(output[0], skip_special_tokens=True)
        return test_code
    except Exception as e:
        print(f"An error occurred while generating the unit test: {e}")
        return None

def write_test_file(file_path, test_code):
    with open(file_path, 'w') as f:
        f.write(test_code)
    print(f"Written test to {file_path}")

def generate_tests_for_app():
    project_name = "MyApp"
    test_dir = f"{project_name}/Tests"
    os.makedirs(test_dir, exist_ok=True)

    # LoginViewController
    with open(f"{project_name}/Controllers/LoginViewController.swift", 'r') as f:
        login_view_controller_code = f.read()
    login_test_code = generate_unit_test(login_view_controller_code, "LoginViewController")
    write_test_file(f"{test_dir}/LoginViewControllerTests.swift", login_test_code)

    # UserAuthenticationManager
    with open(f"{project_name}/Models/UserAuthenticationManager.swift", 'r') as f:
        user_auth_manager_code = f.read()
    user_auth_test_code = generate_unit_test(user_auth_manager_code, "UserAuthenticationManager")
    write_test_file(f"{test_dir}/UserAuthenticationManagerTests.swift", user_auth_test_code)

    # CoreDataManager
    with open(f"{project_name}/Models/CoreDataManager.swift", 'r') as f:
        core_data_manager_code = f.read()
    core_data_test_code = generate_unit_test(core_data_manager_code, "CoreDataManager")
    write_test_file(f"{test_dir}/CoreDataManagerTests.swift", core_data_test_code)

    print("Unit tests generated successfully")

if __name__ == "__main__":
    generate_tests_for_app()
