from unit_tests_test_suite import UnitTestsTestSuite
from integration_tests_test_suite import IntegrationTestsTestSuite
from unittest import TestResult, TestLoader, TextTestRunner

def main():
	problematic_unit_test_files = run_unit_tests()
	print_results(problematic_unit_test_files, 'Unit Tests')

	problematic_integration_test_files = run_integration_tests()
	print_results(problematic_integration_test_files, 'Integration Tests')

def print_results(problematic_files, title):
	print(title)
	if len(problematic_files) == 0:
		print('All tests executed succesfully!')
	else:
		print('Files that did not run successfully:')
		for file in problematic_files:
			print('\t- ' + file)
	print()

def run_unit_tests():
	'''
		Runs all unit tests and returns a list of files that did not execute successfully
	'''
	unit_tests_test_suite = UnitTestsTestSuite()
	unit_tests_test_result = TestResult()
	unit_tests_test_suite.run(unit_tests_test_result)

	problematic_files = set()
	for error in unit_tests_test_result.errors:
		components = str(error[0]).split('.')
		problematic_files.add(components[-2])

	for failure in unit_tests_test_result.failures:
		components = str(failure[0]).split('.')
		problematic_files.add(components[-2])

	return problematic_files

def run_integration_tests():
	'''
		Runs all integration tests and returns a list of files that did not execute successfully
	'''
	integration_tests_test_suite = IntegrationTestsTestSuite()
	integration_tests_test_result = TestResult()
	integration_tests_test_suite.run(integration_tests_test_result)

	problematic_files = set()
	for error in integration_tests_test_result.errors:
		print(error[1])
		components = str(error[0]).split('.')
		problematic_files.add(components[-2])

	for failure in integration_tests_test_result.failures:
		components = str(failure[0]).split('.')
		problematic_files.add(components[-2])
		print(failure[1])

	return problematic_files

if __name__ == '__main__':
	main()