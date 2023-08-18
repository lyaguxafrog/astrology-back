#!flask/bin/python
import sys
from app import app

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'tests':
        import unittest
        tests = unittest.TestLoader().discover('tests')
        result = unittest.TextTestRunner(verbosity=2).run(tests)
        if result.wasSuccessful():
            sys.exit(0)
        else:
            sys.exit(1)
    else:
        if __name__ == '__main__':
            app.run(debug=True)