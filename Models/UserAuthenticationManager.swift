import Foundation

class UserAuthenticationManager {

    // MARK: - Properties

    static let shared = UserAuthenticationManager()
    private let baseURL = "https://api.example.com" // Replace with your actual API base URL

    // MARK: - Methods

    func login(email: String, password: String, completion: @escaping (Result<User, Error>) -> Void) {
        let loginURL = URL(string: "\(baseURL)/login")!
        var request = URLRequest(url: loginURL)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: Any] = ["email": email, "password": password]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "UserAuthenticationManager", code: 0, userInfo: [NSLocalizedDescriptionKey: "No data received"])))
                return
            }

            do {
                let user = try JSONDecoder().decode(User.self, from: data)
                completion(.success(user))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }

    func register(email: String, password: String, completion: @escaping (Result<User, Error>) -> Void) {
        let registerURL = URL(string: "\(baseURL)/register")!
        var request = URLRequest(url: registerURL)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        let body: [String: Any] = ["email": email, "password": password]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)

        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                completion(.failure(error))
                return
            }

            guard let data = data else {
                completion(.failure(NSError(domain: "UserAuthenticationManager", code: 0, userInfo: [NSLocalizedDescriptionKey: "No data received"])))
                return
            }

            do {
                let user = try JSONDecoder().decode(User.self, from: data)
                completion(.success(user))
            } catch {
                completion(.failure(error))
            }
        }.resume()
    }
}

// MARK: - User Model

struct User: Codable {
    let id: String
    let email: String
    // Add any other user properties as needed
}
