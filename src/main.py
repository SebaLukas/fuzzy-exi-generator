# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2024 Contributors to EVerest

import logging

from exi_codec import ExiJarCodec

from generator.supported_app_protocol import GeneratorSupportedAppProtocol

# FIXME(SL): Adding better logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_supported_app_protocol():
    logger.info("Generate")

    app_protocol_generator = GeneratorSupportedAppProtocol()
    app_protocol_generator.generate(10)

if __name__ == '__main__':

    # Create ExiCodec in src
    ExiJarCodec().set_exi_codec("EXICodec.jar")

    generate_supported_app_protocol()


# TODO(sl): add output arg and exicodec.jar filepath
