"""utility function to install Ctrl+C handler
"""
import inspect
import logging
import pprint
import signal
import sys
import types

from utils.logconfig import mylog


__all__ = ['set_signal_int']

def set_signal_int():
    """connect the signal signal.SIGINT to handler handler_signit
    """
    signal.signal(signal.SIGINT, handler_sigint)

def handler_sigint(signum, frame):
    """handler the Ctrl+C command :mod:`signal.signal` (signal.SIGINT, self.handler_SIGINT)

    Parameters
    ----------
    signum : :obj:`int`
    frame  : :class:`types.FrameType`

    """

    def log_frame(some_frame):
        """log the frame where the Ctrl+C occurred

        Parameters
        ----------
        some_frame  : :class:`types.FrameType`
        """

        try:
            class_name = some_frame.f_locals['self'].__class__.__name__
        except KeyError:
            class_name = None

        try:
            mylog.debug("""
signum     :'%s'  
frame      :'%s' 
f_lineno   :'%s' 
class_name :'%s'""" % (signum,
                       some_frame,
                       some_frame.f_lineno,
                       class_name))
            if some_frame.f_exc_type is not None:
                mylog.info("frame.f_exc_type          '%s' " % some_frame.f_exc_type) #exception type if raised in this frame, or None

            if some_frame.f_exc_traceback is not None:
                mylog.info("frame.f_exc_traceback     '%s' " % some_frame.f_exc_traceback) #traceback if raised in this frame, or None

            if some_frame.f_trace is not None:
                mylog.info("frame.f_trace             '%s' " % some_frame.f_trace)#tracing function for this frame, or None

            mylog.debug("frame.f_back              '%s' " % some_frame.f_back) #next outer frame object (this frame caller)

            if mylog.level == logging.DEBUG:
                mylog.info("frame.f_globals         \n'%s' " % (pprint.pformat(some_frame.f_globals, indent=4, width=10, depth=2)))
                mylog.info("frame.f_locals          \n'%s' " % (pprint.pformat(some_frame.f_locals, indent=4, width=10, depth=2)))
            mylog.debug("frame.f_lasti             '%s' " % some_frame.f_lasti) #index of last attempted instruction in bytecode

            if frame.f_exc_type is not None:
                mylog.info("frame.f_exc_type          '%s' " % some_frame.f_exc_type)

            my_stacktrace = inspect.getframeinfo(some_frame)
            mylog.info("'%s' " % pprint.pformat(my_stacktrace))
            mylog.debug("source code file          '%s' " % inspect.getsourcefile(some_frame))
            mylog.debug("source code              '%s' " % inspect.getsource(some_frame))
        except (TypeError,IOError) as e:
            mylog.error("The object is a built-in module, class, or function. e = '%s' type %s" % (e, type(e)))
        except AttributeError as e:
            mylog.error("e = '%s' type %s" % (e, type(e)))
        except Exception as e:
            mylog.error("%s %s" % (e, type(e)))

    mylog.info("signum    :'%d' signal.SIGINT %d" % (signum,signal.SIGINT))
    mylog.info("type(frame) %s isinstance types.FrameType frame ? %s frame.__class__ %s " %
               (type(frame),
                isinstance(frame,types.FrameType),
                frame.__class__))
    my_frame = frame
    my_stacktrace = []
    import traceback

    extract = traceback.extract_stack(frame)

    mylog.info("\n%s" % pprint.pformat(traceback.format_list(extract)))

    while my_frame is not None:
        if mylog.level == logging.DEBUG:
            log_frame(my_frame)
        try:
            my_stacktrace.append(str(inspect.getframeinfo(my_frame)))
        except AttributeError as e:
            mylog.error("AttributeError %s" %e)
            pass
        my_frame = my_frame.f_back
    mylog.debug("'%s' " % pprint.pformat(my_stacktrace))

    sys.exit(0)#this will generate SystemExit exception

