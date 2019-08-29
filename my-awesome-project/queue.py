#!/usr/bin/python3

import argparse
import io
import json
import os
import tarfile
import urllib.request
import uuid

def _issue_task(server_uri, payload, files, roles):
    boundary = '----------3DP_FoRmD4t@Deelymutor_{uuid}_$'.format(
        uuid=uuid.uuid1().hex,
    )
    boundary_delimiter = '--{boundary}'.format(boundary=boundary)
    
    output_body = [
        boundary_delimiter,
        'Content-Disposition: form-data; name="data"',
        '',
        payload,
    ]
    
    for role_path in roles:
        role_archive_stream = io.StringIO()
        role_archive = tarfile.open(mode='w:gz', fileobj=role_archive_stream)
        role_archive.add(role_path)
        role_archive.close()
        role_archive_stream.seek(0)
        
        output_body.extend((
            boundary_delimiter,
            'Content-Disposition: form-data; name="roles"; filename="{}"'.format(
                os.path.basename(role_path),
            ),
            '',
            role_archive_stream.getvalue(),
        ))
        
        del role_archive
        role_archive_stream.close()
        del role_archive_stream
        
    for file_path in files:
        output_body.extend((
            boundary_delimiter,
            'Content-Disposition: form-data; name="files"; filename="{}"'.format(
                os.path.basename(file_path),
            ),
            '',
            open(file_path, 'rb').read(),
        ))
        
    output_body.extend((
        boundary_delimiter + '--',
        '',
    ))

    output_body = '\r\n'.join(output_body)
    
    request = urllib.request.Request(
        url=server_uri,
        data=output_body,
        headers={
            'Content-Type': 'multipart/form-data; boundary={boundary}'.format(boundary=boundary),
        }
    )
    
    urllib.request.urlopen(request)
    
def issue_task(server, playbook, hosts, retry, name, files, roles):
    return _issue_task(
        server_uri=(server + 'load-multi'),
        payload=json.dumps({
            'instructions': playbook,
            'hosts': hosts,
            'retry': retry,
            'name': name,
        }),
        files=files,
        roles=roles,
    )
    
def issue_task_single(server, playbook, host, retry, name, files, roles):
    return _issue_task(
        server_uri=(server + 'load-single'),
        payload=json.dumps({
            'instructions': playbook,
            'host': host,
            'retry': retry,
            'name': name,
        }),
        files=files,
        roles=roles,
    )
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run Ansible logic over a fleet')
    parser.add_argument(
        '--playbook', metavar='FILE',
        help='an Ansible playbook to be executed', required=True,
    )
    parser.add_argument(
        '--hosts', metavar='FILE',
        help='a linebreak-delimited list of hosts over which to run the playbook', required=True,
    )
    parser.add_argument(
        '--name',
        help='a symbolic name for this operation',
    )
    parser.add_argument(
        '--file', dest='files', nargs='*', metavar='FILE',
        help='a file to be pushed for use in executing the playbook',
    )
    parser.add_argument(
        '--role', dest='roles', nargs='*', metavar='ROLES',
        help='a role-directory for use in executing the playbook',
    )
    parser.add_argument(
        '--single', dest='multi', action='store_false',
        help='use single-host (priority) mode',
    )
    parser.add_argument(
        '--no-retry', dest='retry', action='store_false',
        help='prevent the playbook from being retried on failue (never a good idea in production)',
    )
    parser.add_argument(
        '--server', default='http://localhost:46092/',
        help='the address to deliver the playbook and any related files',
    )
    args = parser.parse_args()
    if args.files is None:
        args.files = []
    if args.roles is None:
        args.roles = []
        
    hosts = []
    with open(args.hosts, 'rb') as hostsfile:
        for host in hostsfile:
            host = host.strip()
            if host:
                hosts.append(host)
                
    if args.multi:
        issue_task(
            server=args.server,
            playbook=open(args.playbook, 'rb').read().strip(),
            hosts=hosts,
            retry=args.retry,
            name=args.name,
            files=args.files,
            roles=args.roles,
        )
    else:
        playbook = open(args.playbook, 'rb').read().strip()
        for host in hosts:
            issue_task_single(
                server=args.server,
                playbook=playbook,
                host=host,
                retry=args.retry,
                name=args.name,
                files=args.files,
                roles=args.roles,
            )
            
