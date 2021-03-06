# Copyright (c) 2017-2018 CRS4
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or
# substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE
# AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

class UnknownSender(Exception):
    """
    Exception to be raised when it was impossible to instantiate the correct sender
    """

class UnknownReceiver(Exception):
    """
    Exception to be raised when it was impossible to instantiate the correct receiver
    """

class NotInRangeError(Exception):
    """
    Exception to be raised when an id is not in the correct range
    """

class TopicNotAssigned(Exception):
    """
    Raise when trying to read a topic that is not assigned to the consumer
    """

class SendingError(Exception):
    """
    Exception to be raised when a notification error happens
    """

class BrokerConnectionError(Exception):
    """
    Exception to be raised when the connection to a broker fails
    """

class SerializationError(Exception):
    """
    Exception to be raised when error happens during serialization
    """

class DeserializationError(Exception):
    """
    Exception to be raised when error happens during serialization
    """