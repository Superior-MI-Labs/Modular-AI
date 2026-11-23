#!/usr/bin/env python3
"""Static review of the illustrative manifest and registry contracts.

Only checks design examples. Does not instantiate or train model implementations.
Optional: `pip install jsonschema` for full JSON schema verification.
"""
from pathlib import Path
import json

root=Path(__file__).resolve().parents[1]
registry=json.loads((root/'registry/reference_modules.json').read_text())['modules']
schema=json.loads((root/'schemas/experiment.schema.json').read_text())
try:
    from jsonschema import Draft202012Validator
except ImportError:
    Draft202012Validator=None


def check_eq(left,right,what):
    if left != right:
        raise AssertionError(f'{what}: incompatible ports {left} != {right}')


def verify(path):
    ex=json.loads(path.read_text())
    if Draft202012Validator:
        Draft202012Validator(schema).validate(ex)
    assert ex['schema_version']==1
    wf=registry[ex['workflow']['use']]
    slots=ex['workflow']['slots']
    for required in wf['slots']:
        assert required in slots,f'missing {required}'
    for slot,module_id in slots.items():
        assert slot in wf['slots']+wf.get('optional_slots',[]),f'unexpected slot {slot}'
        assert module_id in registry,f'unknown module {module_id}'
    r=lambda name:registry[slots[name]]
    if ex['workflow']['use']=='ref.workflow.episode@1':
        if 'state_encoder' in slots:
            check_eq(r('environment')['output']['observation'],r('state_encoder')['input']['observation'],'environment -> state encoder')
            check_eq(r('state_encoder')['output']['state'],r('policy')['input']['observation'],'state encoder -> policy')
        else:
            check_eq(r('environment')['output']['observation'],r('policy')['input']['observation'],'environment -> policy')
        check_eq(r('policy')['output']['action'],r('environment')['input']['action'],'policy -> environment')
    elif ex['workflow']['use']=='ref.workflow.autoregressive@1':
        check_eq(r('tokenizer')['output']['token_ids'],r('predictor')['input']['token_ids'],'tokenizer -> predictor')
        check_eq(r('predictor')['output']['logits'],r('sampler')['input']['logits'],'predictor -> sampler')
        check_eq(r('sampler')['output']['token_ids'],r('decoder')['input']['token_ids'],'sampler -> decoder')
    elif ex['workflow']['use'] in ('ref.workflow.iterative-image@1','ref.workflow.iterative-video@1'):
        net='denoiser' if 'denoiser' in slots else 'video_denoiser'
        check_eq(r('conditioner')['output']['conditioning'],r(net)['input']['conditioning'],'conditioner -> denoiser')
        check_eq(r(net)['output']['estimate'],r('scheduler')['input']['prediction'],'denoiser -> scheduler')
        check_eq(r('scheduler')['output']['latent'],r(net)['input']['latent'],'scheduler -> denoiser latent')
        check_eq(r('scheduler')['output']['latent'],r('codec')['input']['latent'],'scheduler -> codec')
    else:
        raise AssertionError('unreviewed workflow '+ex['workflow']['use'])
    return ex['experiment_id']


if __name__=='__main__':
    files=sorted((root/'examples').glob('*.json'))
    for f in files:
        print('PASS',verify(f))
    mermaids=sorted((root/'diagrams/mermaid').glob('*.mmd'))
    svgs=sorted((root/'diagrams/svg').glob('*.svg'))
    assert len(mermaids)==20 and len(svgs)==20
    assert {x.stem for x in mermaids}=={x.stem for x in svgs}
    print(f'PASS {len(files)} sample manifests, {len(mermaids)} Mermaid and SVG diagrams')
