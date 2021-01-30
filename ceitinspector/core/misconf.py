from ceitinspector.modules.misconf_generator import ConfErr
from ceitinspector.modules.misconf_generator import ConfTest
from ceitinspector.modules.misconf_generator import Fuzzing
from ceitinspector.modules.misconf_generator import ConfDiagDetector
from ceitinspector.modules.misconf_generator import CaseAlt

errs = {"name": None,
        "key": None,
        "operator": None,
        "value": None}


class MisconfEngine( object ):
    log_engine = None
    conf_path = ""
    misconf_mode = ""

    def __init__(self, log_engine, conf_path, misconf_mode):
        self.log_engine = log_engine
        self.log_engine.info( "MisconfEngine Startup." )
        self.conf_path = conf_path
        self.misconf_mode = misconf_mode

    def mutate(self, option):
        if self.misconf_mode == "Fuzzing":
            fuzzing = Fuzzing( option )
            errs = fuzzing.get_misconfs()
            return errs
        elif self.misconf_mode == "ConfErr":
            conferr = ConfErr( option )
            errs = conferr.get_misconfs()
            return errs
        elif self.misconf_mode == "ConfTest":
            conftest = ConfTest( option )
            errs = conftest.get_misconfs()
            return errs
        elif self.misconf_mode == "ConfDiagDetector":
            confdiagdetector = ConfDiagDetector( option )
            errs = confdiagdetector.get_misconfs()
            return errs
        elif self.misconf_mode == "CaseAlt":
            casealt = CaseAlt( option )
            errs = casealt.get_misconfs()
            return errs
        else:
            self.log_engine.error( "misconf_mode could not recognize." )
