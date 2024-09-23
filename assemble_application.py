import os

def create_project_structure(project_name):
    folders = ['Models', 'Views', 'ViewModels', 'Controllers']
    for folder in folders:
        os.makedirs(f"{project_name}/{folder}", exist_ok=True)
    print(f"Created project structure for {project_name}")

def write_code_to_file(file_path, code):
    with open(file_path, 'w') as file:
        file.write(code)
    print(f"Written code to {file_path}")

def assemble_application():
    project_name = "MyApp"
    create_project_structure(project_name)

    # LoginViewController
    login_view_controller_code = """
import UIKit

class LoginViewController: UIViewController {

    // MARK: - Properties

    @IBOutlet weak var emailTextField: UITextField!
    @IBAction func onLogin(_ sender: Any) {
        emailTextField.becomeFirstResponder()
    }

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
    }

    override var preferredStatusBarStyle: UIStatusBarStyle {
        return .lightContent
    }
}
"""
    write_code_to_file(f"{project_name}/Controllers/LoginViewController.swift", login_view_controller_code)

    # UserAuthenticationManager
    user_authentication_manager_code = """
import Foundation

class UserAuthenticationManager {

    // MARK: - Properties

    private let session: URLSession

    init(session: URLSession = URLSession(configuration: .default)) {
        self.session = session
    }

    // MARK: Methods

    func signIn(email: String, password: String, completion: @escaping (Result<User, Error>) -> Void) {
        guard let url = URL(string: "https://api.example.com/login") else {
            completion(.failure(NSError(domain: "Invalid URL", code: 0, userInfo: nil)))
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: String] = ["email": email, "password": password]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        let task = session.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "No data received", code: 0, userInfo: nil)))
                return
            }

            do {
                let decoder = JSONDecoder()
                let user = try decoder.decode(User.self, from: data)
                completion(.success(user))
            } catch {
                completion(.failure(error))
            }
        }

        task.resume()
    }
}
"""
    write_code_to_file(f"{project_name}/Models/UserAuthenticationManager.swift", user_authentication_manager_code)

    # CoreDataManager
    core_data_manager_code = """
import CoreData

class CoreDataManager {

    // MARK: - Properties

    static let shared = CoreDataManager()

    private lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")
        container.loadPersistentStores { (storeDescription, error) in
            if let error = error as NSError? {
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        }
        return container
    }()

    // MARK: - Initialization

    private init() {}

    // MARK: - Core Data Saving support

    func saveContext () {
        let context = persistentContainer.viewContext
        if context.hasChanges {
            do {
                try context.save()
            } catch {
                let nserror = error as NSError
                fatalError("Unresolved error \(nserror), \(nserror.userInfo)")
            }
        }
    }

    // MARK: - CRUD Operations

    func createUser(name: String, email: String) -> User? {
        let context = persistentContainer.viewContext
        let user = NSEntityDescription.insertNewObject(forEntityName: "User", into: context) as! User
        user.name = name
        user.email = email

        do {
            try context.save()
            return user
        } catch {
            print("Failed to create user: \(error)")
            return nil
        }
    }

    func fetchUsers() -> [User] {
        let context = persistentContainer.viewContext
        let fetchRequest: NSFetchRequest<User> = User.fetchRequest()

        do {
            return try context.fetch(fetchRequest)
        } catch {
            print("Failed to fetch users: \(error)")
            return []
        }
    }
}
"""
    write_code_to_file(f"{project_name}/Models/CoreDataManager.swift", core_data_manager_code)

    print("Application assembled successfully")

if __name__ == "__main__":
    assemble_application()
