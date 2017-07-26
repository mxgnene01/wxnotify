# -*- coding: utf-8 -*-
#

class GenericError(Exception):
    error_format = 'generic error'

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs

        if not message:
            try:
                message = self.error_format % self.kwargs
            except:
                message = 'cannot format exception message'

        self.message = message
        super(GenericError, self).__init__(message)
