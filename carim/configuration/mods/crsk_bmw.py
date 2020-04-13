import logging
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types

log = logging.getLogger(__name__)


@decorators.register
@decorators.mod('@[CrSk] BMW 525i E34')
@decorators.profile
def crsk_bmw_types():
    new_types = ElementTree.parse('resources/original-mod-files/[CrSk] BMW 525i E34/types.xml')
    types.get().getroot().extend(new_types.getroot())
