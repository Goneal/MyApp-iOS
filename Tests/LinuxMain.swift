import XCTest

@testable import MyAppTests

XCTMain([
    testCase(CreateLoginUITests.allTests),
    testCase(ImplementUserAuthenticationBackendTests.allTests),
    testCase(SetUpCoreDataTests.allTests),
    testCase(DesignUserProfileViewTests.allTests),
    testCase(ImplementDataPersistenceLogicTests.allTests)
])
