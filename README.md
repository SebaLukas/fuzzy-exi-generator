# fuzzy-exi-generator

This is a small fuzzy generator. It generates exi streams and matching json files for DIN70121, ISO15118-2 and -20 messages.
It uses the message definition from the `iso15118` project (https://github.com/EcoG-io/iso15118).

> Efficient XML Interchange (EXI) is a very compact representation for the Extensible Markup Language (XML) Information Set that is intended to simultaneously optimize performance and the utilization of computational resources
>
> -- <cite>Efficient XML Interchange (EXI) Format 1.0 (Second Edition) [1]</cite>

With this generator it is possible to generate thousands of different exi streams and matching json files to test EXI codec libraries. The DIN and ISO messages do not make sense for a charging process, but are still valid EXI streams that comply with the XSD.

## Usage

Install the necessary python packages using

```bash
python3 -m pip install -r requirements.txt
```

Use the following command to generate the exi streams and json files

```bash
python3 src/main.py
```

You can find the generated data in the `output` folder, saved as `.csv` files.

You can change the number of generated messages using the arguments

```bash
python3 src/main.py ---number-sap-msgs 5 --number-din-msgs 25 --number-iso2-msgs 40
```

## Status

The current generator status is described here, which messages can currently be generated.

### DIN70121 messages

| Messages (Req & Res)     | Status             |
|--------------------------|--------------------|
| SessionSetup             | :heavy_check_mark: |
| ServiceDiscovery         | :heavy_check_mark: |
| ServicePaymentSelectio   | :heavy_check_mark: |
| ContractAuthentication   | :heavy_check_mark: |
| ChargeParameterDiscovery | :heavy_check_mark: |
| PowerDelivery            | :heavy_check_mark: |
| CableCheck               | :heavy_check_mark: |
| PreCharge                | :heavy_check_mark: |
| CurrentDemand            | :heavy_check_mark: |
| WeldingDetection         | :heavy_check_mark: |
| SessionStop              | :heavy_check_mark: |

### ISO15118-2 messages

| Messages (Req & Res)     | Status             |
|--------------------------|--------------------|
| SessionSetup             | :heavy_check_mark: |
| ServiceDiscovery         | :heavy_check_mark: |
| ServiceDetail            | :heavy_check_mark: |
| PaymentServiceSelection  | :heavy_check_mark: |
| CertificateInstallation  |                    |
| CertificateUpdate        |                    |
| PaymentDetails           |                    |
| Authorization            | :heavy_check_mark: |
| ChargeParameterDiscovery |                    |
| PowerDelivery            |                    |
| ChargingStatus           | :heavy_check_mark: |
| MeteringReceipt          |                    |
| CableCheck               | :heavy_check_mark: |
| PreCharge                | :heavy_check_mark: |
| CurrentDemand            | :heavy_check_mark: |
| WeldingDetection         | :heavy_check_mark: |

### ISO15118-20 messages

| Messages (Req & Res)     | Status             |
|--------------------------|--------------------|
|                          |                    |

[1]: https://www.w3.org/TR/exi/

