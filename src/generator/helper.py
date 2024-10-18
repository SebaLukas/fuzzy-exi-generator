# SPDX-License-Identifier: Apache-2.0
# Copyright 2024 SebaLukas

import secrets

def get_random_bytes(nbytes: int) -> bytes:
    # TODO(SL): move to another file
    return secrets.token_bytes(nbytes)