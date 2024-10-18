# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 Pionix GmbH and Contributors to EVerest

import logging
from builtins import Exception
import json
from base64 import b64encode
from pathlib import Path

logger = logging.getLogger(__name__)


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


class ExiJarCodec:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExiJarCodec, cls).__new__(cls)
            cls._instance.exi_codec = None
        return cls._instance

    def set_exi_codec(self, jar_file_path: Path):
        from py4j.java_gateway import JavaGateway

        if not jar_file_path.exists() or not jar_file_path.is_file():
            raise Exception(f'Exi codec jar file {jar_file_path.resolve()} does not exist')

        self.gateway = JavaGateway.launch_gateway(
            classpath=str(jar_file_path.absolute()),
            die_on_exit=True,
            javaopts=["--add-opens", "java.base/java.lang=ALL-UNNAMED"],
        )

        self.exi_codec = self.gateway.jvm.com.siemens.ct.exi.main.cmd.EXICodec()

    def encode(self, message: str, namespace: str) -> bytes:
        exi = self.exi_codec.encode(message, namespace)

        if exi is None:
            raise Exception(self.exi_codec.get_last_encoding_error())
        return exi
