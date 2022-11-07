# maDMP Metadata Standard Link Evaluation Example

*Example evaluator of metadata standard links for maDMPs according to [RDA DMP Common Standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard)*

## Motivation and Objectives

This machine-actionable DMP evaluator prototype serves to check if the metadata standard links from maDMP created according to the [RDA DMP Common Standard](https://github.com/RDA-DMP-Common/RDA-DMP-Common-Standard) exist in some acknowledged sources. You can provide any such DMP as input for the evaluator (you can also use the provided [examples](./examples/)). The evaluator will extract every metadata standard identifier (JSON path `dmp/dataset/metadata/metadata_standard_id/identifier`) and check its existence in the [FAIRsharing](https://api.fairsharing.org/) Registry. As a result, information about passed/failed tests is presented for each metadata standard in the DMP. 

## Requirements

* Python 3.6+ (preferably used with [virtualenv](https://docs.python.org/3/library/venv.html))

## Usage

### Install dependencies

```
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
```

Alternatively, on Windows:

```
python -m venv env
env\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### Get help

```shell
python madmp-evaluate-metadata-standard-links.py --help
```

### Evaluate

```shell
python madmp-evaluate-metadata-standard-links.py examples/madmp.json --fairsharing-username=<username> --fairsharing-password=<password>
```

Example output:

```
FAILED: Metadata Standard with the following DOI (http://example.com/my-metadata-standard) does not exists in the FAIRsharing registry.
PASSED: Metadata Standard with the following DOI (https://doi.org/10.25504/FAIRsharing.1esk4f) exists in the FAIRsharing registry.
```

## License

This project is licensed under the Apache License v2.0 - see the
[LICENSE](LICENSE) file for more details.
