#!/usr/bin/python3

import argparse
import json
import os
import time
import urllib.request, urllib.error, urllib.parse
import uuid

def _issue_request(server_uri, payload='{}'):
    request = urllib.request.Request(
        url=server_uri,
        data=urllib.parse.urlencode({
            'data': payload,
        }),
    )
    return urllib.request.urlopen(request).read()
    
def pause(server):
    _issue_request(
        server_uri=(server + "pause"),
    )
    
def restart(server):
    _issue_request(
        server_uri=(server + "restart"),
    )
    
def list_tasks(server):
    result = json.loads(_issue_request(
        server_uri=(server + "list"),
    ))
    
    if result['single']:
        print("Single-host tasks:")
        for task in result['single']:
            print("\t{name} ({date})".format(
                name=task['name'],
                date=task['date'],
            ))
            print("\tID: {id}".format(
                id=task['instructions_id'],
            ))
            if not task.get('retry', True):
                print("\tTask will not be retried upon failure")
            if task.get('cull'):
                print("\tTask will be removed prior to next execution")
            print("\tHost: {host}".format(
                host=task['host'],
            ))
            print("")
            
    if result['multi']:
        print("Multi-host tasks:")
        for task in result['multi']:
            print("\t{name} ({date})".format(
                name=task['name'],
                date=task['date'],
            ))
            print("\tID: {id}".format(
                id=task['instructions_id'],
            ))
            if not task.get('retry', True):
                print("\tTask will not be retried upon failure")
            if task.get('cull'):
                print("\tTask will be removed prior to next execution")
            print("\tHosts:")
            for host in task['hosts']:
                print("\t\t{host}".format(
                    host=host,
                ))
            print("")
            
def remove_single(server, instructions_id):
    _issue_request(
        server_uri=(server + "remove-single"),
        payload=json.dumps({
            'instructions_id': instructions_id,
        }),
    )
    
def remove_multi(server, instructions_id):
    _issue_request(
        server_uri=(server + "remove-multi"),
        payload=json.dumps({
            'instructions_id': instructions_id,
        }),
    )
    
def remove_host(server, host):
    _issue_request(
        server_uri=(server + "remove-host"),
        payload=json.dumps({
            'host': host,
        }),
    )
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manage a Chorus server')
    parser.add_argument(
        '--pause', action='store_true',
        help='pause execution',
    )
    parser.add_argument(
        '--restart', action='store_true',
        help='restart execution',
    )
    parser.add_argument(
        '--list', action='store_true',
        help='list outstanding tasks',
    )
    parser.add_argument(
        '--remove-multi', metavar='ID',
        help='remove a multi-target task, given its ID',
    )
    parser.add_argument(
        '--remove-single', metavar='ID',
        help='remove a single-target task, given its ID',
    )
    parser.add_argument(
        '--remove-host', metavar='HOST',
        help='remove all tasks associated with a host',
    )
    parser.add_argument(
        '--server', default='http://localhost:46092/',
        help='the address to communicate with',
    )
    args = parser.parse_args()
    
    if args.pause:
        pause(args.server)
        
    if args.restart:
        restart(args.server)
        
    if args.remove_multi:
        remove_multi(args.server, args.remove_multi)
        
    if args.remove_single:
        remove_single(args.server, args.remove_single)
        
    if args.remove_host:
        remove_host(args.server, args.remove_host)
        
    if args.list:
        list_tasks(args.server)
        
