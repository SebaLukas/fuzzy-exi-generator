# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 SebaLukas

import json
from pathlib import Path
import pandas as pd
from builtins import Exception
from progress.bar import Bar
import time

from exi_codec import CustomJSONEncoder, ExiJarCodec

from generator.helper import get_random_bytes

from config import output_dir

from iso15118.shared.messages.enums import Namespace
from iso15118.shared.messages import BaseModel
from iso15118.shared.messages.iso15118_20.common_messages import (
    SessionSetupReq, SessionSetupRes,
    AuthorizationSetupReq, AuthorizationSetupRes,
    AuthorizationReq, AuthorizationRes,
    ServiceDiscoveryReq, ServiceDiscoveryRes,
    ServiceDetailReq, ServiceDetailRes,
    ServiceSelectionReq, ServiceSelectionRes,
    ScheduleExchangeReq, ScheduleExchangeRes,
    PowerDeliveryReq, PowerDeliveryRes,
    MeteringConfirmationReq, MeteringConfirmationRes,
    SessionStopReq, SessionStopRes,
    CertificateInstallationReq, CertificateInstallationRes,
)
from iso15118.shared.messages.iso15118_20.ac import (
    ACChargeParameterDiscoveryReq, ACChargeParameterDiscoveryRes,
    ACChargeLoopReq, ACChargeLoopRes,
)
from iso15118.shared.messages.iso15118_20.dc import (
    DCChargeParameterDiscoveryReq, DCChargeParameterDiscoveryRes,
    DCChargeLoopReq, DCChargeLoopRes,
    DCCableCheckReq, DCCableCheckRes,
    DCPreChargeReq, DCPreChargeRes,
    DCWeldingDetectionReq, DCWeldingDetectionRes,
)

from polyfactory.factories.pydantic_factory import ModelFactory


class SessionSetupReqFactory(ModelFactory[SessionSetupReq]):
    ...


class SessionSetupResFactory(ModelFactory[SessionSetupRes]):
    ...


class AuthorizationSetupReqFactory(ModelFactory[AuthorizationSetupReq]):
    ...


class AuthorizationSetupResFactory(ModelFactory[AuthorizationSetupRes]):
    ...


class AuthorizationReqFactory(ModelFactory[AuthorizationReq]):
    ...


class AuthorizationResFactory(ModelFactory[AuthorizationRes]):
    ...


class ServiceDiscoveryReqFactory(ModelFactory[ServiceDiscoveryReq]):
    ...


class ServiceDiscoveryResFactory(ModelFactory[ServiceDiscoveryRes]):
    ...


class ServiceDetailReqFactory(ModelFactory[ServiceDetailReq]):
    ...


class ServiceDetailResFactory(ModelFactory[ServiceDetailRes]):
    ...


class ServiceSelectionReqFactory(ModelFactory[ServiceSelectionReq]):
    ...


class ServiceSelectionResFactory(ModelFactory[ServiceSelectionRes]):
    ...


class ScheduleExchangeReqFactory(ModelFactory[ScheduleExchangeReq]):
    ...


class ScheduleExchangeResFactory(ModelFactory[ScheduleExchangeRes]):
    ...


class PowerDeliveryReqFactory(ModelFactory[PowerDeliveryReq]):
    ...


class PowerDeliveryResFactory(ModelFactory[PowerDeliveryRes]):
    ...


class MeteringConfirmationReqFactory(ModelFactory[MeteringConfirmationReq]):
    ...


class MeteringConfirmationResFactory(ModelFactory[MeteringConfirmationRes]):
    ...


class SessionStopReqFactory(ModelFactory[SessionStopReq]):
    ...


class SessionStopResFactory(ModelFactory[SessionStopRes]):
    ...


class CertificateInstallationReqFactory(ModelFactory[CertificateInstallationReq]):
    ...


class CertificateInstallationResFactory(ModelFactory[CertificateInstallationRes]):
    ...


class ACChargeParameterDiscoveryReqFactory(ModelFactory[ACChargeParameterDiscoveryReq]):
    ...


class ACChargeParameterDiscoveryResFactory(ModelFactory[ACChargeParameterDiscoveryRes]):
    ...


class ACChargeLoopReqFactory(ModelFactory[ACChargeLoopReq]):
    ...


class ACChargeLoopResFactory(ModelFactory[ACChargeLoopRes]):
    ...


class DCChargeParameterDiscoveryReqFactory(ModelFactory[DCChargeParameterDiscoveryReq]):
    ...


class DCChargeParameterDiscoveryResFactory(ModelFactory[DCChargeParameterDiscoveryRes]):
    ...


class DCChargeLoopReqFactory(ModelFactory[DCChargeLoopReq]):
    ...


class DCChargeLoopResFactory(ModelFactory[DCChargeLoopRes]):
    ...


class DCCableCheckReqFactory(ModelFactory[DCCableCheckReq]):
    ...


class DCCableCheckResFactory(ModelFactory[DCCableCheckRes]):
    ...


class DCPreChargeReqFactory(ModelFactory[DCPreChargeReq]):
    ...


class DCPreChargeResFactory(ModelFactory[DCPreChargeRes]):
    ...


class DCWeldingDetectionReqFactory(ModelFactory[DCWeldingDetectionReq]):
    ...


class DCWeldingDetectionResFactory(ModelFactory[DCWeldingDetectionRes]):
    ...


generators_list = [
    [SessionSetupReqFactory, SessionSetupResFactory],
    # [AuthorizationSetupReqFactory, AuthorizationSetupResFactory],
    # [AuthorizationReqFactory, AuthorizationResFactory],
    [ServiceDiscoveryReqFactory, ServiceDiscoveryResFactory],
    # [ServiceDetailReqFactory, ServiceDetailResFactory],
    [ServiceSelectionReqFactory, ServiceSelectionResFactory],
    # [ScheduleExchangeReqFactory, ScheduleExchangeResFactory],
    # [PowerDeliveryReqFactory, PowerDeliveryResFactory],
    # [MeteringConfirmationReqFactory, MeteringConfirmationResFactory],
    [SessionStopReqFactory, SessionStopResFactory],
    # [CertificateInstallationReqFactory, CertificateInstallationResFactory],
    # [ACChargeParameterDiscoveryReqFactory, ACChargeParameterDiscoveryResFactory],
    # [ACChargeLoopReqFactory, ACChargeLoopResFactory],
    # [DCChargeParameterDiscoveryReqFactory, DCChargeParameterDiscoveryResFactory],
    # [DCChargeLoopReqFactory, DCChargeLoopResFactory],
    [DCCableCheckReqFactory, DCCableCheckResFactory],
    [DCPreChargeReqFactory, DCPreChargeResFactory],
    [DCWeldingDetectionReqFactory, DCWeldingDetectionResFactory],
]

def convert_msg_to_dict(msg_element: BaseModel) -> dict:
    # ISO15118-20 messages already include the header in their structure
    # We need to ensure the header has proper SessionID and timestamp
    msg_dict = msg_element.dict(by_alias=True, exclude_none=True)
    
    # Update header with proper SessionID and timestamp if it exists
    if "Header" in msg_dict:
        msg_dict["Header"]["SessionID"] = get_random_bytes(8).hex().upper()
        msg_dict["Header"]["TimeStamp"] = int(time.time())
        # Remove Signature field as it's not needed for our test data generation
        msg_dict["Header"].pop("Signature", None)

    return {str(msg_element): msg_dict}

def get_namespace_for_message(msg: BaseModel) -> str:
    """Determine the correct namespace for a given ISO15118-20 message type"""
    msg_type = type(msg).__name__
    
    # AC-specific messages
    if msg_type.startswith('AC'):
        return Namespace.ISO_V20_AC
    # DC-specific messages  
    elif msg_type.startswith('DC'):
        return Namespace.ISO_V20_DC
    # Common messages (everything else)
    else:
        return Namespace.ISO_V20_COMMON_MSG


def generate_json_and_exi(msg: BaseModel) -> tuple[bytes, str]:
    msg_dict = convert_msg_to_dict(msg)
    msg_json = json.dumps(msg_dict, cls=CustomJSONEncoder)
    namespace = get_namespace_for_message(msg)
    msg_stream = ExiJarCodec().encode(msg_json, namespace)

    return msg_stream.hex(), msg_json

class GeneratorIso20:
    def __generate(self, req_factory, res_factory) -> tuple[list[bytes], list[str]]:

        while True:
            try:
                req = generate_json_and_exi(req_factory.build())
                res = generate_json_and_exi(res_factory.build())
                return [req[0], res[0]], [req[1], res[1]]
            except ValueError:
                continue
                # print(f"ValueError: {repr(v_error)}")
            except Exception:
                continue
                # print(f"Exception: {repr(e)}, {e}")

    def generate(self, no_of_msgs: int):

        message_list = []
        bytes_list = []
        json_list = []

        with Bar('Generate ISO-20 messages', max=no_of_msgs) as bar:
            for i in range(0, no_of_msgs):
                for generators in generators_list:
                    messages = self.__generate(generators[0], generators[1])
                    message_list.extend(
                        [generators[0].__model__.__name__, generators[1].__model__.__name__])
                    bytes_list.extend(messages[0])
                    json_list.extend(messages[1])
                bar.next()

        df = pd.DataFrame(
            {
                "message": message_list,
                "exi_stream": bytes_list,
                "exi_json": json_list,
            }
        )

        filepath = Path(f"{output_dir}/iso20.csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)

