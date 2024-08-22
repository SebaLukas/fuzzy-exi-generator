# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2024 Contributors to EVerest

import logging
from builtins import Exception

logger = logging.getLogger(__name__)


class ExiJarCodec:

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ExiJarCodec, cls).__new__(cls)
            cls._instance.exi_codec = None
        return cls._instance

    def set_exi_codec(self, jar_file_path: str):
        from py4j.java_gateway import JavaGateway

        self.gateway = JavaGateway.launch_gateway(
            classpath=jar_file_path,
            die_on_exit=True,
            javaopts=["--add-opens", "java.base/java.lang=ALL-UNNAMED"],
        )

        self.exi_codec = self.gateway.jvm.com.siemens.ct.exi.main.cmd.EXICodec()

    def encode(self, message: str, namespace: str) -> bytes:
        exi = self.exi_codec.encode(message, namespace)

        if exi is None:
            raise Exception(self.exi_codec.get_last_encoding_error())
        return exi
