import CoreData

class CoreDataManager {

    // MARK: - Properties

    static let shared = CoreDataManager()

    lazy var persistentContainer: NSPersistentContainer = {
        let container = NSPersistentContainer(name: "MyApp")
        container.loadPersistentStores { (storeDescription, error) in
            if let error = error as NSError? {
                fatalError("Unresolved error \(error), \(error.userInfo)")
            }
        }
        return container
    }()

    // MARK: - Core Data Saving support

    func saveContext() {
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

    func createUser(email: String, password: String) -> User? {
        let context = persistentContainer.viewContext
        let user = NSEntityDescription.insertNewObject(forEntityName: "User", into: context) as! User
        user.email = email
        user.password = password

        do {
            try context.save()
            return user
        } catch {
            print("Failed to create user: \(error)")
            return nil
        }
    }

    func fetchUser(withEmail email: String) -> User? {
        let context = persistentContainer.viewContext
        let fetchRequest: NSFetchRequest<User> = User.fetchRequest()
        fetchRequest.predicate = NSPredicate(format: "email == %@", email)

        do {
            let users = try context.fetch(fetchRequest)
            return users.first
        } catch {
            print("Failed to fetch user: \(error)")
            return nil
        }
    }

    func updateUser(_ user: User) {
        let context = persistentContainer.viewContext
        do {
            try context.save()
        } catch {
            print("Failed to update user: \(error)")
        }
    }

    func deleteUser(_ user: User) {
        let context = persistentContainer.viewContext
        context.delete(user)
        do {
            try context.save()
        } catch {
            print("Failed to delete user: \(error)")
        }
    }
}

// MARK: - User Entity

@objc(User)
public class User: NSManagedObject {
    @NSManaged public var email: String?
    @NSManaged public var password: String?
}

extension User {
    @nonobjc public class func fetchRequest() -> NSFetchRequest<User> {
        return NSFetchRequest<User>(entityName: "User")
    }
}
