import unittest, logging, json, sys

try:
 import xmlrunner
except ImportError:
 pass

try:
    from StringIO import StringIO
except ImportError:
    # Python 3 Support
    from io import StringIO

sys.path.append('src')
import jsonlogger

class testJsonLogger(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        self.buffer = StringIO()
        
        self.logHandler = logging.StreamHandler(self.buffer)
        self.logger.addHandler(self.logHandler)

    def testDefaultFormat(self):
        fr = jsonlogger.JsonFormatter()
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        logJson = json.loads(self.buffer.getvalue())

        self.assertEqual(logJson["message"], msg)

    def testFormatKeys(self):
        supported_keys = [
            'asctime',
            'created',
            'filename',
            'funcName',
            'levelname',
            'levelno',
            'lineno',
            'module',
            'msecs',
            'message',
            'name',
            'pathname',
            'process',
            'processName',
            'relativeCreated',
            'thread',
            'threadName'
        ]

        log_format = lambda x : ['%({0:s})'.format(i) for i in x] 
        custom_format = ' '.join(log_format(supported_keys))

        fr = jsonlogger.JsonFormatter(custom_format)
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        self.logger.info(msg)
        log_msg = self.buffer.getvalue()
        log_json = json.loads(log_msg)

        for supported_key in supported_keys:
            if supported_key in log_json:
                self.assertTrue(True)
    
    def testUnknownFormatKey(self):
        fr = jsonlogger.JsonFormatter('%(unknown_key)s %(message)s')
        self.logHandler.setFormatter(fr)

        msg = "testing logging format"
        try:
            self.logger.info(msg)
        except KeyError:
            self.assertTrue("KeyError exception thrown")

if __name__=='__main__':
    if len(sys.argv[1:]) > 0 :
        if sys.argv[1] == 'xml':
            testSuite = unittest.TestLoader().loadTestsFromTestCase(testJsonLogger)
            xmlrunner.XMLTestRunner(output='reports').run(testSuite)
    else:
        unittest.main()
