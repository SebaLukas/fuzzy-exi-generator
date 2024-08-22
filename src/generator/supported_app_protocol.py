# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Pionix GmbH and Contributors to EVerest

import json
from base64 import b64encode
from pathlib import Path

import pandas as pd

from exi_codec import ExiJarCodec

from config import output_dir

from iso15118.shared.messages.enums import Namespace
from iso15118.shared.messages import BaseModel
from iso15118.shared.messages.app_protocol import SupportedAppProtocolReq, SupportedAppProtocolRes

from polyfactory.factories.pydantic_factory import ModelFactory


class CustomJSONEncoder(json.JSONEncoder):
    """
    Custom JSON encoder to allow the encoding of raw bytes to Base64 encoded
    strings to conform with their XSD type base64Binary. Also, JSON cannot
    encode bytes by default, so the base64Binary type comes in handy.
    """

    # pylint: disable=method-hidden
    def default(self, o):
        if isinstance(o, bytes):
            return b64encode(o).decode()
        return json.JSONEncoder.default(self, o)


class SupportedAppProtocolReqFactory(ModelFactory[SupportedAppProtocolReq]):
    ...


class SupportedAppProtocolResFactory(ModelFactory[SupportedAppProtocolRes]):
    ...


def convert_msg_to_dict(msg_element: BaseModel) -> dict:
    msg_to_dct: dict = msg_element.dict(by_alias=True, exclude_none=True)
    return {str(msg_element): msg_to_dct}


# Better return tuple with Exi bytes and json
class GeneratorSupportedAppProtocol:
    def __generate_req(self) -> tuple[bytes, dict]:
        req_dict = convert_msg_to_dict(SupportedAppProtocolReqFactory.build())
        req_json = json.dumps(req_dict, cls=CustomJSONEncoder)
        stream = ExiJarCodec().encode(req_json, Namespace.SAP)

        return stream, req_json

    def __generate_res(self) -> tuple[bytes, dict]:
        res_dict = convert_msg_to_dict(SupportedAppProtocolResFactory.build())
        res_json = json.dumps(res_dict, cls=CustomJSONEncoder)
        stream = ExiJarCodec().encode(res_json, Namespace.SAP)

        return stream, res_json

    def generate(self, no_of_messages: int):

        bytes_list = []
        json_list = []

        for _ in range(0, no_of_messages):
            req = self.__generate_req()
            res = self.__generate_res()

            bytes_list.extend([req[0].hex(), res[0].hex()])
            json_list.extend([req[1], res[1]])

        df = pd.DataFrame(
            {
                "exi_stream": bytes_list,
                "exi_json": json_list,
            }
        )

        filepath = Path(f"{output_dir}/app_protocol.csv")
        filepath.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(filepath, index=False)
