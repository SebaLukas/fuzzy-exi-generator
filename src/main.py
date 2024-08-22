# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2024 Contributors to EVerest

import logging
import argparse
from pathlib import Path

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

    parser = argparse.ArgumentParser(description="Fuzzy exi generator")
    parser.add_argument('--exi-jar', type=Path, default=Path('EXICodec.jar'))

    args = parser.parse_args()

    ExiJarCodec().set_exi_codec(args.exi_jar)

    generate_supported_app_protocol()
