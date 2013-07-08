from abc import ABCMeta, abstractmethod

def _has_attribute( cls, attr ):
    return True if any(attr in B.__dict__ for B in cls.__mro__) else False

def _has_attributes( cls, attrs ):
    return True if all(_has_attribute(cls, a) for a in attrs) else False

    

#*******************************************************************************
# R e q u e s t A B C                                                          *
#*******************************************************************************

class RequestABC:
    __metaclass__ = ABCMeta

    @abstractmethod
    def wait( self ):
        ''' doc '''

    @abstractmethod
    def notify( self, callback, **kwargs ):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is RequestABC:
            return True if _has_attributes(C, ['wait', 'notify']) else False
        return NotImplemented



#*******************************************************************************
# S o u r c e A B C                                                            *
#*******************************************************************************

class SourceABC:
    __metaclass__ = ABCMeta

    @abstractmethod
    def request( self, slicing ):
        pass

    @abstractmethod
    def setDirty( self, slicing ):
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is SourceABC:
            return True if _has_attributes(C, ['request', 'setDirty']) else False
        return NotImplemented

    @abstractmethod
    def __eq__( self, other ):
        raise NotImplementedError

    @abstractmethod
    def __ne__( self, other ):
        raise NotImplementedError
    
    @abstractmethod
    def clean_up(self):
        pass
