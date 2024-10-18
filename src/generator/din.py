# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 SebaLukas

import json
from pathlib import Path
import pandas as pd
from builtins import Exception
from progress.bar import Bar

from exi_codec import CustomJSONEncoder, ExiJarCodec

from generator.helper import get_random_bytes

from config import output_dir

from iso15118.shared.messages.enums import Namespace
from iso15118.shared.messages import BaseModel
from iso15118.shared.messages.din_spec.datatypes import ResponseCode
from iso15118.shared.messages.din_spec.body import (
    Body,
    SessionSetupReq, SessionSetupRes,
    ServiceDiscoveryReq, ServiceDiscoveryRes,
    ServicePaymentSelectionReq, ServicePaymentSelectionRes,
    ContractAuthenticationReq, ContractAuthenticationRes,
    ChargeParameterDiscoveryReq, ChargeParameterDiscoveryRes,
    PowerDeliveryReq, PowerDeliveryRes,
    CableCheckReq, CableCheckRes,
    PreChargeReq, PreChargeRes,
    CurrentDemandReq, CurrentDemandRes,
    WeldingDetectionReq, WeldingDetectionRes,
    SessionStopReq, SessionStopRes,
)
from iso15118.shared.messages.din_spec.msgdef import V2GMessage
from iso15118.shared.messages.din_spec.header import MessageHeader

from polyfactory.factories.pydantic_factory import ModelFactory


class SessionSetupReqFactory(ModelFactory[SessionSetupReq]):
    ...


class SessionSetupResFactory(ModelFactory[SessionSetupRes]):
    ...


class ServiceDiscoveryReqFactory(ModelFactory[ServiceDiscoveryReq]):
    ...


class ServiceDiscoveryResFactory(ModelFactory[ServiceDiscoveryRes]):
    ...


class ServicePaymentSelectionReqFactory(ModelFactory[ServicePaymentSelectionReq]):
    ...


class ServicePaymentSelectionResFactory(ModelFactory[ServicePaymentSelectionRes]):
    ...


class ContractAuthenticationReqFactory(ModelFactory[ContractAuthenticationReq]):
    ...


class ContractAuthenticationResFactory(ModelFactory[ContractAuthenticationRes]):
    ...


class ChargeParameterDiscoveryReqFactory(ModelFactory[ChargeParameterDiscoveryReq]):
    ...


class ChargeParameterDiscoveryResFactory(ModelFactory[ChargeParameterDiscoveryRes]):
    ...


class PowerDeliveryReqFactory(ModelFactory[PowerDeliveryReq]):
    ...


class PowerDeliveryResFactory(ModelFactory[PowerDeliveryRes]):
    ...


class CableCheckReqFactory(ModelFactory[CableCheckReq]):
    ...


class CableCheckResFactory(ModelFactory[CableCheckRes]):
    ...


class PreChargeReqFactory(ModelFactory[PreChargeReq]):
    ...


class PreChargeResFactory(ModelFactory[PreChargeRes]):
    ...


class CurrentDemandReqFactory(ModelFactory[CurrentDemandReq]):
    ...


class CurrentDemandResFactory(ModelFactory[CurrentDemandRes]):
    ...


class WeldingDetectionReqFactory(ModelFactory[WeldingDetectionReq]):
    ...


class WeldingDetectionResFactory(ModelFactory[WeldingDetectionRes]):
    ...


class SessionStopReqFactory(ModelFactory[SessionStopReq]):
    ...


class SessionStopResFactory(ModelFactory[SessionStopRes]):
    ...


generators_list = [
    [SessionSetupReqFactory, SessionSetupResFactory],
    [ServiceDiscoveryReqFactory, ServiceDiscoveryResFactory],
    [ServicePaymentSelectionReqFactory, ServicePaymentSelectionResFactory],
    [ContractAuthenticationReqFactory, ContractAuthenticationResFactory],
    [ChargeParameterDiscoveryReqFactory, ChargeParameterDiscoveryResFactory],
    [PowerDeliveryReqFactory, PowerDeliveryResFactory],
    [CableCheckReqFactory, CableCheckResFactory],
    [PreChargeReqFactory, PreChargeResFactory],
    [CurrentDemandReqFactory, CurrentDemandResFactory],
    [WeldingDetectionReqFactory, WeldingDetectionResFactory],
    [SessionStopResFactory, SessionStopReqFactory],
]


def convert_msg_to_dict(msg_element: BaseModel) -> dict:
    # TODO(sl): Refactoring in another file
    body: Body = Body.parse_obj(
        {str(msg_element): msg_element.dict()}
    )
    header = MessageHeader(SessionID=get_random_bytes(8).hex().upper())
    msg: V2GMessage = V2GMessage(header=header, body=body)
    msg_to_dct: dict = msg.dict(by_alias=True, exclude_none=True)

    return {"V2G_Message": msg_to_dct}


def generate_json_and_exi(msg: BaseModel) -> tuple[bytes, str]:
    msg_dict = convert_msg_to_dict(msg)
    msg_json = json.dumps(msg_dict, cls=CustomJSONEncoder)
    msg_stream = ExiJarCodec().encode(msg_json, Namespace.DIN_MSG_DEF)

    return msg_stream.hex(), msg_json


class GeneratorDIN:
    def __generate(self, req_factory, res_factory) -> tuple[list[bytes], list[str]]:
        done: bool = False

        while not done:
            try:
                req = generate_json_and_exi(req_factory.build())
                res = generate_json_and_exi(res_factory.build())
                done = True
            # TODO(sl): Check every Exception for every DIN Message
            except (ValueError, Exception):
                continue

        return [req[0], res[0]], [req[1], res[1]]

    def generate(self, no_of_msgs: int):

        message_list = []
        bytes_list = []
        json_list = []

        with Bar('Generate DIN messages', max=no_of_msgs) as bar:
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

        filepath = Path(f"{output_dir}/din.csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
