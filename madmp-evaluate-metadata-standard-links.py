import json

import click
import requests

FAIRSHARING_ENDPOINT = 'https://api.fairsharing.org'


def extract_metadata(madmp_json):
    dmp = madmp_json['dmp']
    datasets = dmp['dataset']
    metadata_identifiers = []
    for dataset in datasets:
        if dataset.get('metadata') is not None:
            for metadata in dataset.get('metadata'):
                if metadata is not None:
                    metadata_identifiers.append(metadata["metadata_standard_id"]["identifier"])
    return metadata_identifiers


def get_fairsharing_token(username, password):
    url = FAIRSHARING_ENDPOINT + "/users/sign_in"
    payload = "{\"user\": {\"login\":\"" + username + "\",\"password\":\"" + password + "\"} }"
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    # Get the JWT from the response.text to use in the next part.
    data = response.json()
    return data['jwt']


def get_fairsharing_standards(username, password):
    jwt_token = get_fairsharing_token(username, password)
    url = FAIRSHARING_ENDPOINT + "/fairsharing_records?fairsharing_registry=standards&page[size]=1000000"
    headers = {'Authorization': 'Bearer ' + jwt_token, 'Accept': 'application/json'}
    res = requests.get(url=url, headers=headers)
    res.raise_for_status()
    return res.json()


@click.command()
@click.argument('madmp', type=click.File(mode='r'))
@click.option('--fairsharing-username', type=str,
              help='FAIRsharing username.')
@click.option('--fairsharing-password', type=str,
              help='FAIRsharing password.')
def cli(madmp, fairsharing_username, fairsharing_password):
    metadata_identifiers = []
    try:
        madmp_json = json.load(madmp)
        metadata_identifiers = extract_metadata(madmp_json)
    except KeyError as e:
        click.echo(f'Invalid maDMP in JSON: {str(e)}', err=True)
    except Exception as e:
        click.echo(f'Cannot parse JSON: {str(e)}', err=True)
    results = {}
    for metadata_identifier in metadata_identifiers:
        faisharing_standards = get_fairsharing_standards(fairsharing_username, fairsharing_password)
        results[metadata_identifier] = False
        for faisharing_standard in faisharing_standards["data"]:
            doi = metadata_identifier.replace("https://doi.org/", "")
            if faisharing_standard.get("attributes") is not None \
                    and faisharing_standard.get("attributes").get("metadata") is not None \
                    and faisharing_standard.get("attributes").get("metadata").get("doi") == doi:
                results[metadata_identifier] = True
    for (metadata_identifier, result) in results.items():
        if result:
            echo = click.style(
                f'PASSED: Metadata Standard with the following DOI ({metadata_identifier}) exists in the FAIRsharing registry.',
                fg='green')
            click.echo(echo)
        else:
            echo = click.style(
                f'FAILED: Metadata Standard with the following DOI ({metadata_identifier}) does not exists in the FAIRsharing registry.',
                fg='red')
            click.echo(echo)


if __name__ == '__main__':
    cli()
