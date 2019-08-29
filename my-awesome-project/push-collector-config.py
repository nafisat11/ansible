#!/usr/bin/python3

import argparse
import json
import os
import urllib.request
import uuid

def _build_playbook(filenames):
    return """
- hosts: all
  tasks:
    - block:
      - name: make system writable
        shell: /usr/sbin/rw
        
      - name: remove old collector config
        shell: /bin/rm -rf /etc/3d-p/iep-collector/tests-enabled/*
        
      - name: install new collector config
        copy:
          src: "{{{{ ce__local_blob_path }}}}/{{{{ item.src }}}}"
          dest: "/etc/3d-p/iep-collector/tests-enabled/{{{{ item.dest }}}}"
        with_items:
          {jinja_items}
          
      - name: restart collector
        service:
          name: iep-collector
          state: restarted
          
      always:
        - name: make system read-only
          shell: /usr/sbin/ro
""".strip().format(
    jinja_items='\n      '.join(
        "- {{ src: '{src}', dest: '{dest}' }}".format(
            src=filename,
            dest=filename,
        )
        for filename in filenames
    )
)

def issue_task(server_uri, files, hosts):
    boundary = '----------3DP_FoRmD4t@Deelymutor_{uuid}_$'.format(
        uuid=uuid.uuid1().hex,
    )
    boundary_delimiter = '--{boundary}'.format(boundary=boundary)
    
    output_body = [
        boundary_delimiter,
        'Content-Disposition: form-data; name="data"',
        '',
        json.dumps({
            'instructions': _build_playbook((os.path.basename(f) for f in files)),
            'hosts': hosts,
            'name': 'push collector config',
        }),
    ]
    
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
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Push collector configurations to multiple hosts')
    parser.add_argument(
        '--file', dest='files', nargs='+', required=True,
        help='a file to be pushed',
    )
    parser.add_argument(
        '--host', dest='hosts', nargs='+',
        help='a host to which files should be pushed', required=True,
    )
    parser.add_argument(
        '--server_uri', dest='server_uri', default='http://10.0.2.4:8080/load',
        help='a host to which files should be pushed',
    )
    args = parser.parse_args()
    
    issue_task(args.server_uri, args.files, args.hosts)
    
