# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 SebaLukas

import logging
import argparse
from pathlib import Path

from exi_codec import ExiJarCodec

from generator.supported_app_protocol import GeneratorSupportedAppProtocol
from generator.din import GeneratorDIN
from generator.iso_2 import GeneratorIso2

# FIXME(SL): Adding better logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Fuzzy exi generator")
    parser.add_argument('--exi-jar', type=Path,
                        default=Path('src/EXICodec.jar'))
    parser.add_argument('--number-sap-msgs', type=int, default=10)
    parser.add_argument('--number-din-msgs', type=int, default=50)
    parser.add_argument('--number-iso2-msgs', type=int, default=50)

    args = parser.parse_args()

    ExiJarCodec().set_exi_codec(args.exi_jar)

    GeneratorSupportedAppProtocol().generate(args.number_sap_msgs)
    GeneratorDIN().generate(args.number_din_msgs)
    GeneratorIso2().generate(args.number_iso2_msgs)
