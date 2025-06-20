class RDiffRuntimeError(RuntimeError):
    def __init__(self):
        super(RDiffRuntimeError, self).__init__()


class EmptyBackupTargetException(RuntimeError):
    def __init__(self):
        super(EmptyBackupTargetException, self).__init__()
