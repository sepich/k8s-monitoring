#!/usr/bin/env python3
import sys
import yaml
import os


ALERTS = {}
alert = ''


def fail(msg):
    print(f'{alert}: {msg}')
    os._exit(1)


for f in sys.argv[1:]:
    print(f)
    with open(f, 'r') as stream:
        data = yaml.load(stream)
    if len(data['groups']) > 1:
        fail('More than one group in file')
    name = f.split('/')[-1].split('.')[-2]
    if data['groups'][0]['name'] != name:
        alert = ''
        fail(f'Group name should be {name}')

    for rule in data['groups'][0]['rules']:

        if not 'for' in rule:
            fail('"for" should be set for at least a minute!')
        if not 'severity' in rule['labels']:
            fail('"severity" label is missing')
        if rule['labels']['severity'] not in ['informational', 'warning', 'minor', 'major', 'critical']:
            fail('wrong value for severity: ' + rule['labels']['severity'])

        alert = rule['alert']
        if alert in ALERTS:
            if rule['labels']['severity'] in ALERTS[alert]:
                fail(f'same alert with severity {rule["labels"]["severity"]} already exist')
            ALERTS[alert].add(rule['labels']['severity'])
        else:
            ALERTS[alert] = {rule['labels']['severity']}

        for label in rule['labels']:
            if '$value' in label:
                fail('$value in labels would generate new alert each time')
        if 'environment' in rule['labels']:
            fail('labels.environment is already set in external_labels')
        if 'service' in rule['labels']:
            fail('labels.service would be overriden by $monitor')
        if 'description' not in rule['annotations']:
            fail('annotations.description is not set')
