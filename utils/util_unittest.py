""":mod:`util_inittest` extends unittest.runner.TextTestRunner to add support variables like Db2_Cli
"""
import sys
import unittest
import pprint
import traceback
import logging
from utils.logconfig import mylog # @UnusedImport

class MyTextRunner(unittest.runner.TextTestRunner):

    #TextTestRunner
    #def __init__(self, stream=sys.stderr, descriptions=True, verbosity=1,
    #             failfast=False, buffer=False, resultclass=None):

    def __init__(self, verbosity=1, resultclass=None, Db2_Cli=None):
        """
        Parameters
        ----------
        verbosity   : :obj:`int`
        resultclass : :class:`MyTextTestResult`
        Db2_Cli     : :class:`cli_object.Db2_Cli`
        """

        super(MyTextRunner, self).__init__(descriptions=True,
                                           verbosity=verbosity,
                                           failfast=True,
                                           resultclass=resultclass)

        self.mDb2_Cli = Db2_Cli
        resultclass.mDb2_Cli = Db2_Cli 

        mylog.debug("MyTextRunner Db2_Cli       '{}' ", Db2_Cli)
        mylog.debug("MyTextRunner resultclass   '{}' ", resultclass)

    def run(self, testsuite):
        """I assign to each test mDb2_Cli
        """
 
        mylog.info("tests to be ran  \n%s " % pprint.pformat(testsuite._tests))
        for one_test in testsuite._tests:
            mylog.debug("tests to be tested  '%s' name '%s' " % (one_test, one_test.testName))
            one_test.mDb2_Cli = self.mDb2_Cli

        try:
            super(MyTextRunner, self).run(testsuite)
        except KeyboardInterrupt as _e:
            mylog.warn("KeyboardInterrupt")
            #self.stopTestRun()
            return

    #def stopTestRun(self):
    #    mylog.info("stopTestRun")
    #    super(MyTextRunner, self).stopTestRun()
    #    #if hasattr(test, "stop_test"):
    #    #    if test.stop_test:
    #    #        mylog.info("They called stopTestRun, stop_test is True")


class MyTextTestResult(unittest.runner.TextTestResult):
    """A test result class that can print formatted text results to a stream.

    Used by :class:`MyTextRunner`, extends :class:`unittest.runner.TextTestResult`
    """
    test=None
    def __init__(self, stream, descriptions, verbosity):
        super(MyTextTestResult, self).__init__(stream, descriptions, verbosity)
        self.success_test = []

        mylog.debug("""
descriptions %s 
verbosity    %s""" % (descriptions, verbosity))
        mylog.debug("current function that called  %s" % sys._getframe(  ).f_back.f_code.co_name)

    def startTestRun(self):
        if self.showAll:
            mylog.info("Starting Test...I can add parameters here per test")
        super(MyTextTestResult, self).startTestRun()
        mylog.info("done")

    def __del__(self):
        self.stream.close()
        if mylog.level == logging.DEBUG:
            print ("MyTextTestResult.__del__")

    def log_errors(self, errorlist, msg):
        for test, err in errorlist:
            mylog.error("""
%s : '%s'
Some  Desc  : '%s'
error trace : '%s'
""" % (msg,
       test,
       self.getDescription(test),
       pprint.pformat(err.split("\n"))))

    def addFailure(self, test, err):
        test.exc_info = err
        super(MyTextTestResult, self).addFailure(test, err)
        mylog.error("""
test :'%s' 
'%s'
'%s'
'%s'
""" % (test, err[0], err[1], err[2])
) 
        #mylog.info("type '%s'" % type(err[2]))
        mylog.error("%s" % traceback.format_exc())


    def addSuccess(self, func_name, *args, **kwargs):
        super(MyTextTestResult, self).addSuccess(func_name)
        my_str_arg = "("

        for arg in args:
            #mylog.info(str(arg))
            if my_str_arg != "(":
                my_str_arg += " ,"
            my_str_arg += str(arg)

        for kw in kwargs.keys():
            #mylog.info(str(kwargs[kw]))
            if my_str_arg != "(":
                my_str_arg += " ," 
            my_str_arg += "%s=%s" % (kw, kwargs[kw])

        my_str_arg += ")"
        if not str(func_name).startswith("runTest"):

            mylog.debug("test '%s   <.>   %s' %s" % (
                self.test.__class__.__name__,
                func_name,
                my_str_arg))

            self.success_test.append("%s.%s %s" % (
                self.test.__class__.__name__, 
                func_name,
                my_str_arg))

    def log_success(self):
        mylog.info("test succeeded \n'%s'\n" % pprint.pformat(self.success_test)) 
        #for success in self.success_test:
        #    mylog.info("test succeeded '%s'" % str(success))

    def log_skipped(self):
        if self.skipped:
            mylog.warn("test skipped \n'%s'\n" % pprint.pformat(self.skipped))
        #for skip in self.skipped:
        #    mylog.warn("test skipped '%s'" % str(skip))

    def stopTestRun(self):
        mylog.info("stopping  Test..'%s'" % self.descriptions)

        if self.mDb2_Cli.connected:

            if self.failures:
                mylog.debug("some failures \n%s\n" % self.failures)

            if self.errors:
                mylog.debug("some errors   \n%s\n" % pprint.pformat(self.errors))

            self.log_errors(self.errors  , "Some error")
            self.log_errors(self.failures, "Some Failure")
            self.log_success()
            self.log_skipped()
        else:
            mylog.error("Could not connect, wont log errors here mDb2_Cli.connected '%s'" % self.mDb2_Cli.connected)

        super(MyTextTestResult, self).stopTestRun()

    def startTest(self, test):
        test.stream = self.stream
        test.result = self
        self.test = test
        if self.showAll:
            mylog.info("""
test           '%s'
getDescription '%s'
""" % (test,
       self.getDescription(test)))

        super(MyTextTestResult, self).startTest(test)

