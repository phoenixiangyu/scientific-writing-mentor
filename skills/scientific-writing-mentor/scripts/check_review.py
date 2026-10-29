#!/usr/bin/env python3
"""Check clean-text / editorial-issue separation; does not judge scientific truth."""
import argparse
import json
from pathlib import Path
import re
import sys

KINDS={'evidence','citation','data','method','statistics','logic','venue'}
FIELDS={'id','anchor','location','kind','severity','question','needed','status'}
PLACEHOLDERS=[r'\[\s*(?:TODO|TBD|CITATION NEEDED|待补充|待核实)[^\]]*\]',r'\{\{\s*(?:TODO|TBD)[^}]*\}\}']

def validate(draft, payload, final=False):
    errors=[]
    if not isinstance(payload,dict) or not isinstance(payload.get('issues'),list):
        return ['Issue file must be an object with an issues array.']
    for pattern in PLACEHOLDERS:
        if re.search(pattern,draft,re.I):
            errors.append('An editorial placeholder remains in the clean draft.')
    identifiers=set()
    for index,issue in enumerate(payload['issues'],1):
        if not isinstance(issue,dict):
            errors.append(f'Issue {index} must be an object.')
            continue
        if FIELDS-set(issue):
            errors.append(f'Issue {index} missing fields: {sorted(FIELDS-set(issue))}')
            continue
        if any(not isinstance(issue[k],str) or not issue[k].strip() for k in FIELDS):
            errors.append(f'Issue {index} fields must be nonempty strings.')
            continue
        key=issue['id']
        if key in identifiers:
            errors.append(f'Duplicate issue id: {key}')
        identifiers.add(key)
        if issue['anchor'] not in draft:
            errors.append(f'{key}: anchor is absent from the draft.')
        if issue['kind'] not in KINDS or issue['severity'] not in {'blocking','advisory'} or issue['status'] not in {'open','resolved'}:
            errors.append(f'{key}: invalid kind, severity or status.')
        if final and issue['severity']=='blocking' and issue['status']=='open':
            errors.append(f'{key}: unresolved blocking issue.')
    return errors

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('draft',type=Path)
    parser.add_argument('issues',type=Path)
    parser.add_argument('--final',action='store_true',help='Also reject open blocking issues.')
    args=parser.parse_args()
    try:
        draft=args.draft.read_text(encoding='utf-8-sig')
        payload=json.loads(args.issues.read_text(encoding='utf-8-sig'))
        errors=validate(draft,payload,args.final)
    except (OSError,ValueError) as exc:
        errors=[str(exc)]
    print(json.dumps({'ok':not errors,'mode':'final' if args.final else 'draft','errors':errors},ensure_ascii=False))
    return 1 if errors else 0

if __name__=='__main__':
    sys.exit(main())
