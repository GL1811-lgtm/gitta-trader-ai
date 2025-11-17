import unittest
import os

# This test attempts to parse the HTML structure of the frontend.
# It uses BeautifulSoup, a common library for parsing HTML.
# As per project constraints, we will not install it, but wrap the
# import in a try-except block.

# Note: Testing the JavaScript functionality (e.g., button clicks,
# API calls) from Python without a browser environment (like Selenium)
# or a JS runtime is not practical. A proper frontend test would be
# written in JavaScript using a framework like Jest.

try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

class TestFrontendStatic(unittest.TestCase):

    def setUp(self):
        self.base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.html_path = os.path.join(self.base_path, 'frontend', 'index.html')

    @unittest.skipUnless(BS4_AVAILABLE, "BeautifulSoup4 is not installed. Skipping HTML structure tests.")
    def test_html_structure(self):
        """
        Tests if the index.html file has the required UI elements.
        """
        with open(self.html_path, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        self.assertIsNotNone(soup, "Could not parse HTML file.")

        # Check for header
        header = soup.find('h1')
        self.assertIsNotNone(header, "H1 header not found.")
        self.assertEqual(header.text.strip(), "Gitta Trader AI – Dashboard")

        # Check for input field
        input_field = soup.find('input', {'id': 'symbol-input'})
        self.assertIsNotNone(input_field, "Symbol input field not found.")

        # Check for button
        button = soup.find('button', {'id': 'predict-btn'})
        self.assertIsNotNone(button, "Prediction button not found.")
        self.assertEqual(button.text.strip(), "Get Prediction")

        # Check for output box and its children
        output_box = soup.find('div', {'id': 'output-box'})
        self.assertIsNotNone(output_box, "Output box not found.")

        signal_val = soup.find('span', {'id': 'signal-value'})
        self.assertIsNotNone(signal_val, "Signal value span not found.")

        confidence_val = soup.find('span', {'id': 'confidence-value'})
        self.assertIsNotNone(confidence_val, "Confidence value span not found.")

        reason_val = soup.find('span', {'id': 'reason-value'})
        self.assertIsNotNone(reason_val, "Reason value span not found.")

    def test_file_existence(self):
        """
        Tests that all required frontend files exist.
        """
        self.assertTrue(os.path.exists(self.html_path))
        self.assertTrue(os.path.exists(os.path.join(self.base_path, 'frontend', 'style.css')))
        self.assertTrue(os.path.exists(os.path.join(self.base_path, 'frontend', 'app.js')))

if __name__ == '__main__':
    unittest.main()
