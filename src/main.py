# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2024 Contributors to EVerest

import logging
import argparse
from pathlib import Path

from exi_codec import ExiJarCodec

from generator.supported_app_protocol import GeneratorSupportedAppProtocol
from generator.din import GeneratorDIN

# FIXME(SL): Adding better logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def generate_supported_app_protocol():
    app_protocol_generator = GeneratorSupportedAppProtocol()
    app_protocol_generator.generate(10)

def generate_din():
    din_generator = GeneratorDIN()
    din_generator.generate(50)

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Fuzzy exi generator")
    parser.add_argument('--exi-jar', type=Path, default=Path('src/EXICodec.jar'))

    args = parser.parse_args()

    ExiJarCodec().set_exi_codec(args.exi_jar)

    generate_supported_app_protocol()
    generate_din()
